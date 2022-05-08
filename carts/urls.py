from django.urls import path
from carts import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:item_id>/', views.add_cart, name='add_cart'),
    path('minus_cart/<int:item_id>/<int:cart_item_id>/', views.minus_cart, name='minus_cart'),
    path('remove_cart_item/<int:item_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),

    path('checkout/', views.checkout, name='checkout'),
]
