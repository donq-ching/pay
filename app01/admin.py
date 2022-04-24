from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree', 'college', 'mojor', 'grad_date', 'card_id', 'phone', 'bank', 'bank_id', 'email')
    list_display_links = ('name', )
    list_per_page = 20
    ordering = ('-degree',)
    search_fields = ('user',)

class PostionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_probation', 'is_formal', 'is_direct', 'entry_date', 'formal_date', 'quit_date', 'probation_end_date', 'department', 'level', 'is_manager', 'is_labor', 'company')
    list_display_links = ('user', )
    list_per_page = 20
    ordering = ('-level',)
    search_fields = ('user',)

class SalaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'probation_salary', 'formal_salary', 'performance_salary', 'management_salary', 'commission', 'social', 'fund', 'tax', 'modification_before_tax', 'modification_after_tax')
    list_display_links = ('user', )
    list_per_page = 20
    ordering = ('-formal_salary',)
    search_fields = ('user',)

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('leave_id', 'user', 'start_time', 'end_time', 'leave')
    list_display_links = ('user', )
    list_per_page = 20
    ordering = ('-leave',)
    search_fields = ('user',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'time')
    list_display_links = ('user', )
    list_per_page = 20
    ordering = ('-time',)
    search_fields = ('user',)

class Work_Overtime_Admin(admin.ModelAdmin):
    list_display = ('work_overtime_id', 'user', 'detail', 'overtime_start_datetime', 'overtime_end_datetime')
    list_display_links = ('user', )
    list_per_page = 20
    ordering = ('-overtime_start_datetime',)
    search_fields = ('user',)



admin.site.register(User, UserAdmin)
admin.site.register(Postion, PostionAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Work_Overtime, Work_Overtime_Admin)