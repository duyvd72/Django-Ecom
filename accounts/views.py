from django.http import HttpResponse
from django.shortcuts import render, redirect

from carts.models import Cart, CartItem
from carts.views import _cart_id
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            username = email.split("@")[0]
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            messages.success(request, 'Registration successful!')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart)
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # Getting the item variations by cart id
                    item_variation = []
                    for product in cart_item:
                        variation = product.variations.all()
                        item_variation.append(list(variation))

                    # Getting the cart items from the user to access his item variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for product in cart_item:
                        existing_variation = product.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(product.id)

                    for pr in item_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            product_id = id[index]
                            product = CartItem.objects.get(id=product_id)
                            product.quantity += 1
                            product.user = user
                            product.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for product in cart_item:
                                product.user = user
                                product.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)

            except:
                return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('login')


def activate(request, uidb64, token):
    return HttpResponse('ok')
