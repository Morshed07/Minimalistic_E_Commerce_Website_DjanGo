from django.db import models
from django.conf import settings
from product.models import Product
from cart.models import Coupon

# Create your models here.
class OrderItems(models.Model):
    product = models.ForeignKey(Product, related_name='ordered', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveBigIntegerField()

    class Meta:
        ordering = ['-id']

    def __str__(self) -> str:
        return f"{self.product.title} x {self.quantity}"
    
class Order(models.Model):
    STATUS = ('Recieved', 'On the Way', 'Delivered')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    order_items = models.ManyToManyField(OrderItems)
    coupon = models.ForeignKey(Coupon,null=True,blank=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    address =  models.TextField()
    total = models.DecimalField(max_digits=8,decimal_places=2)
    paid = models.BooleanField(default=True)
    transaction_id = models.UUIDField()
    status = models.CharField(max_length=15, choices=list(zip(STATUS, STATUS)))
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name