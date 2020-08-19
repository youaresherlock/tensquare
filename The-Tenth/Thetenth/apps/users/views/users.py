from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from apps.users.serializers.users import UserRegisterSerializer, LoginSerializer
from rest_framework.response import Response
from apps.users.models import User


class RegisterUserView(APIView):
    """
    用户注册
    """
    def post(self, request):
        # 1. 获取参数进行反序列化校验
        serializer = UserRegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # 2. 服务器需要生成JWTtoken
        serializer.save()  # 调用create方法

        # 3. 返回相应数据 登录成功
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserView(CreateAPIView):
    """
    登录视图
    """
    serializer_class = LoginSerializer
    queryset = User.objects.all().order_by('pk')