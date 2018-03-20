from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()


def get_data(request, *args):
    data = {
        "sales": 100,
        "customers": 10,
    }
    return JsonResponse(data) # http response




class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data = {
            "sales": 100,
            "customers": 10,
        }

        return Response(data)