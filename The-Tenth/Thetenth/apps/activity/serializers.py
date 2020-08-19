from django.db import models
from rest_framework import serializers
from apps.activity.models import Gathering


class GatheringsListSerializer(serializers.ModelSerializer):
    '''活动列表序列化器类'''

    id = serializers.IntegerField(label='活动ID')

    class Meta:
        model = Gathering
        fields = ('id', 'name', 'image', 'city', 'starttime', 'endtime', 'endrolltime', 'users')


class GatherSerializer(serializers.ModelSerializer):
    '''获取活动详情'''

    class Meta:
        model = Gathering
        fields = "__all__"


class GatheringsDetailsSerializer(serializers.ModelSerializer):
    '''活动列表序列化器类'''
    id = serializers.IntegerField(label='活动ID')
    gathering = models.ForeignKey(Gathering,
                                  on_delete=models.CASCADE,
                                  verbose_name='活动行')

    class Meta:
        model = Gathering
        fields = ('name', 'summary', 'detail', 'address', 'sponsor', 'image', 'city', 'state', 'starttime', 'endtime',
                  'endrolltime', 'users')
