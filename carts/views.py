from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from store.models import Item, Variation


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, item_id):
    item = Item.objects.get(id=item_id)
    item_variation = []
    if request.method == 'POST':
        for product in request.POST:
            key = product
            value = request.POST[key]

            try:
                variation = Variation.objects.get(item=item, variation_category__iexact=key, variation_value__iexact=value)
                item_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(item=item, cart=cart)
        if len(item_variation) > 0:
            cart_item.variations.clear()
            for product in item_variation:
                cart_item.variations.add(product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            item = item,
            quantity = 1,
            cart = cart,
        )
        if len(item_variation) > 0:
            cart_item.variations.clear()
            for product in item_variation:
                cart_item.variations.add(product)
        cart.save()
    return redirect('cart')


def minus_cart(request, item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    item = get_object_or_404(Item, id=item_id)
    cart_item = CartItem.objects.get(item=item, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.item.public_price * cart_item.quantity)
            quantity += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
    }
    return render(request, 'store/cart.html', context)