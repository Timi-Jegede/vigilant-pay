from rest_framework import serializers
from .models import FraudDetectionSDKUser, DeviceFingerprint, FraudDetectionSDKTimelineEvent

class APISDKEventSerializers(serializers.Serializer):
    account_id = serializers.CharField(max_length=255)
    event_type = serializers.CharField(max_length=50)
    description = serializers.CharField()

    client_platform = serializers.CharField(max_length=50)
    device_id = serializers.CharField(max_length=255)
    os_version = serializers.CharField(max_length=20)
    device_model = serializers.CharField(max_length=100)
    is_rooted_or_jailbroken = serializers.BooleanField(default=False)
    paste_detected = serializers.BooleanField(default=False)
    typing_speed_cps = serializers.FloatField(required=False, allow_null=True)

    def validate_account_id(self, value):
        return value
    
    def create(self, validated_data):
        account_id = validated_data.pop('account_id')
        fraud_detection_profile, _ = FraudDetectionSDKUser.objects.get_or_create(
            external_user_id=account_id
        )

        client_platform_str = validated_data.pop('client_platform')
        device_id = validated_data.pop('device_id')
        os_version = validated_data.pop('os_version')
        device_model = validated_data.pop('device_model')
        is_rooted_or_jailbroken = validated_data.pop('is_rooted_or_jailbroken')

        device, _ = DeviceFingerprint.objects.update_or_create(
            device_id=device_id,
            defaults={
                'user': fraud_detection_profile,
                'os_version': os_version,
                'device_model': device_model,
                'is_rooted_or_jailbroken': is_rooted_or_jailbroken
            }
        )

        timeline_event = FraudDetectionSDKTimelineEvent.objects.create(
            user=fraud_detection_profile,
            device=device,
            event_type=validated_data.get('event_type'),
            description=validated_data.get('description'),
            paste_detected=validated_data.get('paste_detected', False),
            typing_speed_cps=validated_data.get('typing_speed_cps', 0.0)
        )

        self._calculate_instant_risk(fraud_detection_profile, timeline_event)

        return timeline_event
    
    def _calculate_instant_risk(self, profile, event):
        score_increase = 0

        if event.typing_speed_cps and event.typing_speed_cps > 40.0:
            score_increase += 30
            event.description += ' [ALERT: Abnormally fast input layout]'
    
        if event.paste_detected and event.event_type == 'TRANSACTION VERIFICATION':
            score_increase += 20
            event.description += ' [ALERT: Clipboard bypass on payment field]'
        
        if event.device and event.device.is_rooted_or_jailbroken:
            score_increase += 40
            event.description += ' [ALERT: Rooted hardware environment]'
        
        if score_increase > 0:
            event.save()
            profile.risk_score = min(profile.risk_score + score_increase, 100)
            profile.save()

class APISDKTimelineReadSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source='device.device_model', read_only=True)
    current_risk_user = serializers.IntegerField(source='fraud_detection_profile.risk_score', read_only=True)

    class Meta:
        model = FraudDetectionSDKTimelineEvent
        fields = [
            'id',
            'user_id',
            'current_risk_user',
            'event_type',
            'description',
            'timestamp',
            'paste_detected',
            'typing_speed_cps',
            'device_name',
        ]
                                                
                                                