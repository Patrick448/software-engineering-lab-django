from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, CustomerViewSet
from .views import ProductListView, ProductDetailView, ProductCreateView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/products/', ProductListView.as_view(),
    name='product_list'),
    path('user/products/<int:pk>/', ProductDetailView.as_view(),
    name='product_detail'),
    path('user/products/new/', ProductCreateView.as_view(),
    name='product_create')
]

