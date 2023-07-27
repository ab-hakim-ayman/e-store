from django.urls import path
from .views import *


urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('category/<int:pk>/', CategoryView.as_view()),
    path('brand/', BrandView.as_view()),
    path('brand/<int:pk>/', BrandView.as_view()),
    path('product/', ProductView.as_view()),
    # path('product/<int:pk>/', ProductView.as_view()),
    path('product/<int:pk>/', Visits.as_view()),
    path('brand-product/', BrandProductView.as_view()),
    path('category-product/', CategoryProductView.as_view()),
    path('brand-product/<int:pk>/', SingleBrandProductView.as_view()),
    path('category-product/<int:pk>/', SingleCategoryProductView.as_view()),
    path('category-product/<int:pk>/', SingleCategoryProductView.as_view()),
]
