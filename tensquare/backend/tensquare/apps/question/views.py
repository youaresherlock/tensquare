from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from question.models import Label, Question, Reply
from question.serializers import LabelSerializerSimple, QuestionSerializerForList, QuestionSerializerForCreate, ReplySerializerForCreate, LabelSerializer, LabelSerializerWithQuestionAndArticle, QuestionSerializerForDetail


class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()

    # 发表一个问题  questions/
    def create(self, request, *args, **kwargs):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            request_data = request.data
            request_data["user"] = user.id
            s = QuestionSerializerForCreate(data=request_data)
            s.is_valid(raise_exception=True)
            s.save()
            return Response({'success': True, 'message': '发表成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    # 查询问题详情 questions/{pk}/
    def retrieve(self, request, pk):
        question = self.get_object()
        question.visits += 1
        question.save()
        replies = question.replies.all()
        question.comment_question = []
        question.answer_question = []

        for item in replies:
            if item.type == 0: # 问题的评论
                question.comment_question.append(item)
            elif item.type == 2: # 回答的评论
                question.answer_question.append(item)

        s = QuestionSerializerForDetail(instance=question)
        return Response(s.data)

    # 更新有用数量 questions/{pk}/useful/
    @action(methods=['put'], detail=True)
    def useful(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('question')
            flag = redis_conn.hget("question_userful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            else:
                question = self.get_object()
                question.useful_count += 1
                question.save()
                redis_conn.hset("question_userful_%s" % user.id, pk, 1)
                return Response({'success': True, 'message': '更新成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    # 更新无用数量 questions/{pk}/unuseful/
    @action(methods=['put'], detail=True)
    def unuseful(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('question')
            flag = redis_conn.hget("question_unuserful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            else:
                question = self.get_object()
                question.unuseful_count += 1
                question.save()
                redis_conn.hset("question_unuserful_%s" % user.id, pk, 1)
                return Response({'success': True, 'message': '更新成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    # /questions/{pk}/label/new/ 查询labelid为pk的所有问题,按照回复的时间进行降序
    @action(methods=["GET"], detail=True, url_path="label/new")
    def get_new_question_by_labelid(self, request, pk):
        if pk == "-1":
            questions = Question.objects.all().order_by("-replytime")
        else:
            label = Label.objects.get(id=pk)
            questions = label.questions.all().order_by("-replytime")
        s = QuestionSerializerForList(instance=questions, many=True)
        return Response(s.data)

    # /questions/{pk}/label/hot/ 查询labelid为pk的所有问题,按照回复的数量进行降序
    @action(methods=["GET"], detail=True, url_path="label/hot")
    def get_hot_question_by_labelid(self, request, pk):
        if pk == "-1":
            questions = Question.objects.all().order_by("-reply")
        else:
            label = Label.objects.get(id=pk)
            questions = label.questions.all().order_by("-reply")
        s = QuestionSerializerForList(instance=questions, many=True)
        return Response(s.data)

    # /questions/{pk}/label/wait/ 查询labelid为pk未解答的问题,按照问题创建的时间降序
    @action(methods=["GET"], detail=True, url_path="label/wait")
    def get_wait_question_by_labelid(self, request, pk):
        if pk == "-1":
            questions = Question.objects.all()
        else:
            label = Label.objects.get(id=pk)
            questions = label.questions.all()
        questions = questions.filter(reply=0).order_by("-createtime")
        s = QuestionSerializerForList(instance=questions, many=True)
        return Response(s.data)


class ReplyViewSet(ModelViewSet):
    queryset = Reply.objects.all()

    # 创建新的评论 reply/
    def create(self, request,*args, **kwargs):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            request_data = request.data
            request_data["user"] = user.id
            s = ReplySerializerForCreate(data=request_data)
            s.is_valid(raise_exception=True)
            reply = s.save()
            problem = reply.problem
            # 如果是回答,则更新对应的数据
            if request_data.get('type') == 2:
                problem.reply += 1
                problem.replyname = reply.user.username
                problem.replytime = reply.createtime;
                problem.save()
            return Response({'success': True, 'message': '发表成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    # 更新有用数量 reply/{pk}/useful/
    @action(methods=['put'], detail=True)
    def useful(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            redis_conn = get_redis_connection('reply')
            flag = redis_conn.hget("reply_userful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            else:
                replyitem = self.get_object()
                replyitem.useful_count += 1
                replyitem.save()
                redis_conn.hset("reply_userful_%s" % user.id, pk, 1)
                return Response({'success': True, 'message': '更新成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    # 更新没用数量 reply/{pk}/unuseful/
    @action(methods=['put'], detail=True)
    def unuseful(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:

            redis_conn = get_redis_connection('reply')
            flag = redis_conn.hget("reply_unuserful_%s" % user.id, pk)
            if flag:
                return Response({'success': False, 'message': '请不要重复操作'})
            else:
                replyitem = self.get_object()
                replyitem.unuseful_count += 1
                replyitem.save()
                redis_conn.hset("reply_unuserful_%s" % user.id, pk, 1)
                return Response({'success': True, 'message': '更新成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)


class LabelsViewSet(ModelViewSet):
    queryset = Label.objects.all()

    # labels/{pk}/  获取某个标签详情
    def retrieve(self, request, pk):
        label = self.get_object()
        s = LabelSerializerWithQuestionAndArticle(instance=label)
        return Response(s.data)

    # labels/  获取标签基本信息列表
    def list(self, request):
        labels = self.get_queryset()
        s = LabelSerializerSimple(instance=labels, many=True)
        return Response(s.data)

    # labels/users/  获取用户关注的标签基本信息列表
    @action(methods=['get'], detail=False)
    def users(self, request):
        try:
            user = self.request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            labels = user.labels.all()
            s = LabelSerializerSimple(instance=labels, many=True)
            return Response(s.data)
        else:
            return Response([])

    # labels/full/  获取标签详细信息列表
    @action(methods=['get'], detail=False)
    def full(self, request):
        labels = self.get_queryset()
        s = LabelSerializer(instance=labels, many=True)
        return Response(s.data)

    # labels/{pk}/focus/  关注标签
    @action(methods=['put'], detail=True)
    def focusin(self, request, pk):
        try:
            user = self.request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            label = self.get_object()
            if user not in label.users.all():
                label.users.add(user)
                label.save()
                return Response({'success': True, 'message': '关注成功'})
            else:
                return Response({'success': True, 'message': '已经关注了...'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    # labels/{pk}/focusout/  取消关注标签
    @action(methods=['put'], detail=True)
    def focusout(self, request, pk):
        try:
            user = self.request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            label = self.get_object()
            if user in label.users.all():
                label.users.remove(user)
                label.save()
                return Response({'success': True, 'message': '取消关注成功'})
            else:
                return Response({'success': True, 'message': '已经取消关注了...'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)
