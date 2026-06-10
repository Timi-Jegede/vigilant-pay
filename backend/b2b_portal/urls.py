from django.urls import path
from .views import ClientDashboardView

app_name = 'b2b_portal'

urlpatterns = [
    path('client-dashboard', ClientDashboardView.as_view(), name='cient_dashboard')
]
