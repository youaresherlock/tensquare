from rest_framework import serializers
from apps.recruit.models import Enterprise, Recruit


class EnterpriseSerializer(serializers.ModelSerializer):
    """
    获取企业信息
    """
    recruits = serializers.PrimaryKeyRelatedField(label='企业', read_only=True, many=True)

    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'logo', 'recruits', 'summary')


class RecruitSerializer(serializers.ModelSerializer):
    """
    获取推荐职位
    """
    enterprise = EnterpriseSerializer(label='简单企业数据')

    class Meta:
        model = Recruit

        fields = (
            'id', 'jobname', 'salary', 'condition', 'education', 'type', 'city', 'createtime', 'enterprise', 'labels')


# 新建企业详情序列化器
class EnterpriseDetailSerializer(serializers.ModelSerializer):
    """
    获取企业详情序列化器
    """
    users = serializers.PrimaryKeyRelatedField(label='用户名', many=True, read_only=True)

    recruits = RecruitSerializer(label='职位简单数据', many=True)

    class Meta:
        model = Enterprise
        fields = "__all__"


# 新建职位详情序列化器类
class RecruitDetailSerializer(serializers.ModelSerializer):
    """
    获取职位详情
    """

    users = serializers.PrimaryKeyRelatedField(label='用户名', many=True, read_only=True)

    enterprise = EnterpriseDetailSerializer(label='企业详情')

    class Meta:
        model = Recruit

        fields = "__all__"


