from django.urls import path

from . import views

# shop/urls.py
from django.urls import path
from .views import submit_payment, payment_success



app_name = 'shop_payment'

urlpatterns = [

    path('submit-payment/', submit_payment, name='submit_payment'),
    path('payment-success/', payment_success, name='payment_success'),
    path('', views.product_list, name='product_list'),
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category',
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail',
    ),
]
