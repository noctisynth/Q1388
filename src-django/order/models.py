from django.db import models
from account.models import UserAccount
from product.models import Product


# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ("未支付", "未支付"),
        ("已支付", "已支付"),
        ("传输中", "传输中"),
        ("已完成", "传输中"),
        ("已取消", "已取消"),
    )
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name="用户")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="未支付",
        verbose_name="订单状态",
    )
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="总价格"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="日期")
    address = models.CharField(max_length=200, verbose_name="地址")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="订单")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="产品")
    quantity = models.IntegerField(verbose_name="数量")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="价格")

    class Meta:
        verbose_name = "订单内容"
        verbose_name_plural = "订单内容"
