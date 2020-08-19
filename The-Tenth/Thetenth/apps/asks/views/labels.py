from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.asks.models import Label
from apps.asks.serializers.labels import LablesSerializer, LabelRRetrieveSerializers


class LablesView(GenericAPIView):

    # 指定序列化器
    serializer_class = LablesSerializer
    # 执行查询机
    queryset = Label.objects.all()

    def get(self, request):
        """获取所有标签列表"""
        # 获取查询集合
        queryset = self.get_queryset()
        # 序列化
        serializer = LablesSerializer(queryset, many=True)
        return Response(serializer.data)


class LablesUserView(GenericAPIView):
    """
    获取当前用户关注的标签
    """

    serializer_class = LablesSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = Label.objects.filter(users=user)

        return queryset

    def get(self, request):
        """获取用户关注的标签"""
        queryset = self.get_queryset()
        serializer = LablesSerializer(queryset, many=True)
        return Response(serializer.data)


class LabelDetailView(GenericAPIView):
    """
    获取标签详情
    """
    serializer_class = LabelRRetrieveSerializers

    queryset = Label.objects.all()

    def get(self, request, pk):

        label = self.get_object()

        serializer = LabelRRetrieveSerializers(label)

        return Response(serializer.data)


class FocusinLabelView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Label.objects.all()

    def put(self, request, pk):
        user = request.user
        label = self.get_object()
        label.users.add(user)
        label.save()
        return Response({'success': True, 'message': '关注成功'})


class FocusoutLabelView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Label.objects.all()

    def put(self, request, pk):
        user = request.user
        label = self.get_object()

        label.users.remove(user)
        label.save()
        return Response({'success': True, 'message': '取消关注成功'})


class LabelFullView(GenericAPIView):

    queryset = Label.objects.all()

    serializer_class = LablesSerializer

    def get(self, request):

        labels = self.get_queryset()

        serializer = LabelRRetrieveSerializers(labels, many=True)

        return Response(serializer.data)

