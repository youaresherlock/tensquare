from apps.users.models import User
from django.utils import timezone
from apps.article.models import Channel
from apps.article.models import Article
from apps.article.models import Comment
from rest_framework import serializers
from apps.article.search_indexes import ArticleIndex
from drf_haystack.serializers import HaystackSerializer


class ArticleIndexSerializer(HaystackSerializer):
    """
    Article索引结果数据序列化器
    """
    class Meta:
        index_classes = [ArticleIndex]
        fields = ('text', 'id', 'title', 'content', 'createtime')


class ChannelsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = '__all__'


class CreateArticleSerializer(serializers.ModelSerializer):
    """发布文章"""
    articleid = serializers.IntegerField(read_only=True, source='id')
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Article
        fields = ('articleid', 'content', 'labels', 'title', 'channel', 'image', 'user_id')
        extra_kwargs = {
            'content': {
                'write_only': True
            },
            'title': {
                'write_only': True
            },
            'image': {
                'write_only': True,
                'allow_blank': True
            }
        }


class ArticlesFromUserSerializer(serializers.ModelSerializer):
    """文章列表中 用户信息的 发布文章信息"""
    class Meta:
        model = Article
        fields = ('id', 'title')
        extra_kwargs = {
            'title': {
                'read_only': True
            }
        }


class AutherSimpleSerializer(serializers.ModelSerializer):
    """文章列表中 发布者信息"""
    articles = ArticlesFromUserSerializer(read_only=True, many=True)
    fans = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar', 'articles', 'fans')
        extra_kwargs = {
            'username': {
                'read_only': True
            },
            'avatar': {
                'read_only': True
            }
        }

    def get_fans(self, obj):
        fans = User.objects.filter(idols=obj)
        return AutherSimpleSerializer(fans, many=True).data


class SubsSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    subs = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = '__all__'


class CommentsForArticleSerializer(serializers.ModelSerializer):
    user = AutherSimpleSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    subs = SubsSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ArticleListSerializer(serializers.ModelSerializer):
    user = AutherSimpleSerializer(read_only=True)
    collected = serializers.BooleanField(default=False)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'createtime', 'user',
                  'collected_users', 'collected', 'image')
        extra_kwargs = {
            'title': {
                'read_only': True
            },
            'content': {
                'read_only': True
            },
            'createtime': {
                'read_only': True
            },
            'collected_users': {
                'read_only': True
            },
            'image': {
                'read_only': True
            }
        }


class ArticlesDetailSerializer(serializers.ModelSerializer):
    user = AutherSimpleSerializer(read_only=True)
    comments = CommentsForArticleSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


















