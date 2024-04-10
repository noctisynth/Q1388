from django.db import models
from account.models import UserAccount
from product.models import Product


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(UserAccount, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity
