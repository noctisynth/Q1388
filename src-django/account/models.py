from django.db import models

# Create your models here.
class UserAccount(models.Model):
    username = models.CharField(max_length=30,verbose_name="用户名",unique=True,null=False)
    password = models.CharField(max_length=50,verbose_name="密码",null=False)
    email = models.EmailField(max_length=254,verbose_name="邮件", default="")
    avatar = models.CharField(max_length=254,verbose_name="头像", default="")
    addresses = models.CharField(max_length=2000,verbose_name="地址", default="")
    default_address = models.CharField(max_length=200, verbose_name="默认地址", default="")