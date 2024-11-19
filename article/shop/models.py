from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensuring category names are unique
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    keywords = models.ManyToManyField('Keyword', blank=True, related_name='products')

    def __str__(self):
        return f"{self.name} - {self.price} ({self.stock} in stock)"

    def get_discounted_price(self, discount_rate):
        """Calculate discounted price based on a given discount rate."""
        return self.price * (1 - discount_rate) if 0 <= discount_rate < 1 else self.price

class Keyword(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    target = models.ManyToManyField(Product, blank=True, related_name='keyword_targets')

    def __str__(self):
        return self.name

class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    payment = models.OneToOneField('Payment', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_order')

    def __str__(self):
        return f"Order by {self.customer_name} for {self.quantity} x {self.product.name}"

    def total_price(self):
        """Calculate the total price for the order."""
        return self.product.get_discounted_price(0) * self.quantity  # Assuming no discount for the total price calculation


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='related_payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)  # Using choices for payment methods
    transaction_id = models.CharField(max_length=100, unique=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Order {self.order.id} - Amount: {self.amount} - Successful: {self.is_successful}"
