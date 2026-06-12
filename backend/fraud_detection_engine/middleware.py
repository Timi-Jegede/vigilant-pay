from django.conf import settings
from django.http import JsonResponse
import geoip2.database
from django.core.exceptions import MiddlewareNotUsed
import json
from .models import ClientPlatform
import logging
import sys

logger = logging.getLogger(__name__)

try:
    CITY_READER = geoip2.database.Reader(settings.MAXMIND_CITY_DB_PATH)
except Exception as e:
    logger.error(f'MaxMind City Database failed to load: {e}')
    CITY_READER = None

try:
    ASN_READER = geoip2.database.Reader(settings.MAXMIND_ASN_DB_PATH)
except Exception as e:
    logger.error(f'MaxMind ASN Database failed to load: {e}')
    ASN_READER = None

RESIDENTIAL_CLEAN = 0
VPN_OR_PROXY = 1
HOSTING_DATACENTER = 2
UNKNOWN_UNCLASSIFIED = -1

class FraudSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        remote_addr = request.META.get('REMOTE_ADDR')

        if remote_addr in getattr(settings, 'TRUSTED_PROXY_IPS', []):
            x_forwarded_for = request.headers.get('x-forwarded-for')

            if x_forwarded_for:
                client_ip = [ip.strip() for ip in x_forwarded_for.split(',') if ip.strip()]
            else:
                client_ip = remote_addr
        
        else:
            client_ip = remote_addr

        if client_ip in getattr(settings, 'BLACKLISTED_IPS', []):
            return JsonResponse({'error': 'Security Block', 'code': 403}, status=403)
        

        request.client_ip = client_ip

        return self.get_response(request)

class NewAccountSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path == '/api/pay' and request.method =='POST':
            if request.user.is_authenticated:           
                limit = request.user.profile.transaction_limit

                if limit is not None:
                    try:
                        data = json.loads(request.body)
                        amount = float(data.get('amount', 0))

                        if amount > limit:
                            return JsonResponse({
                                'error': 'limit_exceeded',
                                'limit': limit,
                                'message': f'Your current account limit is ${limit}'
                            }, status=403)
                    except (json.JSONDecodeError, ValueError):
                        pass

        return self.get_response(request)

class FraudDataEnrichmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        if not CITY_READER or not ASN_READER:
            missing_databases = []
            if not CITY_READER: missing_databases.append('CITY DB')
            if not ASN_READER: missing_databases.append('ASN DB')

            error_msg = f'\nFraudDataEnrichmentMiddleware deactivated: Missing databases: {', '.join(missing_databases)}\n\n'
            
            if missing_databases:
                sys.stdout.write(error_msg)
                sys.stdout.flush()

                raise MiddlewareNotUsed(error_msg)
    
    def __call__(self, request):
        ip = self.get_secure_client_ip(request)

        request.json_payload = {}
        request.ip_intelligence = {
            'ip_address': ip,
            'latitude': 0.0,
            'longitude': 0.0,
            'f9_isp_classification': RESIDENTIAL_CLEAN,
            'country_code': 'XX'
        }

        content_type = request.META.get('CONTENT_TYPE', '').lower()

        if request.method == 'POST' and 'application/json' in content_type:
            try:
                raw_body = request.body
                if raw_body:
                    request.json_payload = json.loads(raw_body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Malformed JSON Payload'}, status=400)

        if request.method == 'POST':
            sender = request.json_payload.get('sender')
            
            if not sender or not isinstance(sender, dict) or not sender.get('external_id'):
                return JsonResponse({
                    'error': 'Invalid payload',
                    'message': 'Transaction evaluation aborted: Sender validation identifier is missing.'
                }, status=400)

        if not ip:
            request.ip_intelligence.update({
                'latitude': None,
                'longitude': None,
                'f9_isp_classification': UNKNOWN_UNCLASSIFIED
            })
            return self.get_response(request)

        if CITY_READER:
            try: 
                city_res = CITY_READER.city(ip)
                request.ip_intelligence.update({
                    'latitude': city_res.location.latitude,
                    'longitude': city_res.location.longitude,
                    'country_code': city_res.country.iso_code or 'XX'
                })
            except Exception:
                request.ip_intelligence.update({
                    'latitude': None,
                    'longitude': None,
                    'country_code': 'XX'
                })

        if ASN_READER:
            try:
                asn_res = ASN_READER.asn(ip)
                asn_number = asn_res.autonomous_system_number
                org_name = (asn_res.autonomous_system_organization or '').lower()

                if not org_name and not asn_number:
                    request.ip_intelligence.update(
                        {
                            'f9_isp_classification': UNKNOWN_UNCLASSIFIED
                        }
                    )
                else:
                    datacenter_asns = {16509, 15169, 14061, 24940, 63949}
                    
                    if asn_number in datacenter_asns:
                        request.ip_intelligence.update(
                            {
                                'f9_isp_classification': HOSTING_DATACENTER
                            }
                        )
                    else:
                        hosting_keywords = ['amazon', 'aws', 'google cloud', 'digitalocean', 'linode', 'ovh', 'hetzner']
                        if any(keyword in org_name for keyword in hosting_keywords):
                            request.ip_intelligence.update(
                                {
                                    'f9_isp_classification': HOSTING_DATACENTER
                                }
                            )
                        elif 'proxy' in org_name or 'vpn' in org_name:
                            request.ip_intelligence.update(
                                {
                                    'f9_isp_classification': VPN_OR_PROXY
                                }
                            )
                        else:
                            request.ip_intelligence.update(
                                {
                                    'f9_isp_classification': RESIDENTIAL_CLEAN
                                }
                            )
            except Exception:
                request.ip_intelligence.update(
                    {
                        'f9_isp_classification': UNKNOWN_UNCLASSIFIED
                    }
                )

        country = request.ip_intelligence.get('country_code', 'XX')
        transaction_block = request.json_payload.get('transaction', {})
        
        try:
            amount = float(transaction_block.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0.0

        if country in ['KP', 'IR'] and amount > 0:
            return JsonResponse({
                'status': 'DENIED',
                'reason': 'Regulatory compliance intercept: Sanctioned zone transaction block.'
            }, status=403)

        return self.get_response(request)

    def get_secure_client_ip(self, request):
        remote_addr = request.META.get('REMOTE_ADDR')

        x_forwarded_for = (
            request.headers.get('X-Forwarded-For') or
            request.headers.get('x-forwarded-for') or
            request.META.get('HTTP_X_FORWARDED_FOR')
        )
        
        trusted_proxies = getattr(settings, 'TRUSTED_PROXY_IPS', [])
        if not trusted_proxies:
            return remote_addr
        
        if remote_addr not in trusted_proxies:
            return remote_addr
        
        if not x_forwarded_for:
            return remote_addr
        
        ip_chain = [ip.strip() for ip in x_forwarded_for.split(',') if ip.strip()]

        for ip in reversed(ip_chain):
            if ip not in trusted_proxies:
                return ip
            
        return remote_addr

class ClientPlatformAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        client_authentication = request.headers.get('authorization')

        if client_authentication:
            try:
                authenticated_platform = ClientPlatform.objects.get(
                    api_key=client_authentication
                )

                request.auth_platform = authenticated_platform
            
            except ClientPlatform.DoesNotExist:
                return JsonResponse({'Error': 'Invalid platform authentication key.'}, status=500)

            except Exception as e:
                return JsonResponse({'Error': 'Unable to authenticate platform.'}, status=401)
        
        return self.get_response(request)