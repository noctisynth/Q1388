from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout),
    path("detail/<int:order_id>", views.detail),
    path("cancel/<int:order_id>", views.cancel),
    path("all", views.all),
    path("pay/<int:order_id>", views.pay),
]
