from django.shortcuts import render, get_object_or_404
from .models import Product, Variations
from category.models import Category
from carts.models import Cart_item
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.


def store(request, category_slug=None):
    categories = None
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        product = get_object_or_404(Product, slug=product_slug)
        in_cart = Cart_item.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        var_col = Variations.objects.filter(product=product, variation_category='color')
        var_size = Variations.objects.filter(product=product, variation_category='size')
    except Exception as e:
        raise e
    context = {
        'product': product,
        'in_cart': in_cart,
    }
    if var_col:
        context['var_col'] = var_col
    if var_size:
        context['var_size'] = var_size
    return render(request, 'store/product-detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        product_count = 0
        if keyword:
            products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword)).order_by('-created')
            product_count = products.count()
        else:
            products = []
    context = {
        'products':products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
