from .models import Nav,Banner
from .serializers import NavModelSerializers,BannerModelSerializer
from luffycityapi.utlis import constants
from luffycityapi.utlis.views import CacheListAPIView



class NavHeaderListAPIView(CacheListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_delete=False).order_by("orders",
                                                                                                        "-id")[
               :constants.NAV_HEADER_SIZE]
    serializer_class = NavModelSerializers


class NavFooterListAPIView(CacheListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_delete=False).order_by("orders",
                                                                                                        "-id")[
               :constants.NAV_FOOTER_SIZE]
    serializer_class = NavModelSerializers

class BannerListAPIView(CacheListAPIView):
    queryset = Banner.objects.filter(is_show=True,is_delete=False).order_by("orders","-id")[:constants.BANNER_SIZE]
    serializer_class = BannerModelSerializer
