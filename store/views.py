from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from carts.models import CartItem
from carts.views import _cart_id
from store.models import Item, ItemType
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def store(request, item_type_slug=None):
    item_type = None
    items = None

    if item_type_slug != None:
        item_type = get_object_or_404(ItemType, slug=item_type_slug)
        items = Item.objects.filter(item_type=item_type, is_available=True)
        paginator = Paginator(items, 6)
        page = request.GET.get('page')
        paged_items = paginator.get_page(page)
        item_count = items.count()
    else:
        items = Item.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(items, 6)
        page = request.GET.get('page')
        paged_items = paginator.get_page(page)
        item_count = items.count()

    context = {
        'items': paged_items,
        'item_count': item_count,
    }
    return render(request, 'store/store.html', context)


def item_detail(request, item_type_slug, item_slug):
    try:
        single_item = Item.objects.get(item_type__slug=item_type_slug, slug=item_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), item=single_item).exists()
    except Exception as e:
        raise e

    context = {
        'single_item': single_item,
        'in_cart': in_cart,
    }
    return render(request, 'store/item_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            items = Item.objects.filter(Q(description__icontains=keyword) |  Q(item_name__icontains=keyword))
            item_count = items.count()
    context = {
        'items': items,
        'item_count': item_count,
    }
    return render(request, 'store/store.html', context)