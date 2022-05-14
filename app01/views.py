import uuid
import datetime
import pandas as pd
from random import Random

from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from salary.settings import EMAIL_FROM
from .models import User, UserToken, UserCode, Leave, Report
from .utils.auth import LoginAuth, DateAuth, DateTimeAuth
from .utils.statistic_data import statistic_leave, statistic_report, statistic_salary


class EmailCodeView(APIView):
    authentication_classes = []

    def random_code(self, n=4):
        s = ''
        chars = '0123456789'
        random = Random()
        for i in range(n):
            s += chars[random.randint(0, len(chars) - 1)]
        return s

    def email_verify(self, email):
        user = User.objects.filter(email=email)
        if not user:
            return 401
        one_minute_age = datetime.datetime.now() - datetime.timedelta(hours=0,
                                                                      minutes=1, seconds=0)
        usercode = UserCode.objects.filter(
            send_code_time__gte=one_minute_age, user__email=email)
        if usercode:
            return 403
        return 200

    def send_code(self, email):
        code = self.random_code()
        email_title = '薪酬系统验证码'
        email_body = '你的邮箱验证码是:%s' % code
        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = 'html'
        send_status = msg.send()
        if send_status == 0:
            return 500
        # 发送成功，写入数据库, 这里的user一定是存在的
        usercode = UserCode()
        usercode.user = User.objects.filter(email=email).first()
        usercode.code = code
        usercode.save()
        return 200

    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        ret = {'message': '验证码发送失败'}
        email_verify_status = self.email_verify(email)

        if email_verify_status != 200:
            ret['错误码'] = email_verify_status
            return Response(ret)

        send_code_status = self.send_code(email)
        if send_code_status == 500:
            ret['错误码'] = 500
            return Response(ret)
        else:
            ret['message'] = '验证码发送成功'
            return Response(ret)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        code = request.POST.get('code')

        five_minute_age = datetime.datetime.now() - datetime.timedelta(hours=0,
                                                                       minutes=5, seconds=0)
        usercode = UserCode.objects.filter(
            send_code_time__gte=five_minute_age, user__email=email, code=code).order_by('send_code_time').first()

        if usercode:
            # 验证码没有用，真正的删除数据
            usercode.delete()
            user = User.objects.filter(email=email).first()
            token = str(uuid.uuid4())
            UserToken.objects.update_or_create(
                defaults={'token': token}, user=user)
            return Response({'message': '登录成功', 'token': token})
        else:
            return Response({'message': '登录失败'})

class LeaveView(APIView):
    authentication_classes = [DateTimeAuth, ]
    # permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        start_date = request.start_date
        end_date = request.end_date

        return Response(statistic_leave(start_date, end_date))

    def post(self, request, *args, **kwargs):
        def get_leave_code(leave):
            leave_choice = ((0, '事假'), (1, '年休假'), (2, '婚假'), (3, '产假'), (4, '哺乳假'),
                            (5, '陪产假'), (6, '丧假'), (7, '工伤假'), (8, '病假'), (9, '调休假'))
            for el in leave_choice:
                if el[1] == leave:
                    return el[0]
        step = int(request.POST.get('step'))
        df = pd.read_excel(request.FILES.get('data'))
        df = df[df['当前审批状态'] == '已通过']
        df = pd.DataFrame(data=df, columns=[
                          '审批编号', '申请人', '请假类型', '开始时间', '结束时间'])
        leave_dict = df.to_dict(orient='records')

        if step != 1:
            return Response(leave_dict)

        ret = {'status': 413, 'userNotExist': [], 'repeat': []}
        for leave in leave_dict:
            if Leave.objects.filter(leave_id=leave['审批编号']):
                ret['repeat'].append(leave)
                continue

            user = User.objects.filter(name=leave['申请人'])
            if not user:
                ret['用户不存在'].append(leave)
                continue
            user = user[0]

            leave['开始时间'] = leave['开始时间'].replace(
                '上午', '08:30').replace('下午', '17:30').replace('/', '-')
            leave['结束时间'] = leave['结束时间'].replace(
                '上午', '08:30').replace('下午', '17:30').replace('/', '-')

            leave_model = Leave()
            leave_model.leave_id = leave['审批编号']
            leave_model.user = user
            leave_model.leave = get_leave_code(leave['请假类型'])
            leave_model.start_time = leave['开始时间']
            leave_model.end_time = leave['结束时间']
            leave_model.save()
            ret['status'] = 201
        return Response(ret)

class ReportView(APIView):
    authentication_classes = [DateAuth, ]
    # permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        start_date = request.start_date
        end_date = request.end_date

        return Response(statistic_report(start_date, end_date))

    def post(self, request, *args, **kwargs):
        report_type = int(request.POST.get('report_type'))
        step = int(request.POST.get('step'))
        df = pd.read_excel(request.FILES.get('data'))

        if report_type == 0:
            df = pd.DataFrame(data=df, columns=['提交时间', '申请人'])
            df.columns = ['time', 'name']
        elif report_type == 1:
            df = pd.DataFrame(data=df, columns=['汇报时间', '汇报人'])
            df.columns = ['time', 'name']
        df = df.dropna(axis=0)
        report_dict = df.to_dict(orient='records')
        if step != 1:
            return Response(report_dict)

        ret = {'status': 413, 'userNotExist': [], 'repeat': []}
        for report in report_dict:
            user = User.objects.filter(name=report['name'])
            if not user:
                ret['userNotExist'].append(report)
                continue
            user = user[0]

            report['time'] = str(report['time']).replace('/', '-')

            report_model = Report()
            report_model.user = user
            report_model.type = report_type
            report_model.time = report['time']
            try:
                report.save()
            except:
                ret['repeat'].append(report)
                continue
            ret['status'] = 201

        return Response(ret)

class UserReportView(APIView):
    authentication_classes = [DateAuth, LoginAuth, ]

    def get(self, request, *args, **kwargs):
        start_date = request.start_date
        end_date = request.end_date

        user = request.user
        reports = statistic_report(start_date, end_date)
        reports['汇报统计'] = reports['汇报统计'][user.name]
        return Response(reports)

class UserLeaveView(APIView):
    authentication_classes = [DateTimeAuth, LoginAuth, ]

    def get(self, request, *args, **kwargs):
        start_date = request.start_date
        end_date = request.end_date

        user = request.user
        leaves = statistic_leave(start_date, end_date)
        leaves['请假统计'] = leaves['请假统计'][user.name]
        return Response(leaves)

class SalaryView(APIView):
    authentication_classes = [DateTimeAuth, ]
    def get(self, request, *args, **kwargs):
        start_date = request.start_date
        end_date = request.end_date
        # 最重要的view，返回最后的每人工资单
        # 1. 目前算法还不清楚，需要查文件
        return Response(statistic_salary(start_date, end_date))
