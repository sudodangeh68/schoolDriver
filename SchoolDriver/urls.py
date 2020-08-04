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
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import PasswordResetView
from Base import views
from Base.views import *

urlpatterns = [
    path('api/', include('api.urls')),
    path('', Login.as_view(), name='login'),
    path('home/', Main.as_view(), name='home'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('password/', views.change_password, name='change_password'),


    path('join/<int:driver_id>/', join.as_view(), name='join'),

    path('parent-school/', AddParent.as_view(), name='parent'),

    path('parent/', Parent.as_view(), name='parent'),
    path('parent/add/', AddParent.as_view(), name='add_parent'),
    path('parent/update/', UpdateParent.as_view(), name='update_parent'),

    path('headmaster/', Headmaster.as_view(), name='headmaster'),
    path('headmaster/add/', AddHeadmaster.as_view(), name='add_headmaster'),
    path('headmaster/update/<int:id>/', UpdateHeadmaster.as_view(), name='update_headmaster'),

    path('school/', School_list.as_view(), name='school'),
    path('school/add/', AddSchool.as_view(), name='add_school'),
    path('school/update/<int:id>/', UpdateSchool.as_view(), name='update_school'),

    path('student/', StudentList.as_view(), name='student'),
    path('student/add/', AddStudent.as_view(), name='add_student'),
    path('student/update/<int:id>/', UpdateStudent.as_view(), name='update_student'),

    path('driver/', Driver.as_view(), name='driver'),
    path('driver/add/', AddDriver.as_view(), name='add_driver'),
    path('driver/update/<int:id>/', UpdateDriver.as_view(), name='update_driver'),
]
