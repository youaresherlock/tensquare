# 创建用于索引类  指明索引搜索引擎对哪些字段创建索引
from apps.recruit.models import Recruit
from haystack import indexes


class RecruitIndex(indexes.SearchIndex, indexes.Indexable):
    """
    sku索引数据模型类
    """

    id = indexes.IntegerField(model_attr="id")
    jobname = indexes.CharField(model_attr="jobname")

    city = indexes.CharField(model_attr="city")
    # 首先创建字段 对字段命名为text  并且将要建立索引的字段告诉text
    text = indexes.CharField(document=True, use_template=True)

    # 定义方法 用于就返回建立索引模型类
    def get_model(self):
        return Recruit

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
