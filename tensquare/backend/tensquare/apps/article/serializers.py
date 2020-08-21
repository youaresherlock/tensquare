from rest_framework import serializers

from article.models import Article, Channel, Comment
from article.search_indexes import ArticleIndex
from user.models import User
from drf_haystack.serializers import HaystackSerializer


class ArticleSerializerForCreate(serializers.ModelSerializer):
    image = serializers.CharField(required=False, default='',allow_blank=True)

    class Meta:
        model = Article
        exclude = ('collected_users',)


class ArticleSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ("id", "title")


class UserDetailSerializer(serializers.ModelSerializer):

    articles = ArticleSerializerSimple(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'username','avatar','articles','fans')


class CommentSerializerForCreate(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content','article','user','parent','createtime')


class CommentSerializerItem(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    subs = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ('id', 'content','article','user','parent','subs','createtime')


class CommentSerializerList(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    subs = CommentSerializerItem(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = "__all__"


class ArticleSerializerForDetail(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    comments = CommentSerializerList(read_only=True, many=True)

    class Meta:
        model = Article
        fields = "__all__"


class ArticleSerializerForList(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    collected = serializers.BooleanField(default=False)

    class Meta:
        model = Article
        fields = ("id", "title","content","createtime","user","collected_users","collected","image","visits")


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = ("id","name")


class ArticleIndexSerializer(HaystackSerializer):
    """
    Article索引结果数据序列化器
    """
    class Meta:
        index_classes = [ArticleIndex]
        fields = ('text', 'id', 'title', 'content', 'createtime')
