import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created

from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Order
from .forms import OrderForm
from cart.cart import Cart  # Assuming you have a Cart class to handle cart operations
from django.contrib.auth.decorators import login_required


@login_required
def order_create(request):
    if request.method == 'POST':
        # Initialize the form with POST data
        form = OrderForm(request.POST)

        # Validate the form
        if form.is_valid():
            # Create an Order instance but do not save to the database yet
            order = form.save(commit=False)

            # Assign the current user to the order
            order.user = request.user

            # Calculate the total amount from the cart
            cart = Cart(request)
            total_amount = sum(item['total_price'] for item in cart)

            # Set the total amount for the order
            order.total = total_amount

            # Save the order to the database
            order.save()

            # Clear the cart after saving the order
            cart.clear()

            # Redirect to the payment process page
            return redirect(reverse('payment:process'))
    else:
        # If the request method is GET, display an empty form
        form = OrderForm()

    # Render the order creation form template
    return render(request, 'orders/order_create.html', {'form': form})

def order_create(request):
    # Your code for order creation
    return render(request, 'orders/order_create.html')

def process_order(request):
    # Your code for order processing
    return HttpResponse("Order processed")


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form},
    )


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request, 'admin/orders/order/detail.html', {'order': order}
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))],
    )
    return response
