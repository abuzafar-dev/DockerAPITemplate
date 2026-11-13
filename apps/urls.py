from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.views import HealthCheckView, UserViewSet, calculator_path, calculator_query

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('calculator/path/<int:n1>/<int:n2>/', calculator_path, name='calculator-path'),
    path('calculator/query/', calculator_query, name='calculator-query'),
] + router.urls
