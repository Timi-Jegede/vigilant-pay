from django.urls import path
from . import views
from login import views as login_views
from dashboard import kpis_app

app_name = 'system_admin'

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('settings/profile', views.admin_profile, name='admin_profile'),
    path('settings/security', views.admin_security, name='admin_security'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('logout', login_views.logout_view, name='logout'),
]