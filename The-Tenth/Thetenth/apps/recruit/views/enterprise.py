from rest_framework.permissions import IsAuthenticated

from apps.recruit.serializers.recruit import EnterpriseSerializer, EnterpriseDetailSerializer
from apps.recruit.models import Enterprise
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class EnterpriseHotAPIView(GenericAPIView):
    """
    获取热门企业
    """

    serializer_class = EnterpriseSerializer

    queryset = Enterprise.objects.all()



    def get(self, request):

        enterprises = self.get_queryset().order_by('-visits')[:6]

        serializer = EnterpriseSerializer(enterprises, many=True)

        return Response(serializer.data)


class EnterpriseDetailAPIView(GenericAPIView):
    """
    获取企业详情
    """

    serializer_class = EnterpriseDetailSerializer

    queryset = Enterprise.objects.all()



    def get(self, request, pk):

        enterprise = self.get_object()

        serializer = EnterpriseDetailSerializer(enterprise)

        return Response(serializer.data)


class EnterpriseVisitAPIView(GenericAPIView):
    """
    增加企业访问次数
    """
    serializer_class = EnterpriseDetailSerializer

    queryset = Enterprise.objects.all()



    def put(self, request, pk):

        enterprise = self.get_object()

        enterprise.visits += 1

        enterprise.save()

        return Response({"message": "更新成功", "success": True})


class CollectEnterpriseAPIView(GenericAPIView):
    """
    收藏职位
    """
    permission_classes = [IsAuthenticated]

    serializer_class = EnterpriseDetailSerializer

    queryset = Enterprise.objects.all()



    def post(self, request, pk):

        enterprise = self.get_object()

        user = request.user

        enterprise.users.add(user)

        enterprise.save()

        return Response({"message": "收藏成功", "success": True})


class CollectEnterpriseAPIViews(GenericAPIView):
    """
    收藏职位
    """
    permission_classes = [IsAuthenticated]

    serializer_class = EnterpriseDetailSerializer

    queryset = Enterprise.objects.all()



    def post(self, request, pk):

        enterprise = self.get_object()

        user = request.user

        enterprise.users.remove(user)

        enterprise.save()

        return Response({"message": "取消收藏", "success": True})