"""liusblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('article/', views.article_detail, name='article_detail'),
    path('about/', views.about_me, name='about_me'),
    path('login/', views.login, name='login'),
    path('thridpaty_login/<str:type>', views.thridpaty_login, name='thridpaty_login'),
    path('register/', views.register, name='register'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('verify/', views.verify, name='verify'),
    path('logout/', views.logout, name='logout'),
    path('resetpasswd/', views.resetpasswd, name='resetpasswd'),
    path('logout/', views.logout, name='logout'),
    

    #Test google search
    #path('google/<str:keyworkd>', views.google, name='google'),
]
