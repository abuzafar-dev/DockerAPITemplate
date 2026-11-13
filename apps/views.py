from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import User
from apps.permissions import UserPermission
from apps.serializers import CalculatorResultSerializer, CalculatorSerializer, UserSerializer


class HealthCheckView(APIView):
    @extend_schema(responses=inline_serializer('Health', {'status': serializers.CharField()}))
    def get(self, request):
        return Response({'status': 'ok'})


class UserViewSet(viewsets.ModelViewSet):
    """Foydalanuvchilar CRUD. POST — ro'yxatdan o'tish; admin hammani, oddiy user faqat o'zini ko'radi."""

    serializer_class = UserSerializer
    permission_classes = [UserPermission]

    def get_queryset(self):
        queryset = User.objects.order_by('id')
        if not self.request.user.is_staff:
            queryset = queryset.filter(pk=self.request.user.pk)
        return queryset



# --- Function-based view namunalari (@api_view) ---

@extend_schema(responses=CalculatorResultSerializer, tags=['calculator'])
@api_view(['GET'])
def calculator_path(request, n1: int, n2: int):
    """Path parametr: /api/calculator/path/5/7/"""
    return Response({'result': n1 + n2})


@extend_schema(parameters=[CalculatorSerializer], responses=CalculatorResultSerializer, tags=['calculator'])
@api_view(['GET'])
def calculator_query(request):
    """Query parametr: /api/calculator/query/?n1=5&n2=7 — noto'g'ri qiymatda 400."""
    serializer = CalculatorSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    return Response({'result': data['n1'] + data['n2']})
