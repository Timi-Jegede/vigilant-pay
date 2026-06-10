from django.shortcuts import render
from rest_framework.views import APIView

class ClientDashboardView(APIView):
    def get(self, request):
        return render(request, 'client/base.html')