from . import constants
from rest_framework.generics import ListAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class CacheListAPIView(ListAPIView):
    @method_decorator(cache_page(constants.LIST_PAGE_CACHE_TIME))
    def get(self,request,*args,**kwargs):
        return super().get(request,*args,**kwargs)