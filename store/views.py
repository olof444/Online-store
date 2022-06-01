from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Variations, ReviewRating
from category.models import Category
from carts.models import Cart_item
from orders.models import OrderProduct
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages

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
        cat_name = Category.objects.get(slug=category_slug)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        cat_name = None
    context = {
        'products': paged_products,
        'product_count': product_count,
        'cat_name': cat_name,
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

    # Get reviews
    try:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
        context['reviews'] = reviews
        is_purchased = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()
        context['is_purchased'] = is_purchased
    except:
        pass

    # Check if the user purchased the product



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

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated!')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submited!')
                return redirect(url)
