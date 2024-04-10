from django.http import HttpRequest, JsonResponse
from account.models import UserAccount
from product.models import Product
from product.views import product2dict
from .models import CartItem
import json
from django.views.decorators.csrf import csrf_exempt


def cart_item2dict(ci: CartItem):
    product = product2dict(ci.product)
    return {"product": product, "quantity": ci.quantity, "price": ci.subtotal}


# Create your views here.
@csrf_exempt
def add(request: HttpRequest):
    """
    {
        "product_id":3,
        "quantity":1
    }
    """
    if request.method == "POST":
        ua_session = request.session.get("uname")
        if ua_session:
            try:
                data: dict = json.loads(request.body.decode())
            except:
                return JsonResponse(
                    {"status": 401, "message": "数据格式错误，请使用json"}
                )

            product_id = data.get("product_id", -1)
            quantity = data.get("quantity", 0)

            if product_id == -1:
                return JsonResponse({"status": 400, "message": "商品ID错误"})

            ua = UserAccount.objects.get(username=ua_session)
            product = Product.objects.get(id=product_id)

            try:
                cart_item = CartItem.objects.get(user=ua, product=product)
                cart_item.quantity += quantity
                if cart_item.quantity < 0:
                    cart_item.quantity = 0
                    ## 貌似有点不合理，不打算解决
                cart_item.save()

            except:
                cart_item = CartItem()
                cart_item.user = ua
                cart_item.product = product
                cart_item.quantity = quantity
                cart_item.save()
            return JsonResponse({"status": 200, "message": "添加成功"})
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})

    else:
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})


@csrf_exempt
def remove(request: HttpRequest):
    """
    {
        "product_id":3,
        "number":1
    }
    -1 全删
    """
    if request.method == "POST":
        ua_session = request.session.get("uname")
        if ua_session:
            try:
                data: dict = json.loads(request.body.decode())
            except:
                return JsonResponse(
                    {"status": 401, "message": "数据格式错误，请使用json"}
                )

            product_id = data.get("product_id", -1)
            number = data.get("number", 0)

            if product_id == -1:
                return JsonResponse({"status": 400, "message": "商品ID错误"})

            ua = UserAccount.objects.get(username=ua_session)
            try:
                product = Product.objects.get(id=product_id)
            except:
                return JsonResponse(
                    {"status": 400, "message": "该商品并不在您的购物车"}
                )

            cart_item = CartItem.objects.get(user=ua, product=product)

            if cart_item:
                if number == -1:
                    cart_item.delete()
                else:
                    cart_item.quantity += -number
                    cart_item.save()
                return JsonResponse({"status": 200, "message": "商品移除成功"})
            else:
                return JsonResponse(
                    {"status": 400, "message": "该商品并不在您的购物车"}
                )

        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})

    else:
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})


@csrf_exempt
def all(request: HttpRequest):
    ua_session = request.session.get("uname")
    if ua_session:
        ua = UserAccount.objects.get(username=ua_session)
        cart_items = CartItem.objects.filter(user=ua)
        total_price = sum(cart_item.subtotal for cart_item in cart_items)
        cart_items_list = []
        for c in cart_items:
            cart_items_list.append(cart_item2dict(c))
        return JsonResponse(
            {"status": 200, "cart_items": cart_items_list, "total_price": total_price}
        )

    else:
        return JsonResponse({"status": 403, "message": "用户未登录"})
