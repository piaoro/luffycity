from rest_framework_jwt.views import ObtainJSONWebToken
from luffycityapi.utlis.tencentcloudapi import TencentCloudAPI, TencentCloudSDKException
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from rest_framework.generics import CreateAPIView
from .serializers import UserRegisterModelSerializer


# Create your views here.
class LoginAPIView(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        try:
            api = TencentCloudAPI()
            result = api.captcha(
                request.data.get("ticket"),
                request.data.get("randstr"),
                request._request.META.get("REMOTE_ADDR"),
            )
            if result:
                return super().post(request, *args, **kwargs)
            else:
                raise TencentCloudSDKException
        except TencentCloudSDKException as err:
            return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)


class MobileAPIView(APIView):
    def get(self, request, mobile):
        """
        校验手机号是否已注册
        :param request:
        :param mobile: 手机号
        :return:
        """
        try:
            User.objects.get(mobile=mobile)
            return Response({"errmsg": "当前手机号已注册"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            # 如果查不到该手机号的注册记录，则证明手机号可以注册使用
            return Response({"errmsg": "OK"}, status=status.HTTP_200_OK)

class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterModelSerializer