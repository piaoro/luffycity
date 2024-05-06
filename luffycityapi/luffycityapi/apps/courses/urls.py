from django.urls import path,re_path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# 注册全文搜索到视图集中生成url路由信息
router.register("search",views.CourseSearchViewSet,basename="course-search")
urlpatterns = [
    path("directions/",views.CourseDirectionListAPIView.as_view()),
    re_path(r"category/(?P<direction>\d+)",views.CourseCategoryListAPIView.as_view()),
    re_path(r"^(?P<direction>\d+)/(?P<category>\d+)/$",views.CourseListAPIView.as_view()),
    path("hot_word/",views.HotWordAPIView.as_view()),
    re_path("^(?P<pk>\d+)/$", views.CourseRetrieveAPIView.as_view()),
    re_path("^(?P<course>\d+)/chapters/$", views.CourseChapterListAPIView.as_view()),
] + router.urls