from django.db import models


# Create your models here.
# name, price, comment, quantity, detail, spec_param, pictures, category
# INSERT INTO product_product values("123",20,10,"","","","","","")
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="商品名称", unique=True)
    price = models.IntegerField(verbose_name="价格")
    quantity = models.IntegerField(default=0, verbose_name="库存数量")
    spec_param = models.CharField(max_length=300, verbose_name="规格参数")
    category = models.CharField(max_length=300, verbose_name="种类")
    comment = models.CharField(max_length=500, verbose_name="用户评价")
    detail = models.CharField(max_length=1000, verbose_name="详细描述")
    pictures = models.CharField(max_length=500)
