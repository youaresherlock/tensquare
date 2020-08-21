import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from article.serializers import ArticleSerializerForList
from question.models import Label
from question.serializers import LabelSerializerSimple, QuestionSerializerForList, ReplySerializerForList
from recruit.serializer import EnterpriseSerializerSimple
from user.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """创建用户的序列化器"""
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    token = serializers.CharField(label='JWT token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'sms_code', 'mobile', 'token','avatar')
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """验证手机号"""
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value



    def validate(self, data):
        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = data['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if real_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')
        if data['sms_code'] != real_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')

        return data

    def create(self, validated_data):
        """重写保存方法，增加密码加密"""

        # 移除数据库模型类中不存在的属性
        del validated_data['sms_code']

        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # 签发jwt token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详细信息序列化器
    """
    labels = LabelSerializerSimple(required=False, many=True)
    username = serializers.CharField(read_only=True)
    questions = QuestionSerializerForList(read_only=True, many=True)
    answer_question = ReplySerializerForList(read_only=True, many=True)
    collected_articles = ArticleSerializerForList(read_only=True, many=True)
    enterpises = EnterpriseSerializerSimple(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile','realname','birthday','sex','avatar','website','email','city', 'address','labels','questions','answer_question','collected_articles','enterpises')


class UserLabelSerializer(serializers.ModelSerializer):
    """
    用户修改擅长技术 的序列化器
    """
    labels = serializers.PrimaryKeyRelatedField(required=True, many=True,queryset=Label.objects.all())

    class Meta:
        model = User
        fields = ('id','labels')


class UserPwdSerializer(serializers.ModelSerializer):
    """
    用户详修改密码序列化器
    """
    class Meta:
        model = User
        fields = ('password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user