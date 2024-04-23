from django.urls import path,re_path
from . import views

urlpatterns = [
    path('login/',views.LoginAPIView.as_view(),name='login'),
    re_path(r"^mobile/(?P<mobile>1[3-9]\d{9})/$", views.MobileAPIView.as_view()),
    path("register/", views.UserAPIView.as_view()),
]