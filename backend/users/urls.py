from django.urls import path
from . import views, transaction_overview
from login import views as login_views

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('security', views.user_security, name='user_security'),
    path('security-log', views.security_log, name='security_log'),
    path('profile', views.user_profile, name='user_profile'),
    path('logout', login_views.logout_view, name='logout'),
    path('user-details', views.user_details, name='user_details')
]