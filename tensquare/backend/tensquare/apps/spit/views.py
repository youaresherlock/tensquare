from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_mongoengine.viewsets import ModelViewSet

from spit.models import Spit
from spit.serializers import SpitSerializer


class SpitViewSet(ModelViewSet):
    queryset = Spit.objects.all()
    serializer_class = SpitSerializer

    # 因为可以匿名发表吐槽,因此禁用drf帮我们做的认证
    def perform_authentication(self, request):
        pass

    def retrieve(self, request, id):
        spit = self.get_object()
        spit.visits += 1
        spit.save()
        try:
            user = self.request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            flag_collect = redis_conn.hget("spit_collect_%s" % user.id, str(id))
            flag_thumbup = redis_conn.hget("spit_thumbup_%s" % user.id, str(id))
            if flag_collect:
                spit.collected = True
            if flag_thumbup:
                spit.hasthumbup = True

        s = self.get_serializer(instance=spit)
        return Response(s.data)

    # 获取所有一级吐槽 spit/
    def list(self, request):

        spitList = self.get_queryset().filter(parent=None).order_by("-publishtime")
        retSpitList = []

        try:
            user = self.request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            for spit in spitList:
                flag_collect = redis_conn.hget("spit_collect_%s" % user.id, str(spit.id))
                flag_thumbup = redis_conn.hget("spit_thumbup_%s" % user.id, str(spit.id))
                if flag_collect:
                    spit.collected = True
                if flag_thumbup:
                    spit.hasthumbup = True

                retSpitList.append(spit)
        else:
            retSpitList = spitList

        s = self.get_serializer(instance=retSpitList, many=True)
        return Response(s.data)

    # 获取吐槽的评论  spit/{pk}/children/
    @action(methods=["GET"], detail=True, url_path="children")
    def get_children(self, request, id):

        spitList = self.get_queryset().filter(parent=id).order_by("-publishtime")
        retSpitList = []

        try:
            user = self.request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            for spit in spitList:
                flag_collect = redis_conn.hget("spit_collect_%s" % user.id, str(spit.id))
                flag_thumbup = redis_conn.hget("spit_thumbup_%s" % user.id, str(spit.id))
                if flag_collect:
                    spit.collected = True
                if flag_thumbup:
                    spit.hasthumbup = True

                retSpitList.append(spit)
        else:
            retSpitList = spitList

        s = self.get_serializer(instance=retSpitList, many=True)
        return Response(s.data)

    # 点赞和取消点赞 spit/{id}/updatethumbup/
    @action(methods=["PUT"], detail=True, url_path="updatethumbup")
    def update_thumbup(self, request, id):
        try:
            user = request.user
        except Exception:
            user = None

        spit = self.get_object()

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            flag = redis_conn.hget("spit_thumbup_%s" %user.id, id)
            if flag:
                spit.thumbup -= 1
                spit.save()
                redis_conn.hdel('spit_thumbup_%s' % user.id, id)
                return Response({'success': True, 'message': '取消点赞成功'})
            else:
                redis_conn.hset("spit_thumbup_%s" % user.id, id, 1)
                spit.thumbup += 1
                spit.save()
                return Response({'success': True, 'message': '点赞成功'})
        else:
            return Response({'success': False, 'message': '未登录'},status=400)

    # 收藏和取消收藏 spit/{id}/collect/
    @action(methods=["PUT"], detail=True, url_path="collect")
    def collect(self, request, id):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('spit')
            flag = redis_conn.hget("spit_collect_%s" %user.id, id)
            if flag:
                redis_conn.hdel('spit_collect_%s' % user.id, id)
                return Response({'success': True, 'message': '取消收藏成功'})
            else:
                redis_conn.hset("spit_collect_%s" % user.id, id, 1)
                return Response({'success': True, 'message': '收藏成功'})
        else:
            return Response({'success': False, 'message': '未登录'},status=400)