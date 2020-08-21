from django.shortcuts import render

# Create your views here.
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from article.models import Article, Channel
from article.serializers import ArticleSerializerForCreate, ArticleSerializerForDetail, \
    CommentSerializerItem, ChannelSerializer, ArticleSerializerForList, ArticleIndexSerializer, \
    CommentSerializerForCreate


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()

    # 新建文章 /article/
    def create(self, request, *args, **kwargs):

        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            request_params = request.data
            request_params['user'] = user.id
            serializer = ArticleSerializerForCreate(data=request_params)
            serializer.request = request
            serializer.is_valid(raise_exception=True)
            article = serializer.save()
            return Response({'success':True,'message':'发表成功','articleid':article.id})
        else:
            return Response({'success':False,'message':'未登录'}, status=400)

    # 文章详情  /article/{id}/
    def retrieve(self, request, *args, **kwargs):
        article = super().get_object()
        article.visits += 1
        article.save()
        s = ArticleSerializerForDetail(instance=article)
        return Response(s.data)

    # 文章列表
    def list(self, request, *args, **kwargs):
        articles = super().get_queryset()
        s = ArticleSerializerForList(instance=articles,many=True)
        return Response(s.data)

    # 收藏文章 /article/{id}/collect/
    @action(methods=['put'], detail=True)
    def collect(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            article = self.get_object()
            if user not in article.collected_users.all():
                article.collected_users.add(user)
                article.save()
                return Response({'success':True,'message':'收藏成功'})
            else:
                article.collected_users.remove(user)
                article.save()
                return Response({'success':True,'message':'取消收藏成功'})
        else:

            return Response({'success':False,'message':'未登录'}, status=400)

    # 发布文章的评论 /article/{id}/publish_comment/
    @action(methods=['post'], detail=True)
    def publish_comment(self, request, pk):
        try:
            user = request.user
        except Exception:
            user = None

        if user is not None and user.is_authenticated:
            article = self.get_object()
            article.comment_count+=1
            article.save()
            request_params = request.data
            request_params['user'] = user.id
            request_params['article'] = article.id
            s = CommentSerializerForCreate(data=request_params)
            s.is_valid(raise_exception=True)
            s.save()
            return Response({'success': True, 'message': '评论成功'})
        else:
            return Response({'success': False, 'message': '未登录'}, status=400)

    # 按频道获取文章列表 /article/{pk}/channel/
    @action(methods=['get'], detail=True, url_path="channel")
    def get_article_by_channel(self, request, pk):
        if pk == "-1":
            articles = self.get_queryset()
        else:
            channel = Channel.objects.get(id=pk)
            articles = self.get_queryset().filter(channel=channel)

        page = self.paginate_queryset(articles)
        if page is not None:
            s = ArticleSerializerForList(page, many=True)
            return self.get_paginated_response(s.data)
        else:
            s = ArticleSerializerForList(instance=articles, many=True)
            return Response(s.data)


class ChannelViewSet(ReadOnlyModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ArticleSearchViewSet(HaystackViewSet):
    """
    Article搜索
    """
    index_models = [Article]
    serializer_class = ArticleIndexSerializer