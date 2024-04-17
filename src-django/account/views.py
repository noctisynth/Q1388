from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.session import verify_session
from .models import Session, UserAccount, UserAddress
import json


@csrf_exempt
def add(request: HttpRequest):
    """
    {
        "username":"bash",
        "password":"123456",// md5
        "email":"admin@site.com"
    } //头像使用默认，地址以后添加, 为空逻辑判断交给前端
    """
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})

    username: str = data.get("username", "")
    password: str = data.get("password", "")
    email: str = data.get("email", "")

    if not all([username, password, email]):
        return JsonResponse({"status": 402, "message": "参数错误"})

    else:
        if UserAccount.objects.filter(username=username).exists():
            return JsonResponse({"status": 400, "message": "用户已存在"})
        else:
            ua = UserAccount()
            ua.username = username
            ua.password = make_password(password)
            ua.email = email
            ua.save()
            return JsonResponse({"status": 200, "message": "用户创建成功"})


@csrf_exempt
def login(request: HttpRequest):
    """
    {
        "username":"bash",
        "password":"e10adc3949ba59abbe56e057f20f883e"// md5,
        "token":"123123123123"
    }
    """
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
            return JsonResponse({"status": 201, "message": "用户已登录"})
        else:
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"status": 402, "message": "参数错误"})
            else:
                if UserAccount.objects.filter(username=username).exists():
                    ua = UserAccount.objects.get(username=username)
                    if check_password(password, ua.password):
                        session = Session.objects.filter(
                            account=ua
                        ).first() or Session.objects.create(
                            session_key=make_password(request.session.session_key),
                            account=ua,
                        )
                        return JsonResponse(
                            {
                                "status": 200,
                                "messag": "登陆成功",
                                "token": session.session_key,
                            }
                        )
                    else:
                        return JsonResponse({"status": 403, "message": "密码错误"})
    else:
        return JsonResponse(
            {"status": 400, "message": "未设置token,若是登录请设置为123"}
        )


@csrf_exempt
def update(request: HttpRequest):
    """
    {
        "password":"e10adc3949ba59abbe56e057f20f883e",
        "email":"123@admin.com",
        "avator":"new.jpg",
        "addresses":["213","123"],
        "default_address":"123/123/afd",
        "token":"123123123123"
    }
    不需要更新的直接留空
    """
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})

    token = data.get("token")  # type: ignore
    password: str = data.get("password", "")
    email: str = data.get("email", "")
    default_address: str = data.get("default_address", "")
    addresses: str = data.get("addresses", "")

    if token:
        ua = verify_session(token)
        if not ua:
            return JsonResponse({"status": 403, "message": "用户未登录"})

        else:
            if password:
                ua.password = make_password(password)
            if email:
                ua.email = email
            if default_address:
                ua.default_address = default_address
            if addresses:
                d = ua.addresses
                if addresses not in d:
                    user_adress = UserAddress()
                    user_adress.user = ua
                    user_adress.location = addresses
                    if len(ua.default_address) == 0:
                        ua.default_address = addresses
                    user_adress.save()
            ua.save()

            return JsonResponse({"status": 200, "message": "更新成功"})
    else:
        return JsonResponse({"status": 400, "message": "没有设置token"})


@csrf_exempt
def profile(request: HttpRequest):
    """
    {
        "token":"123123123123"
    }
    """
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})

    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})

    token = data.get("token")  # type: ignore
    if token:
        ua = verify_session(token)
        if ua:

            data = {
                "status": 200,
                "username": ua.username,
                "email": ua.email,
                "avatar": ua.avatar.url,
                "default_address": ua.default_address,
                "addresses": ua.addresses,
            }

            return JsonResponse(data)
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "未设置token"})


@csrf_exempt
def logout(request: HttpRequest):
    """
    {
        "token":"123123123123"
    }
    """
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    token = data.get("token")  # type: ignore

    if token:
        ua = verify_session(token)
        if ua:
            session = Session.objects.filter(account=ua)
            session.delete()

    return JsonResponse({"status": 200, "message": "退出成功"})


@csrf_exempt
def del_address(request: HttpRequest):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})
    try:
        data: dict = json.loads(request.body.decode())
        address: str = data.get("address", "")
    except:
        return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})
    token = data.get("token")  # type: ignore
    if token:
        ua = verify_session(token)
        if ua:
            try:
                a = UserAddress.objects.filter(user=ua, location=address)
                for i in a:
                    i.delete()
                return JsonResponse({"status": 200, "message": "删除成功"})
            except:
                return JsonResponse({"status": 404, "message": "地址未找到"})
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})
    else:
        return JsonResponse({"status": 400, "message": "未设置token"})


@csrf_exempt
def avatar(request: HttpRequest):
    if request.method == "POST" and request.FILES["image"]:
        token = request.POST.get("token", "")
        if token:
            ua = verify_session(token)
            if ua:
                image_file = request.FILES["image"]
                ua.avatar = image_file  # type: ignore
                ua.save()

            else:
                return JsonResponse({"status": 403, "message": "用户未登录"})
        else:
            return JsonResponse({"status": 400, "message": "未设置token"})

        return JsonResponse({"success": 200})
    return JsonResponse({"success": 40}, status=400)
