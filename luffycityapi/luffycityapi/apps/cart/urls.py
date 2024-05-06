from django.urls import path, re_path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.CartAPIView.as_view())
]
