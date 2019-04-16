from django.contrib import admin
from django.urls import path,include
from . import views
from rest_framework import routers
app_name = 'cropsuggestion'

urlpatterns = [
    path('', views.index, name='index'),

    path('test/', views.apitest.as_view(), name='test'),
    path('testform/', views.test_form, name='testfrom'),

]