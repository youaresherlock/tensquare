from rest_framework import status
from apps.article.models import Channel
from apps.article.models import Article
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.viewsets import GenericViewSet
from apps.article.serializers import ChannelsSerializer
from apps.article.serializers import ArticleListSerializer
from apps.article.serializers import CreateArticleSerializer
from apps.article.serializers import ArticleIndexSerializer
from apps.article.serializers import ArticlesDetailSerializer
from apps.article.serializers import CommentsForArticleSerializer
from apps.article.utils.pagination import StandardResultPagination


# Create your views here.
class ChannelsView(ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelsSerializer
    pagination_class = StandardResultPagination


class ArticleViewSet(GenericViewSet):
    lookup_value_regex = '((-1)|\d+)'

    queryset = Article.objects.all()
    pagination_class = StandardResultPagination

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            return CreateArticleSerializer(*args, **kwargs)
        elif self.action == 'comment':
            return CommentsForArticleSerializer(*args, **kwargs)
        elif self.action == 'retrieve':
            return ArticlesDetailSerializer(*args, **kwargs)
        elif self.action == 'list_by_channel':
            return ArticleListSerializer(*args, **kwargs)
        else:
            return Response({'message': '参数错误'}, status=status.HTTP_400_BAD_REQUEST)

    # 发布文章
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'message': "请登陆后重试"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        data['user_id'] = user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

        return Response({
            "articleid": article.id,
            'message': '发布成功',
            'success': True
        })

    # 获取文章
    def retrieve(self, request, pk):
        try:
            instance = Article.objects.get(id=pk)
            instance.visits += 1
            instance.save()
        except Exception as e:
            return Response({'message': '获取文章失败'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    # 文章列表
    @action(methods=['get'], detail=True, url_path='channel')
    def list_by_channel(self, request, pk):
        if pk == '-1':
            queryset = self.get_queryset()
        else:
            queryset = self.get_queryset().filter(channel__id=pk)

        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(instance=page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 收藏、取消收藏
    @action(methods=['put'], detail=True, url_path='collect')
    def collection(self, request, pk):
        user = request.user

        if not user.is_authenticated:
            return Response({'message': "请登陆后重试", 'success': False}, )

        try:
            article = Article.objects.get(id=pk)
        except Exception:
            return Response(({"message": "收藏或取消收藏失败", "success": True}))

        user_collection = user.collected_articles.all()

        if article in user_collection:
            user.collected_articles.remove(article)
            return Response({"message": "取消收藏成功", "success": True})
        else:
            user.collected_articles.add(article)
            return Response({"message": "收藏成功", "success": True})

        # 评论文章
    @action(methods=['post'], detail=True, url_path='publish_comment')
    def comment(self, request, pk):

        user = request.user

        if not user.is_authenticated:
            return Response({'message': "请登陆后重试"}, status=status.HTTP_401_UNAUTHORIZED)

        # 反序列化评论信息
        data = request.data
        data['user_id'] = user.id
        serializer = self.get_serializer(data=data)
        print(serializer)
        print(data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 增加评论数
        if data.get('parent') is None:
            article = Article.objects.get(id=pk)
            article.comment_count += 1
            article.save()

        return Response({"message": "评论成功", "success": True})


class ArticleSearchViewSet(HaystackViewSet):
    """
    Article搜索
    """
    index_models = [Article]
    serializer_class = ArticleIndexSerializer











































