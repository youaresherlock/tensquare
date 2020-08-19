from datetime import datetime
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.activity.models import Gathering
from apps.activity.serializers import GatheringsListSerializer, GatherSerializer


class GatheringListView(ListAPIView):
    '''获取活动列表'''
    queryset = Gathering.objects.filter(state=1)
    serializer_class = GatheringsListSerializer


class GatherView(RetrieveAPIView):
    '''活动详情'''
    serializer_class = GatherSerializer
    queryset = Gathering.objects.filter(state=1)


class GatherJoinView(GenericAPIView):
    '''报名活动'''
    queryset = Gathering.objects.filter(state=1)
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        gathering = self.get_object()
        now = datetime.now()
        endtime = gathering.endrolltime.replace(tzinfo=None)
        if endtime < now:
            return Response({'success': False, 'message': '报名时间已过'}, status=400)
        else:
            if user in gathering.users.all():
                gathering.users.remove(user)
                gathering.save()
                return Response({'success': True, 'message': '取消成功'})
            else:
                gathering.users.add(user)
                gathering.save()
                return Response({'success': True, 'message': '参加成功'})
