import re,random
from luffycityapi.utlis import constants
from rest_framework import serializers
from luffycityapi.utlis.authenticate import generate_jwt_token
from .models import User
from luffycityapi.utlis.tencentcloudapi import TencentCloudAPI, TencentCloudSDKException
from django_redis import get_redis_connection


class UserSmsLoginModelSerializer(serializers.ModelSerializer):
    val_mobile = serializers.IntegerField(required=True,write_only=True,help_text="手机号验证")
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")
    token = serializers.CharField(read_only=True)
    # ticket = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的临时凭证")
    # randstr = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的随机字符串")

    class Meta:
        model = User
        # fields = ["val_mobile","sms_code", "token", "ticket", "randstr"]
        fields = ["val_mobile", "sms_code", "token"]

    def validate(self, data):
        """验证客户端数据"""
        # 手机号格式验证
        mobile = data.get("val_mobile", None)
        if not re.match("^1[3-9]\d{9}$", str(mobile)):
            raise serializers.ValidationError(detail="手机号格式不正确！")
        # 手机号是否已注册
        try:
            User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail="手机号未注册！")
        # # 验证防水墙验证码
        # api = TencentCloudAPI()
        # result = api.captcha(
        #     data.get("ticket"),
        #     data.get("randstr"),
        #     self.context['request']._request.META.get("REMOTE_ADDR"),  # 客户端IP
        # )

        # if not result:
        #     raise serializers.ValidationError(detail="滑块验证码校验失败！")
        # 验证短信验证码
        redis = get_redis_connection("sms_code")
        code = redis.get(f'sms_{mobile}')
        if code is None:
            """获取不到验证码，则表示验证码已经过期了"""
            raise serializers.ValidationError(detail="验证码失效或已过期！", code="sms_code")
        # 从redis提取的数据，字符串都是bytes类型，所以decode
        if code.decode() != data.get("sms_code"):
            raise serializers.ValidationError(detail="短信验证码错误！", code="sms_code")
        redis.delete(f"sms_{mobile}")

        return data

    def create(self, validated_data):
        """保存用户信息，完成登录"""
        mobile = validated_data.get("val_mobile")

        user = User.objects.filter(mobile=mobile).get()

        # 注册成功以后，免登陆
        user.token = generate_jwt_token(user)

        return user


class UserRegisterModelSerializer(serializers.ModelSerializer):
    """
    用户注册的序列化器
    """
    re_password = serializers.CharField(required=True, write_only=True, help_text="确认密码")
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")
    token = serializers.CharField(read_only=True)
    # ticket = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的临时凭证")
    # randstr = serializers.CharField(required=True, write_only=True, help_text="滑块验证码的随机字符串")

    class Meta:
        model = User
        # fields = ["mobile", "password", "re_password", "sms_code", "token", "ticket", "randstr"]
        fields = ["mobile", "password", "re_password", "sms_code"]
        extra_kwargs = {
            "mobile": {
                "required": True, "write_only": True
            },
            "password": {
                "required": True, "write_only": True, "min_length": 6, "max_length": 16,
            },
        }

    def validate(self, data):
        """验证客户端数据"""
        # 手机号格式验证
        mobile = data.get("mobile", None)
        if not re.match("^1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError(detail="手机号格式不正确！", code="mobile")

        # 密码和确认密码
        password = data.get("password")
        re_password = data.get("re_password")
        if password != re_password:
            raise serializers.ValidationError(detail="密码和确认密码不一致！", code="password")

        # 手机号是否已注册
        try:
            User.objects.get(mobile=mobile)
            raise serializers.ValidationError(detail="手机号已注册！")
        except User.DoesNotExist:
            pass

        # # 验证防水墙验证码
        # api = TencentCloudAPI()
        # result = api.captcha(
        #     data.get("ticket"),
        #     data.get("randstr"),
        #     self.context['request']._request.META.get("REMOTE_ADDR"),  # 客户端IP
        # )
        #
        # if not result:
        #     raise serializers.ValidationError(detail="滑块验证码校验失败！")

        # 验证短信验证码
        redis = get_redis_connection("sms_code")
        code = redis.get(f'sms_{mobile}')
        if code is None:
            """获取不到验证码，则表示验证码已经过期了"""
            raise serializers.ValidationError(detail="验证码失效或已过期！", code="sms_code")
        # 从redis提取的数据，字符串都是bytes类型，所以decode
        if code.decode() != data.get("sms_code"):
            raise serializers.ValidationError(detail="短信验证码错误！", code="sms_code")
        redis.delete(f"sms_{mobile}")

        return data

    def create(self, validated_data):
        """保存用户信息，完成注册"""
        mobile = validated_data.get("mobile")
        password = validated_data.get("password")

        user = User.objects.create_user(
            username=mobile,
            mobile=mobile,
            avatar=constants.DEFAULT_USER_AVATAR,
            password=password,
        )

        # 注册成功以后，免登陆
        user.token = generate_jwt_token(user)

        return user
