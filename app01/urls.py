from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .utils import load_data
from .utils.load_to_sqlite import load_to_sqlite

urlpatterns = [
    # 上传数据
    path('load_leave_data/', load_data.load_leave_data),
    path('load_report_data/', load_data.load_report_data),

    # 验证码与登录
    path('login/', views.LoginView.as_view()),
    path('email_code/', views.EmailCodeView.as_view()),

    # 获取全部信息
    path('leaves/', views.LeaveView.as_view()),
    path('reports/', views.ReportView.as_view()),
    path('salarys/', views.SalaryView.as_view()),
    

    # 带token获取用户单个信息
    path('report/', views.UserReportView.as_view()),
    path('leave/', views.UserLeaveView.as_view()),
    # path('salary/', views.SalaryView.as_view()),

    # 初始化通道
    path('sqlite/', load_to_sqlite),
]
