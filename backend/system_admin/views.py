import pyotp
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    return render(request, 'admin/sections/admin-index.html')

def admin_profile(request):
    return render(request, 'admin/settings/admin-profile.html')

def admin_security(request):
    return render(request, 'admin/settings/admin-security.html')

def admin_dashboard(request):
    return render(request, 'admin/dashboard/dashboard.html')