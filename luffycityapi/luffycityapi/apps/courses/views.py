from rest_framework.generics import ListAPIView
from .serializers import CourseDirectionModelSerializer,CourseDirection,CourseCategoryModelSerializer,CourseCategory

# Create your views here.
class CourseDirectionListAPIView(ListAPIView):
    """学习方向"""
    queryset = CourseDirection.objects.filter(is_show=True,is_delete=False).order_by("orders","-id")
    serializer_class = CourseDirectionModelSerializer
    pagination_class = None

class CourseCategoryListAPIView(ListAPIView):
    "课程分类"
    queryset = CourseCategory.objects.filter(is_show=True,is_delete=False).order_by("orders","-id")
    serializer_class = CourseCategoryModelSerializer
    pagination_class = None