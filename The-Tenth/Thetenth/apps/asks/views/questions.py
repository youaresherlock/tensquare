from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.asks.models import Question, Reply
from apps.asks.serializers.questions import QuestionLabelSerializer, QuestionSerializer, DetailQuestionSerializer, \
    ReplySerializer
from rest_framework.permissions import IsAuthenticated


class QuestionLabelsView(APIView):
    def get(self, request, id):
        """获取最新回答问题"""
        if id == "-1":
            queryset = Question.objects.all().order_by("-createtime")
        else:
            queryset = Question.objects.filter(id=id).order_by("-createtime")
        serializer = QuestionLabelSerializer(queryset, many=True)
        return Response(serializer.data)


class QuestionHotView(APIView):
    def get(self, request, id):
        """获取热门问题"""
        if id == "-1":
            queryset = Question.objects.all().order_by("-reply", "-visits")
        else:
            queryset = Question.objects.filter(labels_id=id).order_by("-reply", "-visits")
        serializer = QuestionLabelSerializer(queryset, many=True)
        return Response(serializer.data)


class QuestionWaitView(APIView):
    """
    获取用户等待回答的问题
    """
    def get(self, request, id):
        if id == "-1":
            queryset = Question.objects.filter(reply=0)
        else:
            queryset = Question.objects.filter(id=id, reply=0)
        serializer = QuestionLabelSerializer(queryset, many=True)
        return Response(serializer.data)


class PostQuestion(CreateAPIView):
    # 发布问题
    # 指定视图所使用的序列化器类
    serializer_class = QuestionSerializer
    # 指定视图所使用的查询集
    queryset = Question.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'ok', 'success': True}, status=status.HTTP_201_CREATED)


class QuestionDetail(GenericAPIView):
    serializer_class = DetailQuestionSerializer
    queryset = Question.objects.all()
    """问题详情"""

    def get(self, request, pk):
        question = self.get_object()
        question.visits += 1
        question.save()
        replies = question.replies.all()
        question.comment_question = []
        question.answer_question = []
        for item in replies:
            if item.type == 0:  # 问题的评论
                question.comment_question.append(item)
            elif item.type == 2:  # 回答的评论
                question.answer_question.append(item)
        # 指定视图所使用的序列化器类
        serializer_class = DetailQuestionSerializer(instance=question)
        return Response(serializer_class.data)


class QuestionUseful(GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Question.objects.all()

    """问题有用"""
    def put(self, request, pk):
        user = request.user
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


class QuestionUnuseful(GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Question.objects.all()

    """问题没用"""
    def put(self, request, pk):
        user = request.user
        redis_conn = get_redis_connection('question')
        flag = redis_conn.hget("question_userful_%s" % user.id, pk)
        if flag:
            return Response({'success': False, 'message': '请不要重复操作'})
        else:
            question = self.get_object()
            question.unuseful_count += 1
            question.save()
            redis_conn.hset("question_userful_%s" % user.id, pk, 1)
            return Response({'success': True, 'message': '更新成功'})


class QuestionReply(APIView):
    # 回答问题

    def post(self, request):
        try:
            user = request.user
        except Exception:
            user = None
        if user is not None and user.is_authenticated:
            data = request.data
            data['user'] = user.id
            # 反序列化-数据校验
            serializer = ReplySerializer(data=data)
            serializer.is_valid(raise_exception=True)

            # 反序列化-数据保存(save内部会调用序列化器类的create方法)
            reply = serializer.save()
            problem = reply.problem
            # 如果是回答,则更新对应的数据
            if data.get('type') == 2:
                problem.reply += 1
                problem.replyname = reply.user.username
                problem.replytime = reply.createtime
                problem.save()
            return Response({'success': True, 'message': '发表成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)


class ReplyUseful(GenericAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Reply.objects.all()
    """回答有用"""

    def put(self, request, pk):
        user = request.user
        redis_conn = get_redis_connection('Reply')
        flag = redis_conn.hget("Reply_userful_%s" % user.id, pk)
        if flag:
            return Response({'success': False, 'message': '请不要重复操作'})
        else:
            Reply = self.get_object()
            Reply.useful_count += 1
            Reply.save()
            redis_conn.hset("Reply_userful_%s" % user.id, pk, 1)
            return Response({'success': True, 'message': '更新成功'})


class ReplyUnuseful(GenericAPIView):
    permission_classes = [IsAuthenticated]
    """回答没用"""
    queryset = Reply.objects.all()

    def put(self, request, pk):
        user = request.user
        redis_conn = get_redis_connection('Reply')
        flag = redis_conn.hget("Reply_userful_%s" % user.id, pk)
        if flag:
            return Response({'success': False, 'message': '请不要重复操作'})
        else:
            Reply = self.get_object()
            Reply.unuseful_count += 1
            Reply.save()
            redis_conn.hset("Reply_userful_%s" % user.id, pk, 1)
            return Response({'success': True, 'message': '更新成功'})
