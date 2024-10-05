import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Category, Order, Payment, Product
from .forms import OrderForm


# Product Views
def product_list(request):
    """Fetch and display all products."""
    products = Product.objects.all()
    print(f"Number of products fetched: {products.count()}")
    return render(request, 'shop/products.html', {'products': products})


def product_list_by_category(request, category_id=None):
    """Fetch and display products by category."""
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})


# Cart Views
def cart_view(request):
    """Display items in the shopping cart."""
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items.append({'product': product, 'quantity': quantity})
        total_price += product.price * quantity

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'shop/cart.html', context)


def add_to_cart(request, product_id):
    """Add a product to the cart."""
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')


def update_cart(request, product_id):
    """Update the quantity of a product in the cart."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if quantity > 0:
            cart[product_id] = quantity
        else:
            cart.pop(product_id, None)
        request.session['cart'] = cart
    return redirect('cart_view')


def remove_from_cart(request, product_id):
    """Remove a product from the cart."""
    cart = request.session.get('cart', {})
    cart.pop(product_id, None)
    request.session['cart'] = cart
    return redirect('cart_view')


# Category Views
def category_list(request):
    """Fetch and display all categories."""
    categories = Category.objects.all()
    return render(request, 'shop/categories.html', {'categories': categories})


# Order Views
def order_create(request, product_id):
    """Create a new order for a specific product."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('order_success', order_id=order.id)  # Redirect to the order success page
    else:
        form = OrderForm()

    return render(request, 'shop/order_create.html', {'form': form, 'product': product})


def order_success(request, order_id):
    """Display a success message after order creation."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})


# Payment Views
def process_payment(request, order_id):
    """Process payment for a specific order."""
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = order.product.price * order.quantity

        if payment_method == 'Mpesa':
            mpesa_response = process_mpesa_payment(amount, order)
            return handle_payment_response(mpesa_response, order, amount, 'M-Pesa')

        elif payment_method == 'PayPal':
            paypal_response = process_paypal_payment(amount, order)
            return handle_payment_response(paypal_response, order, amount, 'PayPal')

    return render(request, 'shop/payment.html', {'order': order})


def handle_payment_response(response, order, amount, payment_method):
    """Handle the payment response for both M-Pesa and PayPal."""
    if response.get('status') == 'success':
        Payment.objects.create(
            order=order,
            amount=amount,
            payment_method=payment_method,
            transaction_id=response['transaction_id'],
            is_successful=True
        )
        return redirect('order_success', order_id=order.id)
    else:
        # Log error details for failed payment
        print(f"Payment failed: {response.get('message', 'Unknown error')}")
        return redirect('order_failure', order_id=order.id)  # Redirect to a failure page


# M-Pesa Functions
def get_mpesa_access_token():
    """Retrieve M-Pesa access token."""
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    return response.json().get('access_token')


def process_mpesa_payment(amount, order):
    """Integrate with M-Pesa Daraja API to process payments."""
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {get_mpesa_access_token()}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": settings.MPESA_PASSWORD,
        "Timestamp": get_mpesa_timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": settings.MPESA_PHONE_NUMBER,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": settings.MPESA_PHONE_NUMBER,
        "CallBackURL": settings.MPESA_CALLBACK_URL,  # Update with your callback URL
        "AccountReference": f"Order {order.id}",
        "TransactionDesc": f"Payment for Order {order.id}"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


def get_mpesa_timestamp():
    """Get the current timestamp formatted for M-Pesa."""
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d%H%M%S')


# PayPal Functions
def get_paypal_access_token():
    """Retrieve PayPal access token."""
    api_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    response = requests.post(api_url, headers=headers, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET), data={"grant_type": "client_credentials"})
    return response.json().get('access_token')


def process_paypal_payment(amount, order):
    """Integrate with PayPal API to process payments."""
    api_url = "https://api-m.sandbox.paypal.com/v1/payments/payment"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_paypal_access_token()}"
    }

    payload = {
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "transactions": [{
            "amount": {
                "total": str(amount),
                "currency": "USD"
            },
            "description": f"Payment for Order {order.id}"
        }],
        "redirect_urls": {
            "return": settings.PAYPAL_SUCCESS_URL,  # Update with your success URL
            "cancel": settings.PAYPAL_CANCEL_URL
        }
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


# Callbacks
@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa callback for payment updates."""
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        status = data.get('status')  # e.g., "Success" or "Failed"
        order_id = data.get('order_id')  # Include this in your callback payload

        return update_payment_status(transaction_id, order_id, status)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def paypal_callback(request):
    """Handle PayPal callback for payment updates."""
    if request.method == 'POST':
        data = json.loads(request.body)
        transaction_id = data.get('id')  # PayPal's transaction ID
        status = data.get('status')  # e.g., "COMPLETED" or "FAILED"
        order_id = data.get('order_id')  # Include this in your callback payload

        return update_payment_status(transaction_id, order_id, status)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_payment_status(transaction_id, order_id, status):
    """Update payment status in the database based on the callback."""
    try:
        order = Order.objects.get(id=order_id)
        payment = Payment.objects.get(order=order)

        payment.is_successful = (status == 'Success' or status == 'COMPLETED')
        payment.transaction_id = transaction_id
        payment.save()

        # Here you can handle post-payment logic, e.g., sending confirmation emails.

        return JsonResponse({'status': 'success'})

    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=404)
