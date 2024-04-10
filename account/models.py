from django.db import models

# Create your models here.
class UserAccount(models.Model):
    username = models.CharField(max_length=30,verbose_name="用户名")
    password = models.CharField(max_length=50,verbose_name="密码")
    email = models.EmailField(max_length=254,verbose_name="邮件")
    avatar = models.CharField(max_length=254,verbose_name="头像")
    addresses = models.CharField(max_length=2000,verbose_name="地址")