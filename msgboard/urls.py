from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^login/$', views.msg_user_login, name='login'),
    url(r'^logout/$', views.msg_user_logout, name='logout'),
    url(r'^register/$', views.msg_user_register, name='register'),
    url(r'^pushMsg/$', views.msg_push, name='pushMsg'),
    url(r'^getMsg/$', views.msg_get, name='getMsg'),
    url(r'^test/$', views.test, name='test'),
]
