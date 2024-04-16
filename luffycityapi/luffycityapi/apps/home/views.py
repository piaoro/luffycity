from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_redis import get_redis_connection
import logging
# Create your views here.

logger = logging.getLogger('django')


class HomeAPIView(APIView):
    def get(self, request):
        # logger.debug('debug信息')
        # logger.info("info信息")
        redis = get_redis_connection("sms_code")
        brother = redis.lrange("brother",0,-1)
        return Response(brother,status=status.HTTP_200_OK)
