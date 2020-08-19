from django.http import Http404
from haystack.views import SearchView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.recruit.serializers.recruit import RecruitSerializer, RecruitDetailSerializer
from apps.recruit.models import Recruit
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated


class RecruitRecommendAPIView(GenericAPIView):
    """
    获取推荐职位
    """
    serializer_class = RecruitSerializer

    queryset = Recruit.objects.all()

    def get(self, request):

        recruits = self.get_queryset().order_by('-id')[:4]

        serializer = RecruitSerializer(recruits, many=True)

        return Response(serializer.data)


class RecruitLatestAPIView(GenericAPIView):
    """
    获取最新职位
    """
    serializer_class = RecruitSerializer

    queryset = Recruit.objects.all()

    def get(self, request):

        recruits = self.get_queryset().order_by('-createtime')[:4]

        serializer = RecruitSerializer(recruits, many=True)

        return Response(serializer.data)


class RecruitSearchAPIView(GenericAPIView):
    """
    进行职位搜索
    """
    serializer_class = RecruitSerializer

    def post(self, request):

        name = request.data.get('cityname')

        keyword = request.data.get('keyword')

        # 获取当前为1的岗位 并且按照时间发布最新查看
        jobs = Recruit.objects.filter(state="1").order_by("-createtime")

        # 创建职位列表
        res_jobs = []

        # 如果没有传入城市和关键字
        if not name and not keyword:
            res_jobs = jobs
        # 只传入城市
        elif name and not keyword:
            for job in jobs:
                if job.city == name:
                    res_jobs.append(job)
        # 只传入关键字
        elif not name and keyword:
            for job in jobs:
                if job.jobname.lower().find(keyword.lower()) != -1:
                    res_jobs.append(job)
        else:
            # 当两个参数都传入
            for job in jobs:
                # 只有工作对应的城市和工作关键字都对上 才是这个工作
                if job.city == name and job.jobname.lower().find(keyword.lower()) != -1:
                    res_jobs.append(job)

        serializer = RecruitSerializer(res_jobs, many=True)

        return Response(serializer.data)


# 获取职位详情
class RecruitDetailAPIView(GenericAPIView):
    """
    获取职位详情
    """

    serializer_class = RecruitDetailSerializer

    queryset = Recruit.objects.all()

    def get(self, request, pk):

        recruit = self.get_object()

        serializer = RecruitDetailSerializer(recruit)

        return Response(serializer.data)


# 增加职位访问次数
class RecruitAddAPIView(GenericAPIView):
    """
    增加职位访问次数
    """

    serializer_class = RecruitDetailSerializer

    queryset = Recruit.objects.all()

    def put(self, request, pk):

        recruit = self.get_object()

        recruit.visits += 1

        recruit.save()

        return Response({"message": "更新成功", "success": True})


# 收藏和取消收藏职位
class CollectRecruitAPIView(GenericAPIView):
    """
    收藏职位
    """
    permission_classes = [IsAuthenticated]

    serializer_class = RecruitDetailSerializer

    queryset = Recruit.objects.all()

    def post(self, request, pk):

        recruit = self.get_object()

        user = request.user

        recruit.users.add(user)

        recruit.save()

        return Response({"message": "收藏成功", "success": True})


# 收藏和取消收藏职位
class CollectRecruitAPIViews(GenericAPIView):
    """
    收藏职位
    """
    permission_classes = [IsAuthenticated]

    serializer_class = RecruitDetailSerializer

    queryset = Recruit.objects.all()

    def post(self, request, pk):

        recruit = self.get_object()

        user = request.user

        recruit.users.remove(user)

        recruit.save()

        return Response({"message": "取消收藏", "success": True})


class MySearchView(SearchView):
    """
    重写searchview类
    """

    def create_response(self):

        page = self.request.GET.get('page')

        # 获取搜索结果

        context = self.get_context()

        data_list = []

        for job in context['page'].object_list:

            data_list.append({
                'id': job.object.id,
                'jobname': job.object.jobname,
                'city': job.object.city
            })








