from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny


class UserModelViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class PostionModelViewSet(ModelViewSet):
    serializer_class = PostionSerializer
    queryset = Postion.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class SalaryModelViewSet(ModelViewSet):
    serializer_class = SalarySerializer
    queryset = Salary.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class LeaveModelViewSet(ModelViewSet):
    serializer_class = LeaveSerializer
    queryset = Leave.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class ReportModelViewSet(ModelViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class Work_OvertimeModelViewSet(ModelViewSet):
    serializer_class = Work_OvertimeSerializer
    queryset = Work_Overtime.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [AllowAny]


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        pass
