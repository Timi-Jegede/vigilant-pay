from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.postgres.search import SearchQuery
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()

# Create your views here.

def dashboard(request):
    return render(request, 'system_admin/dashboard/index.html')

def kpis_charts(request):
    return render(request, 'system_admin/sections/kpis_charts.html')

@require_http_methods(['GET'])
def search_user(request):
    search_term = request.GET.get('q', '')
    if not search_term:
        return JsonResponse({'users': []})
    
    id = User.objects.get(username__icontains=search_term).id
    return id
