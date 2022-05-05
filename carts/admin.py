from django.contrib import admin
from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_add',)

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'cart', 'quantity', 'is_active')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)