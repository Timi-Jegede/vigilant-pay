from django.urls import path
from .views import AdminView
from .views import AlertQueueAndManagementView, AdminDashboardView, FraudUserDataAndTimelineView, FraudDetectionSDK

app_name = 'system_admin'

urlpatterns = [
    path('base', AdminView.as_view(), name='base'),
    path('alert-queue-and-management', AlertQueueAndManagementView.as_view(), name='alert_queue_and_management'),
    path('admin-dashboard', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('user-data-and-timeline/<user_id>', FraudUserDataAndTimelineView.as_view(), name='user_data_and_timeline'),
    path('fraud-detection-sdk/', FraudDetectionSDK.as_view(), name='fraud_detection_sdk')
]