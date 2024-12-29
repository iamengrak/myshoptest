from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from .models import Category, Product

# shop/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import PaymentForm
from .models import Payment

@login_required
def submit_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.amount = 100.00  # Replace with the actual amount
            payment.save()
            # Send initial email to user
            send_mail(
                'Payment Verification Pending',
                'Your payment verification is pending. It will be verified within one hour.',
                'admin@cspace.com',
                [request.user.email],
                fail_silently=False,
            )
            return redirect('payment_success')
    else:
        form = PaymentForm()
    return render(request, 'submit_payment.html', {'form': form})

def payment_success(request):
    return render(request, 'payment_success.html')


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products,
        },
    )


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    return render(
        request,
        'shop/product/detail.html',
        {'product': product, 'cart_product_form': cart_product_form},
    )


