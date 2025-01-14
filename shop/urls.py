# urls.py
from django.urls import path
from .views import (
    product_list,
    product_list_by_category,
    cart_view,
    add_to_cart,
    update_cart,
    remove_from_cart,
    category_list,
    order_create,
    order_success,
    process_payment,
    mpesa_callback,
    paypal_callback,
)

urlpatterns = [
    # Product URLs    path('shop/', product_list_view, name='product_list'),  # Ensure this line exists
    path('', product_list, name='shop'),
    path('products/category/<int:category_id>/', product_list_by_category, name='product_list_by_category'),

    # Category URLs
    path('categories/', category_list, name='category_list'),

    # Cart URLs
    path('cart/', cart_view, name='cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),

    # Order URLs
    path('order/create/<int:product_id>/', order_create, name='order_create'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),

    # Payment URLs
    path('payment/process/<int:order_id>/', process_payment, name='process_payment'),

    # Callback URLs
    path('payment/mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('payment/paypal/callback/', paypal_callback, name='paypal_callback'),
]
