
'''
@file serializers.py

@brief 序列化模型 使用PE8标准

@details 创建序列化模型 for rest_framework

@author 程栋权

@email cdongquan@foxmail.com

@version 1.0.0

@date 2022/04/25 10:06:37

'''


from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # field = ['name', 'degree', 'college', 'mojor', 'grad_date',
        #          'card_id', 'phone', 'bank', 'bank_id', 'email']


class PostionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Postion
        fields = '__all__'
        # field = ['user', 'is_probation', 'is_formal', 'is_direct', 'entry_date', 'formal_date',
        #          'quit_date', 'probation_end_date', 'department', 'level', 'is_manager', 'is_labor', 'company']


class SalarySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Salary
        fields = '__all__'
        # field = ['probation_salary', 'formal_salary', 'performance_salary', 'management_salary',
        #          'commission', 'social', 'fund', 'tax', 'modification_before_tax', 'modification_after_tax']


class LeaveSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Leave
        fields = '__all__'
        # field = ['leave_id', 'user', 'start_time', 'end_time', 'leave']


class ReportSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Report
        fields = '__all__'
        # field = ['user', 'type', 'time']


class Work_OvertimeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Work_Overtime
        fields = '__all__'
        # field = ['work_overtime_id', 'user', 'detail',
        #          'overtime_start_datetime', 'overtime_end_datetime']
