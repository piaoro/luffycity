from django.urls import path
from . import views

urlpatterns = [
    path("directions/",views.CourseDirectionListAPIView.as_view()),
    path("category/",views.CourseDirectionListAPIView.as_view()),
]