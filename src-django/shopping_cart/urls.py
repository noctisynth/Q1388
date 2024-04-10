from django.urls import path
from . import views

urlpatterns = [
    path("add", views.add),
    path("del", views.remove),
    path("all", views.all),
]
