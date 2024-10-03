# urls.py
from django.urls import path
from .views import (
    add_to_cart,
    cart_view,
    category_list,
    order_create,
    product_list,
    process_payment,
    order_success,
    mpesa_callback,
    paypal_callback,
    remove_from_cart,
    update_cart,
)

urlpatterns = [

    path('', product_list, name='shop'),
    path('categories/', category_list, name='category_list'),
    path('order/create/<int:product_id>/', order_create, name='order_create'),
    path('payment/<int:order_id>/', process_payment, name='payment'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('paypal/callback/', paypal_callback, name='paypal_callback'),

    # Cart views
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]
