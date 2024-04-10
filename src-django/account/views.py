from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from .models import UserAccount
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


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

        if username == "" or password == "" or email == "":
            return JsonResponse({"status": 402, "message": "参数错误"})

        else:
            if UserAccount.objects.filter(username=username).exists():
                return JsonResponse({"status": 400, "message": "用户已存在"})
            else:
                ua = UserAccount()
                ua.username = username
                ua.password = password
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

        ua_session = request.session.get("uname")
        if ua_session:
            return JsonResponse({"status": 201, "message": "用户已登录"})

        try:
            data = json.loads(request.body.decode())
            username: str = data.get("username", "")
            password: str = data.get("password", "")

            if username == "" or password == "":
                return JsonResponse({"status": 402, "message": "参数错误"})
            else:
                if UserAccount.objects.filter(username=username).exists():
                    ua = UserAccount.objects.get(username=username)
                    if ua.password == password:
                        request.session["uname"] = username
                        request.session.save()
                        return JsonResponse({"status": 200, "messag": "登陆成功"})
                    else:
                        return JsonResponse({"status": 403, "message": "密码错误"})

                else:
                    return JsonResponse({"status": 404, "message": "用户不存在"})

        except:
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
        "addresses":"123/123/afd!@#$fawbqer/qwebrqbwerbq/qbwer",
        "default_address":"123/123/afd"
    }
    不需要更新的直接留空
    """
    if request.method == "POST":

        ua_session = request.session.get("uname")

        if ua_session:
            ua = UserAccount.objects.get(username=ua_session)
            try:
                data = json.loads(request.body.decode())
                # password, email, avator, addresses
                password: str = data.get("password", "")
                email: str = data.get("email", "")
                avatar: str = data.get("avatar", "")
                addresses: str = data.get("addresses", "")
                default_address: str = data.get("default_address", "")

                if password:
                    ua.password = password
                if email:
                    ua.email = email
                if avatar:
                    ua.avatar = avatar
                if addresses:
                    ua.addresses = addresses
                if default_address:
                    ua.default_address = default_address

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
    ua_session = request.session.get("uname")

    if ua_session:
        ua = UserAccount.objects.get(username=ua_session)
        data = {
            "status":200,
            "username": ua.username,
            "email": ua.email,
            "avatar": ua.avatar,
            "default_address": ua.default_address,
            "addresses": ua.addresses.split("!@#$"),
        }

        return JsonResponse(data)

    else:
        return JsonResponse({"status": 403, "message": "用户未登录"})