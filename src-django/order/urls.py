from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout),
    path("detail/<int:order_id>", views.detail),
    path("cancel", views.cancel),
    path("all", views.all),
    path("pay", views.pay),
    path("modify_address", views.modify_address),
]
