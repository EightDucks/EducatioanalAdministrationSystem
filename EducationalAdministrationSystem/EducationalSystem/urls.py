#coding: utf-8
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^jiaowu/$', views.displayCourseForEA, name='jiaowu'),
    url(r'^jiaowu_addcourse/$', views.jiaowu_addcourse, name='jiaowu_addcourse'),
    url(r'^jiaowu_addsemester/$', views.jiaowu_addsemester, name='jiaowu_addsemester'),

    # 教务、学生、教师页头部
    url(r'^header.html$', views.header, name = 'header'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^addCourse/$', views.addCourse, name='addCourse'),
    url(r'^saveTermInfo/$', views.saveTermInfo, name='saveTermInfo'),
    url(r'^student/$', views.displayCourseForStudent, name='student'),
    url(r'^teacher/$', views.displayCourseForTeacher, name='teacher'),
    url(r'^jiaowu/course/(\d+)/$', views.jiaowu_courseinfo, name='jiaowu_courseinfo'),
]