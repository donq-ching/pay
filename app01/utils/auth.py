
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
from ..models import UserToken

class LoginAuth(BaseAuthentication):
    def authenticate(self,request):
        token = request.META.get('HTTP_TOKEN')
        user_token = UserToken.objects.all().filter(token=token).first()
        
        if user_token:
            return user_token.name, token
        else:
            raise AuthenticationFailed("认证失败")