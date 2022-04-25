import imp
from random import Random
from django.core.mail import send_mail
from django.shortcuts import HttpResponse
from salary.settings import EMAIL_FROM  # setting.py添加的的配置信息

# 生成随机字符串


def random_str(n=4):
    s = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    random = Random()
    for i in range(n):
        s += chars[random.randint(0, len(chars) - 1)]
    return s


def send_code(request):
    email = request.GET.get('email')
    code = random_str()
    email_title = '验证码'
    send_status = send_mail(email_title, code, email)
    if not send_status:
        return HttpResponse('验证码发送错误')
