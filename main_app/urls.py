from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.create_view, name='login_view'),
]