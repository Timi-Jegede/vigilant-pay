import time
import math
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg, StdDev, Max
from fraud_detection_engine.models import AccountEntity, FinancialLegderEntry
from django.core.cache import cache
import geoip2.database 
from django.db import transaction as db_transaction
import json

class MLFeatureService:
    try:
        CITY_READER = geoip2.database.Reader(settings.MAXMIND_CITY_DB_PATH)
        ASN_READER = geoip2.database.Reader(settings.MAXMIND_ASN_DB_PATH)
        ANON_READER = geoip2.database.Reader(settings.MAXMIND_ANON_DB_PATH)
    except Exception:
        CITY_READER, ASN_READER, ANON_READER = None, None, None
    
    RESIDENTIAL_CLEAN = 0
    VPN_OR_PROXY = 1
    HOSTING_DATACENTER = 2
    UNKNOWN_UNCLASSIFIED = -1

    @staticmethod
    def extract_all_ml_features(payload, platform, current_lat, current_lon, f9_isp_classification):
        redis_client = cache._cache.get_client()
        now_ts = time.time()

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except json.JSONDecodeError:
                payload = {}

        tx_sender = payload.get('sender', {})
        tx_recipient = payload.get('recipient', {})
        transaction = payload.get('transaction', {})
        sender_id = tx_sender.get('external_id')
        receiver_id = tx_recipient.get('account_number_hash')
        transaction_id = transaction.get('transaction_id', f'tx_{now_ts}_{sender_id}')
        current_device = tx_sender.get('device_fingerprint', 'UNKNOWN')

        try:
            current_amount = float(transaction.get('amount', 0.0))
            avail_balance = float(transaction.get('current_avail_balance', 0.0))
        except (ValueError, TypeError):
            current_amount = 0.0
            avail_balance = 0.0

        sender_key = f'velocity:sender:{platform.id}:{sender_id}'

        identity_hash = tx_sender.get('identiy_hash', 'unknown')
        cold_start_risk_score = 0.0

        with db_transaction.atomic():
            sender, created_sender = AccountEntity.account_entity_records(
                platform_id=platform.id,
                external_account_id=sender_id,
                identity_hash=identity_hash
            )

            receiver, created_receiver = AccountEntity.account_entity_records(
                platform_id=platform.id,
                external_account_id=receiver_id,
                identity_hash=receiver_id
            )

            ledger_entry = FinancialLegderEntry.financial_legder_entry_records(
                platform_id=platform.id,
                transaction_id=transaction_id,
                sender=sender,
                receiver=receiver,
                risk_score=cold_start_risk_score,
                amount=current_amount
            )

            if created_sender:
                sender.precalculated_daily_average = current_amount
                sender.save()

        pipe = redis_client.pipeline()
        pipe.zremrangebyscore(sender_key, 0, now_ts - 900)
        pipe.zadd(sender_key, {str(now_ts): now_ts})
        pipe.zcard(sender_key)
        pipe.zrevrange(sender_key, 1, 1, withscores=True)
        pipe.expire(sender_key, 86400)    
        _, _, count_15m, last_item, _, = pipe.execute()

        daily_baseline = float(sender.precalculated_daily_average) if sender.precalculated_daily_average > 0 else 1.0
        f1_velocity_ratio = count_15m / (daily_baseline if daily_baseline > 0 else 1.0)

        f2_balance_drain_ratio = current_amount / max(avail_balance, 1.0)

        f3_time_gap_seconds = -1.0
        if last_item:
            last_ts = last_item[0][1]
            f3_time_gap_seconds = now_ts - last_ts


        mule_key = f'mule:receiver:{platform.id}:{receiver_id}'
        fanout_key = f'fanout:sender:{platform.id}:{sender_id}'

        redis_client.sadd(mule_key, sender_id)
        redis_client.expire(mule_key, 86400)

        redis_client.sadd(fanout_key, receiver_id)
        redis_client.expire(fanout_key, 3600)

        f4_mule_indicator = float(redis_client.scard(mule_key))

        f5_fanout_ratio = float(redis_client.scard(fanout_key))

        f6_recipient_historical_risk = 1.0 if receiver.is_blacklisted else float(receiver.trust_score)

        trusted_devices_list = getattr(sender, 'trusted_devices', [])

        f7_is_new_device = 0.0 if current_device in trusted_devices_list else 1.0

        geo_key = f'geo:user:{platform.id}:{sender_id}'
        last_geo = redis_client.get(geo_key)

        f8_geo_velocity = 0.0

        if last_geo:
            try:
                l_lat, l_lon, l_ts = last_geo.split(',')
                distance = MLFeatureService.calculate_haversine(current_lat, current_lon, float(l_lat), float(l_lon))
                time_elapsed_hours = (now_ts - float(l_ts)) / 3600.0
                
                if time_elapsed_hours > 0.0001:
                    f8_geo_velocity = distance / time_elapsed_hours
                else:
                    f8_geo_velocity = distance / 0.0001
            
            except (ValueError, TypeError):
                f8_geo_velocity = 0.0
        
        else:
            f8_geo_velocity = 0.0

        redis_client.set(geo_key, f'{current_lat},{current_lon},{now_ts}', ex=86400)

        history = FinancialLegderEntry.objects.filter(sender=sender).aggregate(
            avg_amt=Avg('amount'),
            std_amt=StdDev('amount'),
            max_amt=Max('amount')
        )

        hist_avg = float(history['avg_amt'] or current_amount)
        hist_std = float(history['std_amt'] or 1.0)
        hist_max = float(history['max_amt'] or current_amount)

        f10_amount_z_score = (current_amount - hist_avg) / max(hist_std, 0.01)

        f11_max_multiplier = current_amount / max(hist_max, 1.0)

        feature_list = [
            f1_velocity_ratio, f2_balance_drain_ratio, f3_time_gap_seconds,
            f4_mule_indicator, f5_fanout_ratio, f6_recipient_historical_risk,
            f7_is_new_device, f8_geo_velocity, f9_isp_classification,
            f10_amount_z_score, f11_max_multiplier
        ]

        return feature_list

    @staticmethod
    def calculate_haversine(lat1, lon1, lat2, lon2):
        radius = 3956
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) * math.sin(dlon / 2))
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return radius * c
    
    @staticmethod
    def get_ip_coordinates(ip):
        try:
            with MLFeatureService.CITY_READER as reader:
                city_res = reader.city(ip)

                latitude = city_res.location.latitude
                longitude = city_res.location.longitude

                return {
                    'latitude': latitude,
                    'longitude': longitude
                }
        
        except Exception as e:
            return {
                'latitude': latitude,
                'longitude': longitude
            }
    
    @staticmethod
    def get_isp_classification(ip):
        if not settings.DEBUG:
            try:
                with MLFeatureService.ANON_READER as reader:
                    anon_res = reader.anonymous_ip(ip)

                    if (
                        anon_res.is_public_proxy
                        or anon_res.is_anonymous_vpn
                        or anon_res.is_tor_exit_node
                    ):
                        return MLFeatureService.VPN_OR_PROXY
                    
                    elif anon_res.is_hosting_provider:
                        return MLFeatureService.HOSTING_DATACENTER
                    
                    else:
                        return MLFeatureService.RESIDENTIAL_CLEAN
                    
            except Exception as e:
                return MLFeatureService.UNKNOWN_UNCLASSIFIED
        
        try:
            with MLFeatureService.ASN_READER as reader:
                asn_res = reader.asn(ip)

                asn_number = asn_res.autonomous_system_number
                org_name = (asn_res.autonomous_system_organization or '').lower()

                if not org_name and not asn_number:
                    return MLFeatureService.UNKNOWN_UNCLASSIFIED
                
                else:
                    datacenter_asns = {16509, 15169, 14061, 24940, 63949}

                    if asn_number in datacenter_asns:
                        return MLFeatureService.HOSTING_DATACENTER
                    
                    else:
                        hosting_keywords = [
                            'amazon', 'aws', 'google cloud', 'digitalocean', 'linode',
                            'ovh', 'hetzner', 'microsoft store', 'leaseweb', 'vultr'
                        ]

                        if any(keyword in org_name for keyword in hosting_keywords):
                            return MLFeatureService.HOSTING_DATACENTER
                        
                        elif 'proxy' in org_name or 'vpn' in org_name:
                            return MLFeatureService.VPN_OR_PROXY

                        else:
                            return MLFeatureService.RESIDENTIAL_CLEAN
       
        except Exception as e:
            return MLFeatureService.UNKNOWN_UNCLASSIFIED

