from rest_framework_jwt.views import ObtainJSONWebToken
from luffycityapi.utlis.tencentcloudapi import TencentCloudAPI,TencentCloudSDKException
from rest_framework.response import Response
from rest_framework import status

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
                return super().post(request,*args,**kwargs)
            else:
                raise TencentCloudSDKException
        except TencentCloudSDKException as err:
            return Response({"errmsg": "验证码校验失败！"}, status=status.HTTP_400_BAD_REQUEST)
