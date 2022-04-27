
'''
@file views.py

@brief 

@details 

@author 程栋权

@email cdongquan@foxmail.com

@version 1.0.0

@date 2022/04/27 15:04:44

'''


import uuid

from chinese_calendar import is_holiday, is_workday

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.permissions import AllowAny

from .utils.auth import LoginAuth
from .models import *
from .serializers import *

import datetime

# class UserModelViewSet(ModelViewSet):
#     authentication_classes = [LoginAuth, ]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     pagination_class = PageNumberPagination
#     permission_classes = [AllowAny]


# class PostionModelViewSet(ModelViewSet):
#     authentication_classes = [LoginAuth, ]
#     serializer_class = PostionSerializer
#     queryset = Postion.objects.all()
#     pagination_class = PageNumberPagination
#     permission_classes = [AllowAny]


# class SalaryModelViewSet(ModelViewSet):
#     authentication_classes = [LoginAuth, ]
#     serializer_class = SalarySerializer
#     queryset = Salary.objects.all()
#     pagination_class = PageNumberPagination
#     permission_classes = [AllowAny]


# class LeaveModelViewSet(ModelViewSet):
#     authentication_classes = [LoginAuth, ]
#     serializer_class = LeaveSerializer
#     queryset = Leave.objects.all()
#     pagination_class = PageNumberPagination
#     permission_classes = [AllowAny]


# class ReportModelViewSet(ModelViewSet):
#     authentication_classes = [LoginAuth, ]
#     serializer_class = ReportSerializer
#     queryset = Report.objects.all()
#     pagination_class = PageNumberPagination
#     permission_classes = [AllowAny]


# class Work_OvertimeModelViewSet(ModelViewSet):
#     authentication_classes = [LoginAuth, ]
#     serializer_class = Work_OvertimeSerializer
#     queryset = Work_Overtime.objects.all()
#     pagination_class = PageNumberPagination
#     permission_classes = [AllowAny]


# 未完成邮箱验证，Token已经完成
class LoginView(APIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        user = User.objects.all().filter(email=email).first()
        if user:
            token = str(uuid.uuid4())
            UserToken.objects.update_or_create(
                defaults={'token': token}, user=user)
            return Response({'message': '登录成功', 'code': 100, 'token': token})
        else:
            return Response({'message': '没有该邮箱', 'code': 101})


# 完成
class LeaveView(APIView):
    # authentication_classes = [LoginAuth,]

    def get_leave_len(self, leave_time):
        # 1. 同一天 下午-下午 0.5天 0小时
        # 2. 同一天 上午-下午 1天 9小时
        # 3. 第一天上午-第二天上午 1 + 0.5天 12小时
        # 4. 第一天上午-第二天下午 1 + 1天 9 + 12小时
        leave_len = 0
        if leave_time.days == 0:
            # 是同一天
            if leave_time.seconds/(60*60) == 0:
                leave_len = 0.5
            else:
                leave_len = 1
        else:
            # 不是同一天
            leave_len = leave_time.days
            if leave_time.seconds/(60*60) == 0:
                leave_len += 0.5
            else:
                leave_len += 1

        return leave_len

    def get(self, request, *args, **kwargs):
        # 目的:获取请假信息，还有请假时长
        # 1. 从数据库获取到信息
        # 2. 判断是否为调休假，如果是就需要判断是否有对应的加班信息
        # 3. 统计每个人的请假信息
        # 4. 返回，如果有人没有请假信息对应为0
        start_date = request.GET.get('start_date')
        try:
            start_date = datetime.datetime.strptime(
                start_date, r"%Y-%m-%d %H:%M")
            # start_date = datetime.datetime(2021, 4, 21, 8, 30)
        except Exception as e:
            return Response({'message': '时间有误'})

        ret = {k['name']: {'非调休假': 0, '调休假': 0}
               for k in User.objects.values('name').distinct()}
        leaves = Leave.objects.filter(start_time__gte=start_date)

        for leave in leaves:
            leave_len = self.get_leave_len(leave.end_time - leave.start_time)
            if leave.leave == 9:
                # 请假类型为调休假
                ret[leave.user.name]['调休假'] += leave_len
            else:
                ret[leave.user.name]['非调休假'] += leave_len

        return Response(ret)

# 完成
class ReportView(APIView):
    # authentication_classes = [LoginAuth, ]
    def get(self, request, *args, **kwargs):
        # http://127.0.0.1/app01/report_all/?start_date=2021-1-1&end_date=2022-4-27
        # 目的：获取日报与周计划中迟到提交的信息，并返回
        # 1. 从数据库获取信息
        # 2. 判断是否迟到提交、统计每个人的迟到提交信息
        # 3. 返回

        # 检查请求头上传的时间格式是否正确
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        print(start_date)
        print(end_date)
        try:
            start_date = datetime.datetime.strptime(start_date, r"%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, r"%Y-%m-%d")
        except Exception as e:
            print(e)
            return Response({'message': '时间有误'})

        # ret
        ret = {k['name']: {'日报': {'正常': 0, '异常': 0, '未提交': 0}, '周计划': {'正常': 0, '异常': 0, '未提交': 0}}
               for k in User.objects.values('name').distinct()}

        # 这里的name需要注意，需要换成user_id  才能避免同名导致的异常情况，或者换成email
        for name in [k for k in ret]:
            # 日报
            # 第一天到最后一天遍历
            # 先判断是否为工作日
            # 再查询数据库，查找对应数据，返回正常提交、异常提交或未提交的信息
            for i in range((end_date-start_date).days+1):
                day = start_date + datetime.timedelta(days=i)
                if is_workday(day):
                    data = Report.objects.filter(
                        time__year=day.year, time__month=day.month, time__day=day.day, user__name=name, type=1).order_by('time')
                    if not data:
                        ret[name]['日报']['未提交'] += 1
                        continue
                    # 上面已经continue so...
                    data = data[0]
                    if data.time <= datetime.datetime(day.year, day.month, day.day, 20, 0):
                        # 按时完成日报填写
                        ret[name]['日报']['正常'] += 1
                    else:
                        ret[name]['日报']['异常'] += 1

            # 周计划 只有主管才有周计划
            # 先判断这个人是不是主管
            # 判断当前日期是否为每周第一天上班日
            # 每周第一天上班日未查询到周计划，就去周末里查找
            if Postion.objects.filter(user__name=name, is_manager=True):
                for i in range((end_date-start_date).days+1):
                    day = start_date + datetime.timedelta(days=i)
                    day_1 = day-datetime.timedelta(days=1)
                    # 判断是不是第一天上班日
                    if is_workday(day) and is_holiday(day_1):
                        data = Report.objects.filter(
                            time__year=day.year, time__month=day.month, time__day=day.day, user__name=name, type=0).order_by('time')
                        if data:
                            data = data[0]
                            if data.time <= datetime.datetime(day.year, day.month, day.day, 9, 30):
                                ret[name]['周计划']['正常'] += 1
                            else:
                                ret[name]['周计划']['异常'] += 1
                        else:
                            # 判断是否是上周最后一个工作日结束时提交
                            status = False
                            while is_holiday(day_1):
                                data = Report.objects.filter(
                                    time__year=day_1.year, time__month=day_1.month, time__day=day_1.day, user__name=name, type=0).order_by('time')[0]
                                if data:
                                    ret[name]['周计划']['正常'] += 1
                                    status = True
                                    break
                                else:
                                    day_1 -= datetime.timedelta(days=1)
                            if not status:
                                ret[name]['周计划']['未提交'] += 1

        return Response(ret)


class Work_OvertimeView(APIView):
    authentication_classes = [LoginAuth, ]

    def get(self, request, *args, **kwargs):
        # 返回每个人的加班信息
        # 这个可以最后写
        pass


class SalaryView(APIView):
    authentication_classes = [LoginAuth, ]

    def get(self, request, *args, **kwargs):
        # 最重要的view，返回最后的每人工资单
        # 1. 目前算法还不清楚，需要查文件
        pass
