'''
@file models.py

@brief 模型文件 使用PE8规范

@details 创建数据库模型

@author 程栋权

@email cdongquan@foxmail.com

@version 1.0.0

@date 2022/04/24 15:29:31

'''


import json
from datetime import datetime
from django.db import models

# 增加了UID字段,大改
class User(models.Model):
    uid = models.CharField(verbose_name='用户唯一ID', primary_key=True, max_length=128)
    name = models.CharField(max_length=64, verbose_name='用户名')
    degree_choice = ((0, '高中'), (1, '专科'), (2, '本科'), (3, '硕士'), (4, '博士'))
    degree = models.SmallIntegerField(verbose_name='选择学历',
                                      choices=degree_choice, default=2, blank=True, null=True)
    college = models.CharField(max_length=128, verbose_name='毕业学校', null=True)
    mojor = models.CharField(max_length=128, verbose_name='专业名称', null=True)
    grad_date = models.DateField(verbose_name='毕业时间', null=True)
    card_id = models.CharField(
        verbose_name='身份证号', max_length=32, blank=False, unique=True)
    phone = models.CharField(
        verbose_name='联系方式', max_length=32, blank=False, unique=True)
    bank = models.CharField(verbose_name='开户行', max_length=64, blank=False)
    bank_id = models.CharField(
        verbose_name='银行卡号', max_length=32, blank=False, unique=True)
    email = models.EmailField(verbose_name='电子邮箱', unique=True)

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['name']


class UserToken(models.Model):
    user = models.OneToOneField(
        to="User", on_delete=models.CASCADE, verbose_name='关联用户')
    token = models.CharField(max_length=64, unique=True, verbose_name='token')

    class Meta:
        db_table = 'usertoken'
        verbose_name = 'Token表'
        verbose_name_plural = verbose_name


class UserCode(models.Model):
    user = models.OneToOneField(
        to="User", on_delete=models.CASCADE, verbose_name='关联用户')
    code = models.CharField(max_length=64, unique=True, verbose_name='验证码')
    send_code_time = models.DateTimeField(
        verbose_name='发送时间', default=datetime.now)

    # def __str__(self):
    #     _dict = {
    #         'token': self.token,
    #         'code': self.code,
    #         'email': self.user.email,
    #     }
    #     return json.dumps(_dict)

    class Meta:
        db_table = 'usercode'
        verbose_name = '验证码表'
        verbose_name_plural = verbose_name


class Department(models.Model):
    name = models.CharField(
        verbose_name='部门', primary_key=True, max_length=32)
    datail = models.CharField(max_length=128, verbose_name='部门详情')

    class Meta:
        db_table = 'department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['name']


class Position_Level(models.Model):
    level = models.CharField(
        verbose_name='岗位等级', max_length=32, primary_key=True)
    department = models.ForeignKey(
        to=Department, verbose_name='关联部门', on_delete=models.CASCADE)

    class Meta:
        db_table = 'position_level'
        verbose_name = '职位等级'
        verbose_name_plural = verbose_name
        ordering = ['level']


class Postion(models.Model):
    user = models.OneToOneField(to=User, verbose_name='关联用户',
                                on_delete=models.CASCADE, primary_key=True)
    is_probation = models.BooleanField(verbose_name='是否是在试用期', default=True)
    is_formal = models.BooleanField(verbose_name='是否是转正', default=False)
    is_direct = models.BooleanField(verbose_name='是否是直管', default=False)
    entry_date = models.DateField(verbose_name='入职日期')
    formal_date = models.DateField(verbose_name='转正日期', null=True)
    quit_date = models.DateField(verbose_name='离职时间', null=True)
    probation_end_date = models.DateField(verbose_name='试用期截止时间', null=True)
    postion_level = models.ForeignKey(
        to=Position_Level, verbose_name='关联等级', on_delete=models.CASCADE)
    is_manager = models.BooleanField(verbose_name='是否是主管', default=False)
    is_labor = models.BooleanField(verbose_name='是否劳务', default=False)
    company = models.CharField(max_length=128, verbose_name='所属公司')

    class Meta:
        db_table = 'postion'
        verbose_name = '职位'
        verbose_name_plural = verbose_name
        ordering = ['user__name']


class Salary(models.Model):
    user = models.OneToOneField(to=User, verbose_name='关联用户',
                                on_delete=models.CASCADE, primary_key=True)
    probation_salary = models.IntegerField(verbose_name='试用期薪资')
    formal_salary = models.IntegerField(verbose_name='转正后薪资')
    performance_salary = models.IntegerField(verbose_name='绩效薪资')
    management_salary = models.IntegerField(verbose_name='管理岗薪资')
    commission = models.IntegerField(verbose_name='提成')
    social = models.IntegerField(verbose_name='社保')
    fund = models.IntegerField(verbose_name='公积金')
    tax = models.IntegerField(verbose_name='个税')
    modification_before_tax = models.IntegerField(verbose_name='税前工资调整')
    modification_after_tax = models.IntegerField(verbose_name='税后工资调整')

    class Meta:
        db_table = 'salary'
        verbose_name = '薪资'
        verbose_name_plural = verbose_name
        ordering = ['-formal_salary', '-performance_salary']


class Leave(models.Model):
    leave_id = models.CharField(
        verbose_name='审批编号', primary_key=True, max_length=128)
    user = models.ForeignKey(
        to=User, verbose_name='关联用户', on_delete=models.CASCADE)
    start_time = models.DateTimeField(verbose_name='请假开始日期', blank=False)
    end_time = models.DateTimeField(verbose_name='请假结束日期', blank=False)
    leave_choice = ((0, '事假'), (1, '年休假'), (2, '婚假'), (3, '产假'), (4, '哺乳假'),
                    (5, '陪产假'), (6, '丧假'), (7, '工伤假'), (8, '病假'), (9, '调休假'))
    leave = models.SmallIntegerField(
        verbose_name='请假类型', choices=leave_choice, default=0)

    class Mete:
        db_table = 'leave'
        verbose_name = '请假'
        verbose_name_plural = verbose_name


class Report(models.Model):
    user = models.ForeignKey(
        to=User, verbose_name='关联用户', on_delete=models.CASCADE)
    type_choice = ((0, '周计划'), (1, '日报'))
    type = models.SmallIntegerField(
        verbose_name='汇报类型', choices=type_choice, default=1)
    time = models.DateTimeField(verbose_name='汇报时间')

    class Meta:
        db_table = 'report'
        verbose_name = '周计划与日报'
        verbose_name_plural = verbose_name


class Work_Overtime(models.Model):
    work_overtime_id = models.CharField(
        verbose_name='加班编号', primary_key=True, max_length=128)
    user = models.ForeignKey(
        to=User, verbose_name='关联用户', on_delete=models.CASCADE)
    detail = models.TextField(verbose_name='详细说明')
    overtime_start_datetime = models.DateTimeField(verbose_name='加班开始时间')
    overtime_end_datetime = models.DateTimeField(verbose_name='结束时间')

    class Meta:
        db_table = 'work_overtime'
        verbose_name = '加班'
        verbose_name_plural = verbose_name
