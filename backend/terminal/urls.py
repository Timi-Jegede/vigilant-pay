from django.urls import path
from . import views

app_name = 'terminal'

urlpatterns = [
    path('endpoint', views.endpoint, name='endpoint'),
    path('card-terminal', views.card_terminal, name='card_terminal'),
    path('countries-json', views.countries_json, name='countries_json'),
    path('save-transaction', views.save_transaction, name='save_transaction'),
]