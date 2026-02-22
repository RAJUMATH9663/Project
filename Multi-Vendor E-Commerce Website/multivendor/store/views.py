from django.shortcuts import render, redirect
from .models import Product, Cart, Order
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def home(request):
    product_list = Product.objects.all().order_by('id')
    paginator = Paginator(product_list, 12) # Show 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    return render(request, 'home.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    Cart.objects.create(user=request.user, product=product)
    return redirect('cart')


@login_required
def cart_view(request):
    cart_list = Cart.objects.filter(user=request.user).order_by('id')
    paginator = Paginator(cart_list, 10) # 10 items per page
    page_number = request.GET.get('page')
    cart_items = paginator.get_page(page_number)
    return render(request, 'cart.html', {'cart_items': cart_items})


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity
        )
    cart_items.delete()
    return redirect('orders')


@login_required
def orders(request):
    # order by id descending to show newest first instead of ordered_at in case it doesn't exist
    order_list = Order.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(order_list, 10)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    return render(request, 'orders.html', {'orders': orders})