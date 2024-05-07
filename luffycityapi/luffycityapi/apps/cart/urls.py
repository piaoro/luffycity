from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.CartAPIView.as_view()),
    path('order/',views.CartOrderAPIView.as_view())
]
