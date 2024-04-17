from rest_framework.generics import ListAPIView
from .models import Nav
from .serializers import NavModelSerializers
import constants



class NavHeaderListAPIView(ListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_HEADER_POSITION, is_show=True, is_delete=False).order_by("orders",
                                                                                                        "-id")[
               :constants.NAV_HEADER_SIZE]
    serializer_class = NavModelSerializers


class NavFooterListAPIView(ListAPIView):
    queryset = Nav.objects.filter(position=constants.NAV_FOOTER_POSITION, is_show=True, is_delete=False).order_by("orders",
                                                                                                        "-id")[
               :constants.NAV_FOOTER_SIZE]
    serializer_class = NavModelSerializers
