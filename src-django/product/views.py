from django.http import HttpRequest, JsonResponse
from .models import Product
import json
from django.views.decorators.csrf import csrf_exempt


def product2dict(p: Product):
    return {
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "quantity": p.quantity,
        "spec_param": p.spec_param,
        "categories": p.get_categories(),
        "comment": p.comment,
        "detail": p.detail,
        "pictures": p.pictures,
    }


@csrf_exempt
def all(request: HttpRequest):
    products = Product.objects.all()
    products_list = []
    for p in products:
        products_list.append(product2dict(p))
    return JsonResponse({"status": 200, "products": products_list})


@csrf_exempt
def search(request: HttpRequest, some):
    if request.method == "POST":
        try:
            data: dict = json.loads(request.body.decode())
            description_list = data["description_list"]

            if some == "keyword":
                products = Product.objects.all()
                products_list = []

                for p in products:
                    for d in description_list:
                        if d in p.name or d in p.comment or d in p.detail:
                            products_list.append(product2dict(p))
                            break

                return JsonResponse({"status": 200, "products": products_list})

            elif some == "category":
                products = Product.objects.all()
                products_list = []

                for p in products:
                    for d in description_list:
                        if d in p.get_categories():
                            products_list.append(product2dict(p))
                            break
                return JsonResponse({"status": 200, "products": products_list})
            else:
                return JsonResponse({"status": 400, "message": "请求路径错误"})
        except:
            return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})

    else:
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
