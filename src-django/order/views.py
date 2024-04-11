from django.http import HttpRequest, JsonResponse
from .models import Order, OrderItem
from account.models import UserAccount
from shopping_cart.models import Cart, CartItem
from product.views import product2dict

# Create your views here.


def order2dict(order: Order):
    order_items = []
    for o in order.orderitem_set.all():
        order_items.append(
            {
                "product": product2dict(o.product),
                "quantity": o.quantity,
                "price": o.price,
            }
        )

    return {
        "id": order.id,
        "status": order.status,
        "total_price": order.total_price,
        "date": order.date,
        "order_items": order_items,
    }


def checkout(request: HttpRequest):
    ua_session = request.session.get("uname")

    if ua_session:
        try:
            ua = UserAccount.objects.get(username=ua_session)

            order = Order()
            try:
                cart = Cart.objects.get(user=ua)
                if len(cart.cartitem_set.all()) == 0:
                    raise ("is empty")

                order.total_price = 0
                for cart_item in cart.cartitem_set.all():
                    order.total_price += cart_item.subtotal * cart_item.quantity
                order.user = ua
                order.save()

                for cart_item in cart.cartitem_set.all():
                    order_item = OrderItem()
                    order_item.order = order
                    order_item.product = cart_item.product
                    order_item.quantity = cart_item.quantity
                    order_item.price = cart_item.subtotal
                    order_item.save()
                    cart_item.delete()

                return JsonResponse({"status": 200, "message": "订单创建成功"})
            except Exception as e:
                print(e)
                return JsonResponse({"status": 400, "message": "您的购物车空空如也"})

        except:
            return JsonResponse({"status": 400, "message": "订单不存在"})
    else:
        return JsonResponse({"status": 403, "message": "用户未登录"})


def detail(request: HttpRequest, order_id):
    ua_session = request.session.get("uname")

    if ua_session:
        try:
            ua = UserAccount.objects.get(username=ua_session)

            order = Order.objects.get(id=order_id, user=ua)

            return JsonResponse({"status": 200, "order": order2dict(order)})

        except:
            return JsonResponse({"status": 400, "message": "订单不存在"})
    else:
        return JsonResponse({"status": 403, "message": "用户未登录"})


def cancel(request: HttpRequest, order_id):
    ua_session = request.session.get("uname")

    if ua_session:
        try:
            ua = UserAccount.objects.get(username=ua_session)

            order = Order.objects.get(id=order_id, user=ua)
            order.delete()

            return JsonResponse({"status": 200, "message": "订单删除成功"})

        except:
            return JsonResponse({"status": 400, "message": "订单不存在"})
    else:
        return JsonResponse({"status": 403, "message": "用户未登录"})


def all(request: HttpRequest):
    ua_session = request.session.get("uname")

    if ua_session:
        try:
            ua = UserAccount.objects.get(username=ua_session)

            orders = Order.objects.filter(user=ua)
            orders_list = []
            for o in orders:
                orders_list.append(order2dict(o))

            return JsonResponse({"status": 200, "orders": orders_list})

        except:
            return JsonResponse({"status": 400, "message": "订单不存在"})
    else:
        return JsonResponse({"status": 403, "message": "用户未登录"})
