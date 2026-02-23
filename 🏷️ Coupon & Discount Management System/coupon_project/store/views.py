from django.shortcuts import render
from .models import Product, Coupon
from django.utils import timezone

def home(request):
    products = Product.objects.all()
    total = 0
    discount_amount = 0
    final_price = 0
    message = ""

    if request.method == "POST":
        code = request.POST.get("coupon")
        try:
            coupon = Coupon.objects.get(code=code)

            if coupon.expiry >= timezone.now().date():
                total = sum(p.price for p in products)
                discount_amount = total * (coupon.discount / 100)
                final_price = total - discount_amount
                message = "Coupon Applied Successfully!"
            else:
                message = "Coupon Expired!"
        except:
            message = "Invalid Coupon Code!"

    return render(request, 'home.html', {
        'products': products,
        'total': total,
        'discount': discount_amount,
        'final': final_price,
        'message': message
    })