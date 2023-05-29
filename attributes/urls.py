from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import FamilyList, FamilyDetail, CategoryList, CategoryDetail, BrandList, BrandDetail, ProductList, ProductDetail, ProductAttributeList, ProductAttributeDetail

schema_view = get_schema_view(
    openapi.Info(
        title="Product attributes labelling  API",
        default_version='v1',
        description="Your project API description",
        
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('families/', FamilyList.as_view(), name='family_list'),
    path('families/<int:pk>/', FamilyDetail.as_view(), name='family_detail'),
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
    path('brands/', BrandList.as_view(), name='brand_list'),
    path('brands/<int:pk>/', BrandDetail.as_view(), name='brand_detail'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('product-attributes/', ProductAttributeList.as_view(), name='product_attribute_list'),
    path('product-attributes/<int:pk>/', ProductAttributeDetail.as_view(), name='product_attribute_detail'),
]
