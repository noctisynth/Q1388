from django.urls import path
from . import views

urlpatterns = [
    path("add", views.add),
    path("login", views.login),
    path("update", views.update),
    path("profile", views.profile),
    path("logout", views.logout),
    path("del_address", views.del_address),
    path("avatar", views.avatar),
]
