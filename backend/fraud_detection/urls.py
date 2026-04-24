from django.urls import path

from . import views

urlpatterns = [
    path('predict/', views.predict_fraud, name='predict_fraud'),
    path('stats/', views.stats, name='stats'),
    path('signup', views.signup, name='signup'),
    path('register_users', views.register_users, name='register_users')
]