from enum import verify
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Session, UserAccount, UserAddress

import json


@csrf_exempt
def add(request: HttpRequest):
    """
    {
        "username":"bash",
        "password":"e10adc3949ba59abbe56e057f20f883e",// md5
        "email":"admin@site.com"
    } //头像使用默认，地址以后添加, 为空逻辑判断交给前端
    """
    if request.method == "POST":
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
                ua.avatar = "default_avatar.jpg"
                ua.save()
                return JsonResponse({"status": 200, "message": "用户创建成功"})
    else:
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})


@csrf_exempt
def login(request: HttpRequest):
    """
    {
        "username":"bash",
        "password":"e10adc3949ba59abbe56e057f20f883e"// md5
    }
    """
    if request.method == "POST":
        session_key = request.session.get("token")
        session = Session.objects.filter(session_key=session_key)
        if session.count() != 0:
            return JsonResponse({"status": 201, "message": "用户已登录"})

        try:
            data: dict = json.loads(request.body.decode())

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
                        request.session["token"] = session.session_key
                        request.session.save()
                        return JsonResponse({"status": 200, "messag": "登陆成功"})
                    else:
                        return JsonResponse({"status": 403, "message": "密码错误"})

                else:
                    return JsonResponse({"status": 404, "message": "用户不存在"})

        except Exception as e:
            print(e)
            return JsonResponse({"status": 401, "message": "数据格式错误，请使用json"})

    else:
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})


@csrf_exempt
def update(request: HttpRequest):
    """
    {
        "password":"e10adc3949ba59abbe56e057f20f883e",
        "email":"123@admin.com",
        "avator":"new.jpg",
        "addresses":["213","123"],
        "default_address":"123/123/afd"
    }
    不需要更新的直接留空
    """
    if request.method == "POST":

        session_key = request.session.get("token")
        session = Session.objects.filter(session_key=session_key)
        if session.count() != 0:
            s = session[0]
            ua = s.account
            try:
                data = json.loads(request.body.decode())
                # password, email, avator, addresses
                password: str = data.get("password", "")
                email: str = data.get("email", "")
                avatar: str = data.get("avatar", "")
                default_address: str = data.get("default_address", "")
                addresses: list = data.get("addresses", [])

                if password:
                    ua.password = make_password(password)
                if email:
                    ua.email = email
                if avatar:
                    ua.avatar = avatar
                if default_address:
                    ua.default_address = default_address

                if addresses:
                    d = ua.addresses
                    for a in addresses:
                        if a not in d:
                            user_adress = UserAddress()
                            user_adress.user = ua
                            user_adress.location = a
                            user_adress.save()
                ua.save()

                return JsonResponse({"status": 200, "message": "更新成功"})
            except:
                return JsonResponse(
                    {"status": 401, "message": "数据格式错误，请使用json"}
                )
        else:
            return JsonResponse({"status": 403, "message": "用户未登录"})

    else:
        return JsonResponse({"status": 405, "message": "请使用POST调用接口"})


@csrf_exempt
def profile(request: HttpRequest):
    session_key = request.session.get("token")
    session = Session.objects.filter(session_key=session_key)
    if session.count() != 0:
        s = session[0]
        ua = s.account
        data = {
            "status": 200,
            "username": ua.username,
            "email": ua.email,
            "avatar": ua.avatar,
            "default_address": ua.default_address,
            "addresses": ua.addresses,
        }

        return JsonResponse(data)

    else:
        return JsonResponse({"status": 403, "message": "用户未登录"})


@csrf_exempt
def logout(request: HttpRequest):
    session_key = request.session.get("token")
    session = Session.objects.filter(session_key=session_key)
    if session.count() != 0:
        for s in session:
            s.delete()

    return JsonResponse({"status": 200, "message": "退出成功"})
