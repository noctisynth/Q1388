from django.db import models


# Create your models here.
# name, price, comment, quantity, detail, spec_param, pictures, category
# INSERT INTO product_product values("123",20,10,"","","","","","")
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称")
    description = models.TextField(verbose_name="描述")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "产品类别"
        verbose_name_plural = "产品类别"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="商品名称", unique=True)
    price = models.FloatField(verbose_name="价格")
    quantity = models.IntegerField(default=0, verbose_name="库存数量")
    spec_param = models.CharField(max_length=300, verbose_name="规格参数")
    categories = models.ManyToManyField(Category, verbose_name="类别")
    comment = models.CharField(max_length=500, verbose_name="用户评价")
    detail = models.CharField(max_length=1000, verbose_name="详细描述")
    pictures = models.CharField(max_length=500)

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品"

    def __str__(self):
        return self.name

    def get_categories(self):
        categories_list = []
        for c in self.categories.all():
            categories_list.append(c.name)
        return categories_list
