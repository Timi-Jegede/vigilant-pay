from django.urls import path
from .views import AdminView
from .views import AlertQueueAndManagementView

app_name = 'system_admin'

urlpatterns = [
    path('base', AdminView.as_view(), name='base'),
    path('alert-queue-and-management', AlertQueueAndManagementView.as_view(), name='alert_queue_and_management')
]