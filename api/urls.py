"""SchoolDriver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.db import router
from django.urls import path, include


#from django.contrib.auth.views import login, logout
from Base.views import *
from api.views import UserList, UserCreate,DriverStudent

urlpatterns = [
    path('user/list/', UserList.as_view(), name='home'),
    path('user/create/', UserCreate.as_view(), name='home'),
    path('driver/student/', DriverStudent.as_view(), name='home'),
    # path('user/student/list/', UserList.as_view(), name='home'),
    ]
