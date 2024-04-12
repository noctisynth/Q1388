from django.urls import path
from . import views

urlpatterns = [
    path("add", views.add),
    path("login", views.login),
    path("update", views.update),
    path("profile", views.profile),
]
