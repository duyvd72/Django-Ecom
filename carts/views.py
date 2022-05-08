from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from carts.models import Cart, CartItem
from store.models import Item, Variation
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, item_id):
    current_user = request.user
    item = Item.objects.get(id=item_id)
    if current_user.is_authenticated:
        item_variation = []
        if request.method == 'POST':
            for product in request.POST:
                key = product
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(item=item, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    item_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(item=item, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(item=item, user=current_user)
            ex_var_list = []
            id = []
            for product in cart_item:
                existing_variation = product.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(product.id)

            if item_variation in ex_var_list:
                index = ex_var_list.index(item_variation)
                product_id = id[index]
                product = CartItem.objects.get(item=item, id=product_id)
                product.quantity += 1
                product.save()

            else:
                product = CartItem.objects.create(item=item, quantity=1, user=current_user)
                if len(item_variation) > 0:
                    product.variations.clear()
                    product.variations.add(*item_variation)
                product.save()
        else:
            cart_item = CartItem.objects.create(
                item=item,
                quantity=1,
                user=current_user,
            )
            if len(item_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*item_variation)
            cart_item.save()
        return redirect('cart')
    else:
        item_variation = []
        if request.method == 'POST':
            for product in request.POST:
                key = product
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(item=item, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    item_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(item=item, cart=cart)

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(item=item, cart=cart)

            ex_var_list = []
            id = []
            for product in cart_item:
                existing_variation = product.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(product.id)

            print(ex_var_list)

            if item_variation in ex_var_list:
                index = ex_var_list.index(item_variation)
                product_id = id[index]
                product = CartItem.objects.get(item=item, id=product_id)
                product.quantity += 1
                product.save()

            else:
                product = CartItem.objects.create(item=item, quantity=1, cart=cart)
                if len(item_variation) > 0:
                    product.variations.clear()
                    product.variations.add(*item_variation)
                product.save()
        else:
            cart_item = CartItem.objects.create(
                item=item,
                quantity=1,
                cart=cart,
            )
            if len(item_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*item_variation)
            cart.save()
        return redirect('cart')


def minus_cart(request, item_id, cart_item_id):
    item = get_object_or_404(Item, id=item_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(item=item, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(item=item, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_cart_item(request, item_id, cart_item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(item=item, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(item=item, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
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
    return render(request, 'store/checkout.html', context)