from rest_framework import serializers
from apps.article.models import Article
from apps.asks.models import Label, Question
from apps.users.models import User


class LablesSerializer(serializers.ModelSerializer):
    """获取所有标签列表"""

    class Meta:
        model = Label
        fields = ("id", "label_name")


class ArticleSerializerMin(serializers.ModelSerializer):
    """
    用户文章简单序列化器类
    """
    class Meta:
        model = Article
        fields = ('id', 'title')


class UserSerializers(serializers.ModelSerializer):
    """
    用户简单详情序列化器
    """
    fans = serializers.PrimaryKeyRelatedField(label="用户粉丝或者偶像", many=True, read_only=True)

    articles = ArticleSerializerMin(many=True)

    class Meta:
        model = User

        fields = ('id', 'username', 'avatar', 'fans', 'articles')


class ArticleSerializers(serializers.ModelSerializer):
    """
    文章简单详情序列化器
    """
    collected_users = serializers.PrimaryKeyRelatedField(label="文章关联用户id", many=True, read_only=True)

    user = UserSerializers(read_only=True)

    collected = serializers.BooleanField(default=False)

    class Meta:
        """"""
        model = Article
        fields = ['id', 'title', 'content', 'createtime', 'user', 'collected', 'image', 'visits', 'collected_users']


class QuestionSerializers(serializers.ModelSerializer):
    """
    问题序列化器
    """
    user = serializers.StringRelatedField(read_only=True)

    labels = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Question

        fields = "__all__"


class LabelRRetrieveSerializers(serializers.ModelSerializer):
    """标签详情序列化器类"""

    questions = QuestionSerializers(many=True, read_only=True)
    articles = ArticleSerializers(many=True, read_only=True)

    class Meta:
        model = Label
        fields = "__all__"
