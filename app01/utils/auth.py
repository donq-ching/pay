
'''
@file auth.py

@brief token验证中间件

@details 验证是否登录

@author 程栋权

@email cdongquan@foxmail.com

@version 1.0.0

@date 2022/04/25 11:19:46

'''
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import UserAuth

class Lauth(BaseAuthentication):
    def authenticate(self,request):
        token = request.GET.get("token")
        token_obj = UserAuth.objects.filter(token=token).first()
        
        if not token_obj:
            raise AuthenticationFailed("认证失败")
        return (token_obj.user,token_obj)

