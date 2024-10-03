import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Category, Order, Payment, Product
from .forms import OrderForm

def product_list(request):
    # Fetch all products
    products = Product.objects.all()
    return render(request, 'shop/products.html', {'products': products})

# Cart views
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        cart_items.append({'product': product, 'quantity': quantity})
        total_price += product.price * quantity

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'shop/cart.html', context)

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart_view')

def update_cart(request, product_id):
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
    cart = request.session.get('cart', {})
    cart.pop(product_id, None)
    request.session['cart'] = cart
    return redirect('cart_view')

def category_list(request):
    # Fetch all categories
    categories = Category.objects.all()
    return render(request, 'shop/categories.html', {'categories': categories})

def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('order_success')  # redirect to a success page
    else:
        form = OrderForm()
    
    return render(request, 'shop/order_create.html', {'form': form, 'product': product})
    
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    context = {
        'order': order,
    }
    
    return render(request, 'shop/order_success.html', context)

def get_mpesa_access_token():
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    return response.json()['access_token']

def get_paypal_access_token():
    api_url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
    headers = {
        "Accept": "application/json",
        "Accept-Language": "en_US"
    }
    response = requests.post(api_url, headers=headers, auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET), data={"grant_type": "client_credentials"})
    return response.json()['access_token']


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

def product_list(request, category_id=None):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('order_success')  # redirect to a success page
    else:
        form = OrderForm()
    
    return render(request, 'shop/order_create.html', {'form': form, 'product': product})


def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        amount = order.product.price * order.quantity

        if payment_method == 'Mpesa':
            # Call M-Pesa Daraja API
            mpesa_response = process_mpesa_payment(amount, order)
            if mpesa_response['status'] == 'success':
                # Save payment details
                Payment.objects.create(
                    order=order,
                    amount=amount,
                    payment_method='M-Pesa',
                    transaction_id=mpesa_response['transaction_id'],
                    is_successful=True
                )
                return redirect('order_success', order_id=order.id)

        elif payment_method == 'PayPal':
            # Call PayPal API (handle PayPal payment here)
            paypal_response = process_paypal_payment(amount, order)
            if paypal_response['status'] == 'success':
                # Save payment details
                Payment.objects.create(
                    order=order,
                    amount=amount,
                    payment_method='PayPal',
                    transaction_id=paypal_response['transaction_id'],
                    is_successful=True
                )
                return redirect('order_success', order_id=order.id)

    return render(request, 'shop/payment.html', {'order': order})

def process_mpesa_payment(amount, order):
    # Example M-Pesa Daraja API integration
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
        "CallBackURL": "https://example.com/callback",  # Update with your callback URL
        "AccountReference": f"Order {order.id}",
        "TransactionDesc": f"Payment for Order {order.id}"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def process_paypal_payment(amount, order):
    # Example PayPal API integration
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
            "return": "https://example.com/success",  # Update with your success URL
            "cancel": "https://example.com/cancel"
        }
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()



def get_mpesa_timestamp():
    from datetime import datetime
    return datetime.now().strftime('%Y%m%d%H%M%S')

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        # Assuming M-Pesa sends a JSON body
        data = json.loads(request.body)
        
        # Extract necessary fields
        transaction_id = data.get('transaction_id')
        status = data.get('status')  # e.g., "Success" or "Failed"
        order_id = data.get('order_id')  # Include this in your callback payload
        
        try:
            order = Order.objects.get(id=order_id)
            payment = Payment.objects.get(order=order)

            if status == 'Success':
                payment.is_successful = True
            else:
                payment.is_successful = False

            payment.transaction_id = transaction_id
            payment.save()

            return JsonResponse({'message': 'Payment status updated'}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def paypal_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Extract necessary fields
        transaction_id = data.get('id')  # PayPal's transaction ID
        status = data.get('status')  # e.g., "COMPLETED" or "FAILED"
        order_id = data.get('order_id')  # Include this in your callback payload
        
        try:
            order = Order.objects.get(id=order_id)
            payment = Payment.objects.get(order=order)

            if status == 'COMPLETED':
                payment.is_successful = True
            else:
                payment.is_successful = False

            payment.transaction_id = transaction_id
            payment.save()

            return JsonResponse({'message': 'Payment status updated'}, status=200)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        except Payment.DoesNotExist:
            return JsonResponse({'error': 'Payment not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

