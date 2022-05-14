"""salary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app01 import urls as app01_urls
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(app01_urls)),

    # html
    path('load/leave.html', TemplateView.as_view(template_name='load/leave.html')),
    path('load/report_day.html', TemplateView.as_view(template_name='load/report_day.html')),
    path('load/report_week.html', TemplateView.as_view(template_name='load/report_week.html')),
    path('statistic/leave.html', TemplateView.as_view(template_name='statistic/leave.html')),
    path('statistic/report.html', TemplateView.as_view(template_name='statistic/report.html')),
    path('login.html', TemplateView.as_view(template_name='login.html')),
]
