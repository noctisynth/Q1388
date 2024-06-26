from django.db import models


# Create your models here.
class UserAccount(models.Model):
    username = models.CharField(
        max_length=30, verbose_name="用户名", unique=True, null=False
    )
    password = models.CharField(max_length=200, verbose_name="密码", null=False)
    email = models.EmailField(max_length=254, verbose_name="邮件", default="")
    avatar = models.ImageField(
        upload_to="avatar",
        verbose_name="头像",
        default="avatar/v2-d52893c607cbd58ff48e2e08dcd72b2a_r.jpg",
        null=True,
    )
    default_address = models.CharField(
        max_length=200, verbose_name="默认地址", default=""
    )

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username

    @property
    def addresses(self):
        address_list = []
        for a in self.useraddress_set.all():  # type: ignore
            address_list.append(a.location)
        return address_list


class Session(models.Model):
    session_key = models.CharField(
        max_length=39, verbose_name="会话密钥", null=False, unique=True
    )
    account = models.ForeignKey(
        "UserAccount", on_delete=models.CASCADE, related_name="session", null=False
    )


class UserAddress(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, verbose_name="用户")
    location = models.CharField(max_length=100, verbose_name="地址")

    class Meta:
        verbose_name = "用户地址"
        verbose_name_plural = "用户地址"

    def __str__(self):
        return self.location
