from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import APISDKEventSerializers, APISDKTimelineReadSerializer
from .models import FraudDetectionSDKUser, FraudDetectionSDKTimelineEvent, DeviceFingerprint
import json
# from .models import AppEvent

# Create your views here.

class AdminView(APIView):
    def get(self, request):
        return render(request, 'admin/base.html')

class AlertQueueAndManagementView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin/sections/alert-queue-and-management.html')

class FraudDetectionSDK(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializers = APISDKEventSerializers(data=request.data)

        if serializers.is_valid():
            serializers.save()

            return Response(
                {'status': 'success', 'message': 'Event data packet ingested successfully.'                 
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDashboardView(APIView):
    def get(self, request):
        try:
            suspicious_alerts = FraudDetectionSDKTimelineEvent.objects.filter(
                typing_speed_cps__gte=90
            ) | FraudDetectionSDKTimelineEvent.objects.filter(
                paste_detected=True
            )

            live_alerts = suspicious_alerts.order_by('-timestamp')

            serializer = APISDKTimelineReadSerializer(live_alerts, many=True)

            return Response({
                'total_live_alerts': live_alerts.count(),
                'alerts': serializer.data
            })
        
        except Exception as e:
            print(f'Error fetching live alerts {e}')
            return Response({'error': 'Error fetching live alerts'})

class FraudUserDataAndTimelineView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        try:
            try:
                fraud_user_profile = FraudDetectionSDKUser.objects.get(id=user_id)
            except FraudDetectionSDKUser.DoesNotExist:
                return Response({'error': 'User profile not found'},
                                status=status.HTTP_404_NOT_FOUND)
            
            devices_queryset = fraud_user_profile.devices.all()
            events_queryset = fraud_user_profile.events.all().order_by('-timestamp')

            device_list = []
            for device in devices_queryset:
                specific_device_usages = events_queryset.filter(device=device).count()

                if specific_device_usages <= 1:
                    device_age_string = 'New Device Detected'
                else:
                    device_age_string = f'Old device detected. User {specific_device_usages - 1} times before'

                device_list.append({
                    'device_model': device.device_model,
                    'is_rooted_or_jailbroken': device.is_rooted_or_jailbroken,
                    'device_age_status': device_age_string
                })
            
            user_transaction = []
            for transaction_history in events_queryset:
                user_transaction.append({
                    'event_type': transaction_history.event_type,
                    'description': transaction_history.description,
                    'timestamp': transaction_history.timestamp
                })
            
            response_payload = {
                'user_id': user_id,
                'risk_score': getattr(fraud_user_profile, 'risk_score', 0),
                'devices_tracked': device_list,
                'transaction_history': user_transaction
            }

            return Response(response_payload, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(f'Error fetching data and timeline {e}')
            return Response({
                'error': 'Error fetching data and timeline'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)