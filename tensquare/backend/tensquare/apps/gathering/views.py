from datetime import datetime


# Create your views here.
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gathering.models import Gathering
from gathering.serializers import GatherSerializer, GatherSerializerSimple

# gatherings/ 获取所有活动
class GathersView(ListAPIView):
    serializer_class = GatherSerializerSimple
    queryset = Gathering.objects.filter(state=1)

# gatherings/{pk}/ 获取某个活动详情
class GatherView(RetrieveAPIView):
    serializer_class = GatherSerializer
    queryset = Gathering.objects.filter(state=1)

# gatherings/{pk}/join/ 参加或者取消某个活动
class GatherJoinView(GenericAPIView):
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
                return Response({'success':True,'message':'参加成功'})
