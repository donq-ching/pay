from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .utils import load_data

urlpatterns = [
    path('load_leave_data/', load_data.load_leave_data),
    path('load_report_data/', load_data.load_report_data),
    path('login/', views.LoginView.as_view()),
    path('leave/', views.LeaveView.as_view()),
    path('report/', views.ReportView.as_view()),
]

# router = DefaultRouter()
# router.register('user', viewset=views.UserModelViewSet)
# router.register('postion', viewset=views.PostionModelViewSet)
# router.register('salary', viewset=views.SalaryModelViewSet)
# router.register('leave', viewset=views.LeaveModelViewSet)
# router.register('report', viewset=views.ReportModelViewSet)
# router.register('work_Overtime', viewset=views.Work_OvertimeModelViewSet)

# urlpatterns += router.urls
