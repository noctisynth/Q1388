from django.contrib import admin

# Register your models here.
from .models import UserAccount, UserAddress


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "default_address")


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "location")


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
