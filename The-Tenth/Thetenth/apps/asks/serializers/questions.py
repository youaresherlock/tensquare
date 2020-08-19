from rest_framework import serializers
from apps.asks.models import Label, Question, Reply
from apps.users.models import User


class LabelIDSerializer(serializers.ModelSerializer):
    """
    简单标签id
    """

    class Meta:
        model = Label

        fields = ('id', 'label_name')


class QuestionLabelSerializer(serializers.ModelSerializer):
    """获取最新, 热门, 等待回答问题"""
    labels = serializers.StringRelatedField(label="标签", many=True)

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Question
        exclude = ("solve", "thumbup", "content", "updatetime")


class QuestionSerializer(serializers.ModelSerializer):
    """
    获取和发布问题
    """

    class Meta:
        model = Question
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    # 回答问题的序列化器
    class Meta:
        model = Reply
        fields = '__all__'


class UserSerializerSimple(serializers.ModelSerializer):
    """
    获取简单用户
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class ReplySerializerForSubAndParent(serializers.ModelSerializer):
    """
    获取简单问题回答
    """

    user = UserSerializerSimple(read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content", "createtime", "useful_count", "unuseful_count", "user"]


class ReplySerializerForList(serializers.ModelSerializer):
    """
    问题评论列表
    """

    user = UserSerializerSimple(read_only=True)
    subs = ReplySerializerForSubAndParent(read_only=True, many=True)
    parent = ReplySerializerForSubAndParent(read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content", "createtime", "useful_count", 'problem', "unuseful_count", "subs", "user", "parent"]


class DetailQuestionSerializer(serializers.ModelSerializer):
    """
    问题详情序列化器
    """
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True, many=True)
    comment_question = ReplySerializerForList(read_only=True, many=True)
    comment_reply = ReplySerializerForList(read_only=True, many=True)
    answer_question = ReplySerializerForList(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ["id", "createtime", "labels", "reply", "replyname", "replytime", "title", "unuseful_count",
                  "useful_count", "user", "visits", "content", "comment_question", "comment_reply", "answer_question"]


