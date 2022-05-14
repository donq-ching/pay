
'''
@file admin.py

@brief Admin文件 使用PE8规范

@details 美化Admin界面

@author 程栋权

@email cdongquan@foxmail.com

@version 1.0.0

@date 2022/04/25 09:25:56

'''

from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree', 'college', 'mojor',
                    'grad_date', 'card_id', 'phone', 'bank', 'bank_id', 'email')
    list_display_links = ('name', )
    list_per_page = 20
    ordering = ('-name',)
    search_fields = ('name',)


class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'token')
    list_display_links = ('user_name', )
    list_per_page = 20
    ordering = ('-user__name',)
    search_fields = ('user__name',)

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = '用户名'


class UserCodeAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'code', 'send_code_time')
    list_display_links = ('user_name', )
    list_per_page = 20
    ordering = ('-user__name',)
    search_fields = ('user__name',)

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = '用户名'


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'datail')
    list_display_links = ('name', )
    list_per_page = 20


class Position_Level_Admin(admin.ModelAdmin):
    list_display = ('level', 'department')
    list_display_links = ('level', )
    list_per_page = 20

    def department_name(self, obj):
        return obj.department.name
    department_name.short_description = '部门'


class PostionAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'is_probation', 'is_direct', 'is_manager', 'is_labor', 'entry_date',
                    'quit_date', 'probation_end_date', 'department_name', 'level_name', 'company')
    list_display_links = ('user_name', )
    list_per_page = 20
    ordering = ('-user__name',)
    search_fields = ('user__name',)

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = '用户名'

    def department_name(self, obj):
        return obj.postion_level.department.name
    department_name.short_description = '部门'

    def level_name(self, obj):
        return obj.postion_level.level
    level_name.short_description = '岗位等级'


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'probation_salary', 'formal_salary', 'performance_salary', 'performance_salary_coefficient', 'management_salary',
                    'subsidy', 'commission', 'social_radix', 'fund_radix', 'social', 'fund', 'tax', 'modification_before_tax', 'modification_after_tax')
    list_display_links = ('user_name', )
    list_per_page = 20
    ordering = ('-user__name',)
    search_fields = ('user__name',)

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = '用户名'


class LeaveAdmin(admin.ModelAdmin):
    list_display = ('leave_id', 'user_name', 'start_time', 'end_time', 'leave')
    list_display_links = ('user_name', )
    list_per_page = 20
    ordering = ('-user__name',)
    search_fields = ('user__name',)

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = '用户名'


class ReportAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'type', 'time')
    list_display_links = ('user_name', )
    list_per_page = 20
    ordering = ('-user__name',)
    search_fields = ('user__name',)

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = '用户名'


class Work_Overtime_Admin(admin.ModelAdmin):
    list_display = ('work_overtime_id', 'user_name', 'detail',
                    'overtime_start_datetime', 'overtime_end_datetime')
    list_display_links = ('user_name', )
    list_per_page = 20
    ordering = ('-user__name',)
    search_fields = ('user__name',)

    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = '用户名'


admin.site.register(User, UserAdmin)
admin.site.register(UserToken, UserTokenAdmin)
admin.site.register(UserCode, UserCodeAdmin)
admin.site.register(Postion, PostionAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Work_Overtime, Work_Overtime_Admin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Position_Level, Position_Level_Admin)
