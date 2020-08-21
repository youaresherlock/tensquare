from rest_framework import serializers

from article.serializers import ArticleSerializerForList
from question.models import Label, Reply, Question
from user.models import User


class ReplySerializerForCreate(serializers.ModelSerializer):

    class Meta:
        model = Reply
        fields = '__all__'


class UserSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class ReplySerializerForSubAndParent(serializers.ModelSerializer):

    user = UserSerializerSimple(read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content","createtime","useful_count","unuseful_count","user"]


class ReplySerializerForList(serializers.ModelSerializer):

    user = UserSerializerSimple(read_only=True)
    subs = ReplySerializerForSubAndParent(read_only=True, many=True)
    parent = ReplySerializerForSubAndParent(read_only=True)

    class Meta:
        model = Reply
        fields = ["id", "content","createtime","useful_count",'problem',"unuseful_count","subs","user","parent"]


class QuestionSerializerForList(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True,many=True)

    class Meta:
        model = Question
        fields = ["id","createtime","labels","reply","replyname","replytime","title","unuseful_count","useful_count","user","visits"]


class QuestionSerializerForDetail(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    labels = serializers.StringRelatedField(read_only=True, many=True)
    # replies = ReplySerializerForList(read_only=True, many=True)
    comment_question = ReplySerializerForList(read_only=True, many=True)
    comment_reply = ReplySerializerForList(read_only=True, many=True)
    answer_question = ReplySerializerForList(read_only=True, many=True)

    class Meta:
        model = Question
        fields = ["id","createtime","labels","reply","replyname","replytime","title","unuseful_count","useful_count","user","visits","content","comment_question","comment_reply","answer_question"]


class QuestionSerializerForCreate(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"


class LabelSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "label_name"]


class LabelSerializerWithQuestionAndArticle(serializers.ModelSerializer):
    questions = QuestionSerializerForList(many=True, read_only=True)
    articles = ArticleSerializerForList(many=True, read_only=True)

    class Meta:
        model = Label
        fields = "__all__"
