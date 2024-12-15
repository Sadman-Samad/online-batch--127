from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/update/<int:id>/', views.product_update, name='product_update'),
    path('product/add//cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
]