from types import NoneType
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from .models import Category, Product
from order.models import Order
from account.models import UserAccount

import json
from django.views.decorators.csrf import csrf_exempt


def product2dict(p: Product):
    return {
        "id": p.id,  # type: ignore
        "name": p.name,
        "price": p.price,
        "quantity": p.quantity,
        "spec_param": p.get_spec(),
        "category": p.category.name,  # type: ignore
        "comment": p.comment,
        "detail": p.detail,
        "pictures": p.pictures,
    }


def all(request: HttpRequest):
    products = Product.objects.all()
    products_list = []
    for p in products:
        products_list.append(product2dict(p))
    return JsonResponse({"status": 200, "products": products_list})


@csrf_exempt
def search_keyword(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
        keyword = data["keyword"]
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    products = Product.objects.all()
    products_list = []

    for p in products:
        if keyword in p.name or keyword in p.comment or keyword in p.detail:
            products_list.append(product2dict(p))

    return JsonResponse({"status": 200, "products": products_list})


@csrf_exempt
def search_category(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
        category = data["category"]
    except json.JSONDecodeError:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    except:
        return JsonResponse({"status": 500, "message": "存在没有分类的商品"})

    products = Product.objects.all()
    products_list = []
    for p in products:
        if category in p.category.name or category in p.category.description:  # type: ignore
            products_list.append(product2dict(p))

    return JsonResponse({"status": 200, "products": products_list})


def report(request: HttpRequest):
    data = {
        "useraccount_count": UserAccount.objects.count(),
        "product_count": Product.objects.count(),
        "order_count": Order.objects.count(),
    }
    return render(request, "report.html", data)


@csrf_exempt
def detail(request: HttpRequest):
    """
    {
        "product_id": 1
    }
    """
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
        product_id = data.get("product_id")
        products = Product.objects.filter(id=product_id)
        if products.count() > 0:
            return JsonResponse({"status": 200, "product": product2dict(products[0])})
        else:
            return JsonResponse({"status": 404, "message": "商品不存在"})
    except Exception as e:
        print(e)
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})


@csrf_exempt
def categories(request: HttpRequest):
    categories = [c.name for c in Category.objects.all()]
    return JsonResponse({"status": 200, "categories": categories})


@csrf_exempt
def recommend(request: HttpRequest):
    products = [product2dict(product) for product in Product.objects.order_by("?")[:30]]
    return JsonResponse({"status": 200, "products": products})
