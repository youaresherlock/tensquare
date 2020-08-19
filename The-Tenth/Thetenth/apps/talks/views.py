from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.talks.models import Spit
from apps.talks.serializers import SpitSerializer
from django_redis import get_redis_connection


class SpitView(ListCreateAPIView):
    """获取吐槽列表, 发布吐槽"""
    # 指定序列化器类
    serializer_class = SpitSerializer

    # 指定当前视图的认证方案，不再使用全局认证方案
    authentication_classes = [SessionAuthentication]

    pagination_class = None

    # 重写get_queryset方法
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            # 用户未登录
            querysets = Spit.objects.all()
            for queryset in querysets:
                # 将点赞和收藏状态指定为空
                queryset.collected = False
                queryset.hasthumbup = False
                queryset.save()
            return querysets
        redis_conn = get_redis_connection('spit')
        queryset_li = Spit.objects.all()
        for queryset in queryset_li:
            spit_id = queryset.id
            # 获取点赞和收藏状态信息
            collected = redis_conn.hget('%s_%s' % (self.request.user.id, spit_id), 'collected')
            humbup = redis_conn.hget('%s_%s' % (self.request.user.id, spit_id), 'humbup')
            if collected:
                queryset.collected = True
            if humbup:
                queryset.hasthumbup = True
        return queryset_li


class SpitDetailView(APIView):
    """获取吐槽详情"""
    authentication_classes = [SessionAuthentication]

    def get(self, request, pk):
        spit = Spit.objects.get(pk=pk)
        # 从redis中获取点赞, 收藏状态
        conn = get_redis_connection('spit')
        collected = conn.hget('%s_%s' % (self.request.user.id, pk), 'collected')
        humbup = conn.hget('%s_%s' % (self.request.user.id, pk), 'humbup')
        if collected:
            spit.collected = True
        if humbup:
            spit.hasthumbup = True
        # 获取评论量
        comments = Spit.objects.filter(parent=pk).count()
        spit.comment = comments
        ser = SpitSerializer(spit)
        return Response(ser.data)


class SpitListView(APIView):
    """获取吐槽详情评论列表"""

    authentication_classes = [SessionAuthentication]

    def get(self, request, pk):
        spits = Spit.objects.filter(parent=pk)
        for spit in spits:
            conn = get_redis_connection('spit')
            collected = conn.hget('%s_%s' % (self.request.user.id, pk), 'collected')
            humbup = conn.hget('%s_%s' % (self.request.user.id, pk), 'humbup')
            if collected:
                spit.collected = True
            if humbup:
                spit.hasthumbup = True

        ser = SpitSerializer(spits, many=True)
        return Response(ser.data)


class SpitCollectView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        spit = Spit.objects.get(id=pk)
        conn = get_redis_connection('spit')
        # 从redis中获取收藏状态
        collected = conn.hget('%s_%s' % (request.user.id, pk), 'collected')
        if collected:
            # 说明已经被收藏
            # 此时的操作为取消收藏, 删除redis中数据
            conn.delete('%s_%s' % (request.user.id, pk), 'collected')
            # 访问量-1
            spit.visits -= 1
            spit.save()
            return Response({
                'message': '取消收藏成功',
                'success': True
            })
        else:
            # 未被收藏, 此时操作为收藏操作
            conn.hset('%s_%s' % (request.user.id, pk), 'collected', 1)
            spit.visits += 1
            spit.save()
            return Response({
                'message': '收藏成功',
                'success': True
            })


class SpitUpdatethumbupView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        spit = Spit.objects.get(pk=pk)
        conn = get_redis_connection('spit')
        humbup = conn.hget('%s_%s' % (request.user.id, pk), 'humbup')
        if humbup:
            conn.delete('%s_%s' % (request.user.id, pk), 'humbup')
            spit.thumbup -= 1
            spit.save()
            return Response({
                'message': '取消点赞成功',
                'success': True
            })
        else:
            conn.hset('%s_%s' % (request.user.id, pk), 'humbup', 1)
            spit.thumbup += 1
            spit.save()
            return Response({
                'message': '点赞成功',
                'success': True
            })
