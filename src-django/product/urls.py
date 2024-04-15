from django.urls import path
from . import views

urlpatterns = [
    path("all", views.all),
    path("search/<str:some>", views.search),
    path("report", views.report),
    path("detail", views.detail),
    path("categories", views.categories),
    path("recommend", views.recommend),
]
