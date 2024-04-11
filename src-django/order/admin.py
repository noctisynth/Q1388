from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status", "total_price", "address", "date")


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
