
'''
@file auth.py

@brief 认证文件

@details Token和时间认证类

@author 程栋权

@email cdongquan@foxmail.com

@version 1.0.0

@date 2022/04/25 11:19:46

'''
import datetime

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from ..models import UserToken

class LoginAuth(BaseAuthentication):
    def authenticate(self,request):
        token = request.META.get('HTTP_TOKEN')
        user_token = UserToken.objects.all().filter(token=token).first()
        
        if user_token:
            return user_token.user, token
        else:
            raise AuthenticationFailed("认证失败")

class DateAuth():
    def authenticate_header(self, request):
        pass
    def authenticate(self, request):
        if request.method == 'GET':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            try:
                start_date = datetime.datetime.strptime(start_date, r"%Y-%m-%d")
                end_date = datetime.datetime.strptime(end_date, r"%Y-%m-%d")
                request.start_date = start_date
                request.end_date = end_date
            except Exception as e:
                raise AuthenticationFailed("时间有误")


class DateTimeAuth():
    def authenticate_header(self, request):
        pass
    def authenticate(self, request):
        if request.method == 'GET':
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            try:
                start_date = datetime.datetime.strptime(start_date, r"%Y-%m-%d %H:%M")
                end_date = datetime.datetime.strptime(end_date, r"%Y-%m-%d %H:%M")
                request.start_date = start_date
                request.end_date = end_date
            except Exception as e:
                raise AuthenticationFailed("时间有误")
