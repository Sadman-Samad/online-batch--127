from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_views, name='cart_views'),
    path('create/order/', views.create_order, name='create_order'),
    path('remove/cart/item/<int:id>/', views.remove_cart_item, name='remove_cart_item'),
    path('<int:id>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/update/<int:id>/', views.product_update, name='product_update'),
    path('product/add//cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('add/coupon/', views.add_coupon, name='add_coupon'),
    path('add/wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
]