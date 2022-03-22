from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variations
from .models import Cart, Cart_item
from django.http import HttpResponse

# Create your views here.

def cart(request, total=0, quantity=0, cart_item=None):
    context = {}
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = Cart_item.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
        context = {
            'total': total,
            'quantity': quantity,
            'tax': tax,
            'cart_items': cart_items,
            'grand_total': grand_total,
        }
    except:
        context = {'cart_items': False}
    return render(request, 'store/cart.html', context)

def _cart_id(request):
    cart_session = request.session.session_key
    if not cart_session:
        cart_session = request.session.create()
    return cart_session

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variations.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the session id
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    is_cart_item_exists = Cart_item.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = Cart_item.objects.filter(product=product, cart=cart)
        # Existing variations -> database
        # Current variations -> product_variation
        # item_id -> database
        ex_var_list = []
        id = []
        for item in cart_item:
            variation_color = list(item.variations.colors())
#            variation_size = item.variations.sizes()
            variation_color.extend(list(item.variations.sizes()))
            ex_var_list.append(variation_color)
            id.append(item.id)
        print('variation_color: ', variation_color)
        print('product_variation: ', product_variation )
        print('ex_var_list: ', ex_var_list)

        if product_variation in ex_var_list:
            # Increase the cart item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = Cart_item.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            # Create a new cart item
            item = Cart_item.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
                print(*product_variation)
            item.save()
    else:
        cart_item = Cart_item.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()
    return redirect('carts:cart')

def increase(request, cart_item_id):
    cart_item = Cart_item.objects.get(id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('carts:cart')

def remove_cart(request, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = Cart_item.objects.get(id=cart_item_id, cart=cart)
    try:
        type = request.GET['type']
    except:
        type = 'NOPE'
    if type == 'delete':
        cart_item.delete()
    else:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('carts:cart')

