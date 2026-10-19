from rest_framework.routers import DefaultRouter

from products.views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('products', ProductViewSet, basename='product')

urlpatterns = router.urls
