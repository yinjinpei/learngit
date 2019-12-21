from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls import url
from . import views
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^index/', views.index),
    # url(r'^login/', views.login),
    # url(r'^register/', views.register),
    # url(r'^logout/', views.logout),

    re_path('login$', views.login,name='login'),
    re_path('register$', views.register,name='register'),
    re_path('logout$', views.logout,name='logout'),
    re_path('index$', views.index, name='index'),
    re_path('', views.index, name='index'),
]
