from django.urls import path
from . import views

urlpatterns = [
    path("all", views.all),
    path("search_keyword", views.search_keyword),
    path("search_category", views.search_category),
    path("report", views.report),
    path("detail", views.detail),
    path("categories", views.categories),
    path("recommend", views.recommend),
]
