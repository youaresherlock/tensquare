import re

from rest_framework import serializers

from apps.article.models import Article
from apps.asks.models import Label, Reply, Question
from apps.recruit.models import Enterprise
from apps.users.models import User


class UserLabelSerializer(serializers.ModelSerializer):
    """用户标签序列化器"""
    id = serializers.IntegerField(label='标签ID', read_only=True)

    class Meta:
        model = Label
        fields = ('id', 'label_name')
        extra_kwargs = {
            'label_name': {
                'read_only': True
            }
        }


class UserMessSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class SubsSerializer(serializers.ModelSerializer):
    """问题回复序列化器"""
    user = serializers.SerializerMethodField(label='用户信息')

    class Meta:
        model = Reply
        fields = ('id', 'content', 'createtime', 'useful_count', 'unuseful_count', 'user')

    def get_user(self, obj):
        user = UserMessSerializer(obj)
        return user.data


class UserQuestionsSerializer(serializers.ModelSerializer):
    """用户提问序列化器"""
    labels = serializers.StringRelatedField(label='问题标签', read_only=True, many=True)
    user = serializers.StringRelatedField(label='用户昵称', read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'createtime', 'labels', 'reply', 'replyname', 'replytime', 'title', 'unuseful_count',
                  'useful_count', 'user', 'visits')


class UserAQSerializer(serializers.ModelSerializer):
    """用户回答序列化器"""
    user = UserMessSerializer(label='回答用户信息', read_only=True)

    class Meta:
        model = Reply
        fields = ('id', 'content', 'createtime', 'useful_count', 'problem', 'unuseful_count', 'user')

    def get_subs(self, obj):
        subs = SubsSerializer(obj)
        return subs.data

    def get_user(self, obj):
        user = UserMessSerializer(obj)
        return user.data


class ArticleSimpleSerializer(serializers.ModelSerializer):
    """文章简易序列化器"""
    class Meta:
        model = Article
        fields = ('id', 'title')


class ArticlesUserSerializer(serializers.ModelSerializer):
    """文章用户序列化器"""

    class Meta:
        model = User
        fields = ('id', 'username', 'avatar')


class CollectedArticlesSerializer(serializers.ModelSerializer):
    """收藏文章序列化器"""
    user = ArticlesUserSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'createtime', 'user', 'collected_users', 'image', 'visits')


class EnterpriseSerializer(serializers.ModelSerializer):
    """收藏企业序列化器"""
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'labels', 'logo', 'recruits', 'summary')


class UserInfoSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    labels = UserLabelSerializer(label='用户标签', many=True, read_only=True)
    questions = serializers.SerializerMethodField(label='用户提问', read_only=True)
    answer_question = serializers.SerializerMethodField(label='用户回答', read_only=True)
    collected_articles = serializers.SerializerMethodField(label='收藏文章', read_only=True)
    enterpises = EnterpriseSerializer(label='收藏企业', many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'realname', 'birthday', 'sex', 'avatar', 'website', 'email', 'city',
                  'address', 'labels', 'enterpises', 'questions', 'answer_question', 'collected_articles')
        extra_kwargs = {
            'username': {
                'read_only': True
            }
        }

    def get_questions(self, obj):
        user_questions = obj.question.all()
        questions = []
        if user_questions:
            serializer = UserQuestionsSerializer(user_questions, many=True)
            questions = serializer.data
        return questions

    def get_answer_question(self, obj):
        answers = obj.replies.all()
        answer_question = []
        if answers:
            serializer = UserAQSerializer(answers, many=True)
            answer_question = serializer.data
        return answer_question

    def get_collected_articles(self, obj):
        articles = obj.collected_articles.all()
        collected_articles = []
        if articles:
            serializer = CollectedArticlesSerializer(articles, many=True)
            collected_articles = serializer.data
        return collected_articles

    def validated_website(self, value):
        if not re.match(r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$', value):
            raise serializers.ValidationError('网址不正确')
        return value

    def validate_email(self, value):
        if value:
            if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', value):
                raise serializers.ValidationError('邮箱不正确')
        return value

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式不正确')
        return value




