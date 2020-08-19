import re

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import User
from apps.users.serializers.userinfo import UserInfoSerializer


# 创建视图集 获取用户详情
class UserInfoView(GenericAPIView):
    """
    用户个人详情
    """
    permission_classes = [IsAuthenticated]

    # 指定视图所使用的序列化器类
    serializer_class = UserInfoSerializer

    # 获取用户信息
    def get(self, request):
        # 获取当前登录用户
        instance = request.user

        # 对用户数据进行序列化
        serializer = self.get_serializer(instance)

        # 返回当前用户数据
        return Response(serializer.data)

    # 修改用户信息
    def put(self, request):

        # 获取当前登录用户
        instance = request.user

        # 对当前用户数据进行反序列化进行校验
        serializer = UserInfoSerializer(instance, data=request.data)

        serializer.is_valid(raise_exception=True)

        # 反序列化进行数据保存
        serializer.save()

        return Response(serializer.data)


# 创建修改用户密码的视图
class ChangePasswordView(APIView):
    """
    修改用户密码
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        """
        对用户密码进行修改
        :param request:
        :return:
        """
        password = request.data.get('password')

        if not re.match(r'^[A-Za-z1-9._-]{6,16}$', password):
            raise APIException('参数密码错误')

        request.user.set_password(password)
        request.user.save()

        return Response(status=status.HTTP_200_OK)


# 创建用户关注方面视图
class UserLikeView(GenericAPIView):
    """
    创建用户 关注 取消关注的视图
    """
    permission_classes = [IsAuthenticated]
    
    # 指定序列化器
    serializer_class = UserInfoSerializer
    
    # 指定视图集
    queryset = User.objects.all()

    def post(self, request, pk):
        """
        添加关注
        :param request: 
        :param pk: 
        :return: 
        """
        user = self.get_object()

        user.fans.add(request.user.id)

        user.save()

        return Response({'success': True, 'message': '添加关注成功'})

    def delete(self, request, pk):
        """
        取消关注
        :param request: 
        :param pk: 
        :return: 
        """
        
        user = self.get_object()

        user.fans.remove(request.user.id)

        user.save()

        return Response({'success': True, 'message': '已取消关注'})


class UserLabelView(APIView):
    """
    获取个人登录标签的视图
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):

        labels = request.data.get('labels')

        request.user.labels.clear()

        for i in labels:
            request.user.labels.add(i)

        return Response({})


