from rest_framework import serializers
from apps.users.models import User
import re
from django_redis import get_redis_connection
from rest_framework_jwt.settings import api_settings


# 创建注册序列化器类
class UserRegisterSerializer(serializers.ModelSerializer):
    """
    创建注册序列化器类
    """
    sms_code = serializers.CharField(label='短信验证码', max_length=6, write_only=True)

    token = serializers.CharField(label='token', read_only=True)

    avatar = serializers.CharField(label='头像地址', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'sms_code', 'avatar', 'token')
        # 添加补充限制
        extra_kwargs = {
            'mobile': {
                'required': True
            },
            'password': {
                'write_only': True
            },
            'avatar': {
                'read_only': True
            }
        }

    # 对数据进行补充校验
    def validate(self, attrs):
        # 获取手机号
        mobile = attrs.get('mobile')
        # 获取短信验证码
        sms_code = attrs.get('sms_code', None)
        # 获取密码
        password = attrs.get('password')
        # 获取用户名
        username = attrs.get('username')

        # 对手机号进行验证
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            raise serializers.ValidationError('手机号格式错误')

        # 对密码进行验证判断
        if not re.match(r'^[1-9A-Za-z._-]{6,18}$', password):
            raise serializers.ValidationError('密码必须在6到16位之间')

        # 对用户名进行补充验证
        if not re.match(r'^\w{6,16}$', username):
            raise serializers.ValidationError('用户名必须在6到16位之间')

        if sms_code:
            redis_conn = get_redis_connection('verify_code')

            server_sms_code = redis_conn.get('sms_%s' % mobile)

            if not server_sms_code:
                raise serializers.ValidationError('验证码已过期')

            if server_sms_code.decode() != sms_code:
                raise serializers.ValidationError('验证码不正确,请重新输入')

        else:
            raise serializers.ValidationError('缺少必传参数')

        return attrs

    # 重新创建用户的create函数
    def create(self, validated_data):
        del validated_data['sms_code']
        user = User.objects.create_user(**validated_data)

        password = validated_data.get('password')

        user.set_password(password)

        user.save()

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token
        return user


# 创建登录序列化器类
class LoginSerializer(serializers.ModelSerializer):
    """
    登录序列化器
    """

    token = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = User

        fields = ('id', 'username', 'password', 'mobile', 'token', 'avatar')

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'mobile': {
                'read_only': True
            },
            'avatar': {
                'read_only': True
            }
        }

    # 对数据进行补充校验
    def validate(self, attrs):
        mobile = attrs.get('username')

        password = attrs.get('password')

        try:
            user = User.objects.get(mobile=mobile)

        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或者密码错误,请重试')
        else:
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或者密码错误,请重试')

        attrs['user'] = user

        return attrs

    # 然后实现登录
    def create(self, validated_data):
        user = validated_data.get('user')
        # JWT 认证
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user


