from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

class AdminView(APIView):
    def get(self, request):
        return render(request, 'admin/base.html')

class AlertQueueAndManagementView(APIView):
    def get(self, request):
        return render(request, 'admin/sections/alert-queue-and-management.html')