from ast import Or
from pickletools import read_uint1
from django.http import HttpRequest, JsonResponse
from account.models import UserAccount
from shopping_cart.models import Cart
from product.models import Product
from product.views import product2dict
from utils.session import verify_session
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem

import json


def order2dict(order: Order):
    order_items = []
    for o in order.orderitem_set.all():  # type: ignore
        order_items.append(
            {
                "product": product2dict(o.product),
                "quantity": o.quantity,
                "price": o.price,
            }
        )

    return {
        "id": order.id,  # type: ignore
        "status": order.status,
        "total_price": order.total_price,
        "date": order.date,
        "address": order.address,
        "order_items": order_items,
    }


@csrf_exempt
def checkout(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    token = data.get("token")
    if token:
        ua = verify_session(token)
        if ua:
            order = Order()
            try:
                cart = Cart.objects.get(user=ua)
                if len(cart.cartitem_set.all()) == 0:  # type: ignore
                    raise ("is empty")  # type: ignore

                order.total_price = 0  # type: ignore
                for cart_item in cart.cartitem_set.all():  # type: ignore
                    order.total_price += cart_item.subtotal * cart_item.quantity

                order.address = ua.default_address
                order.user = ua
                order.save()

                for cart_item in cart.cartitem_set.all():  # type: ignore
                    order_item = OrderItem()
                    order_item.order = order
                    order_item.product = cart_item.product
                    order_item.quantity = cart_item.quantity
                    order_item.price = cart_item.subtotal
                    order_item.save()

                    product = Product.objects.get(id=cart_item.product.id)
                    product.quantity -= cart_item.quantity
                    if product.quantity < 0:
                        product.quantity = 0
                    product.save()

                    cart_item.delete()

                return JsonResponse({"status": 200, "message": "订单创建成功"})
            except Exception as e:
                print(e)
                return JsonResponse({"status": 400, "message": "您的购物车空空如也"})
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "未设置token"})


@csrf_exempt
def detail(request: HttpRequest, order_id):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})

    token = data.get("token")
    if token:
        ua = verify_session(token)
        if ua:
            try:
                order = Order.objects.get(id=order_id, user=ua)
                return JsonResponse({"status": 200, "order": order2dict(order)})
            except:
                return JsonResponse({"status": 400, "message": "订单不存在"})
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "未设置token"})


@csrf_exempt
def cancel(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())

    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    token = data.get("token")
    order_id = data.get("order_id")
    if token:
        ua = verify_session(token)
        if ua:
            try:
                order = Order.objects.get(id=order_id, user=ua)
                order.status = "已取消"
                order.save()
                return JsonResponse({"status": 200, "message": "订单删除成功"})
            except:
                return JsonResponse({"status": 400, "message": "订单不存在"})
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "未设置token"})


@csrf_exempt
def all(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    token = data.get("token")
    if token:
        ua = verify_session(token)
        if ua:
            orders = Order.objects.filter(user=ua).order_by("-id")

            orders_list = []
            for o in orders:
                orders_list.append(order2dict(o))

            return JsonResponse({"status": 200, "orders": orders_list})

        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "未设置token"})


@csrf_exempt
def pay(request: HttpRequest):
    """
    // paypal
    {
        "order_id":1,
        "token":"123123"
    }
    """
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    token = data.get("token")
    order_id = data.get("order_id")
    if token:
        ua = verify_session(token)
        if ua:
            try:
                order = Order.objects.get(user=ua, id=order_id)
                order.status = "已支付"
                order.save()
                return JsonResponse({"status": 200, "message": "支付成功"})
            except:
                return JsonResponse({"status": 400, "message": "订单不存在"})
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "未设置token"})


@csrf_exempt
def modify_address(request: HttpRequest):
    """
    {
        "order_id":1,
        "address":"123",
        "token":"by5n4"
    }
    """
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    token = data.get("token")
    order_id = data.get("order_id")
    address = data.get("address", "")
    if token:
        ua = verify_session(token)
        if ua:
            order = Order.objects.get(user=ua, id=order_id)
            order.address = address
            order.save()
            return JsonResponse({"status": 200, "message": "修改地址成功"})
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "token未设置"})
