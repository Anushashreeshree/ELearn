"""
URL configuration for elearn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path,include
from elearnapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('main/<int:sid>',views.main,name='main'),
    path('forgot-password/', views.forget_password, name='forget_password'),
    path('verify-otp/',    views.verify_otp,    name='verify_otp'),
    path('new_password/',views.new_password,name='new_password'),
    path('admindash/',views.admindash,name='admindash'),
    path('dash.html',views.dash,name='dash'),
    path('course_creation/',views.course_creation,name='course'),
    path('course_update/<int:s>',views.course_update,name='course_update'),
    path('course_delete/<int:s>',views.course_delete,name='course_delete')
]
