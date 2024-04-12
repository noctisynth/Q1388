from django.contrib import admin

from .models import UserAccount, UserAddress


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "default_address")


class UserAddressAdmin(admin.ModelAdmin):
    list_display = ("user", "location")


admin.site.register(UserAccount, UserAccountAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
