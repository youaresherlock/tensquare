from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from user import serializers
from user.models import User, OAuthWeixinUser
from user.utils import OAuthWeixin


class UserCreateView(CreateAPIView):
    """
    用户注册
    """
    serializer_class = serializers.CreateUserSerializer


class UserPwdView(UpdateAPIView):
    """
    用户修改密碼
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserPwdSerializer

    def get_object(self):
        return self.request.user


class UserLabelView(UpdateAPIView):
    """
    用户修改擅长技术
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserLabelSerializer

    def get_object(self):
        return self.request.user


class UserDetailView(RetrieveUpdateAPIView):
    """
    用户详细信息
    """
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]  # 指明必须登录认证后才能访问

    def get_object(self):
        user = self.request.user
        replies = user.replies.all()
        user.answer_question = []
        for item in replies:
            if item.type == 2: # 回答的评论
                user.answer_question.append(item)
        return user




class UserLikeView(APIView):
    """
    关注 取消关注
    """
    permission_classes = [IsAuthenticated]  # 指明必须登录认证后才能访问

    # 当前用户关注userid
    def post(self, request, userid):
        user = self.request.user
        idol = User.objects.get(id=userid)
        if idol in user.idols.all():
            return Response({"success": False, "message": "请不要重复关注"}, status=400)
        user.idols.add(idol)
        user.save()
        return Response({"success": True, "message": "关注成功"})

    # 当前用户取消关注userid
    def delete(self, request, userid):
        user = self.request.user
        idol = User.objects.get(id=userid)
        if idol not in user.idols.all():
            return Response({"success": False, "message": "请不要重复取消关注"}, status=400)
        user.idols.remove(idol)
        user.save()
        return Response({"success": True, "message": "取消关注成功"})


class WeixinAuthUserView(APIView):
    """
    微信认证
    """
    def get(self, request):
        # 获取code
        code = request.query_params.get('code')

        if not code:
            return Response({'success':False,'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        oauth_weixin = OAuthWeixin()
        try:
            # 凭借code 获取access_token
            access_token, open_id = oauth_weixin.get_access_token(code)
            # 凭借access_token获取 openid
            open_id, username, avatar = oauth_weixin.get_weixin_user_info(access_token, open_id)
        except:
            return Response({'success':False,'message': '访问weixin接口异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 根据openid查询数据库OAuthQQUser  判断数据是否存在
        try:
            oauth_qq_user = OAuthWeixinUser.objects.get(openid=open_id)
        except OAuthWeixinUser.DoesNotExist:
            # 如果数据不存在，注册新用户并返回
            user = User.objects.create_user(username=username, mobile=username, password='11111111', avatar=avatar)
            oauth_qq_user = OAuthWeixinUser.objects.create(user=user, openid=open_id)

        # 如果数据存在，表示用户已经绑定过身份， 签发JWT token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = oauth_qq_user.user
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'id': user.id,
            'mobile': user.mobile,
            'username': user.username,
            'avatar': user.avatar
        })
        return response

