from django.urls import path
from . import views
from . import dash_app, kpis_app

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/search-user/', views.search_user, name='search_user'),
    path('dashboard/kpis-charts', views.kpis_charts, name='kpis_charts')
]