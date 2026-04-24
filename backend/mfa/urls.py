from django.urls import path
from . import views

app_name = 'mfa'

urlpatterns = [
    path('verify', views.verify_mfa, name='verify_mfa'),
    path('mfa-status', views.set_mfa_status, name='mfa_status'),
    path('setup-mfa', views.setup_mfa, name='setup_mfa'),
    path('setup-uri', views.setup_uri, name='setup_uri'),
    path('complete-mfa-setup', views.complete_mfa_setup, name='complete_mfa_setup'),
    path('mfa-configured-status', views.get_mfa_configured_status, name='mfa_configured_status'),
]
