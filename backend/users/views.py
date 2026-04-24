from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

# Create your views here.

@login_required
def index(request):
    user_id = request.user.id

    dash_context = {
        'session-user-id': {'data': user_id}
    }
    dash_context_string = json.dumps(dash_context)

    return render(request, 'users/sections/index.html', {'dash_context': dash_context_string})

@login_required
def user_security(request):
    return render(request, 'users/settings/user-security.html')

@login_required
def security_log(request):
    return render(request, 'users/sections/security-log.html')

@login_required
def user_profile(request):
    return render(request, 'users/settings/user-profile.html')

@login_required
def user_details(request):
    first_name = request.user.first_name
    last_name = request.user.last_name

    return JsonResponse({'user_details': f'{first_name} {last_name}'})

