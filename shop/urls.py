from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import ShopViewSet, ProductCreateAPIView

router = DefaultRouter()
router.register('stores', ShopViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('products/add/', ProductCreateAPIView.as_view(), name='add_product'),
]
