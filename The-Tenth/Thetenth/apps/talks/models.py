from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
# Create your models here.
from datetime import datetime
import mongoengine


# 吐槽和吐槽的评论数据都存储在mongodb中,不是存储在mysql中
# 吐槽和吐槽的评论都属于吐槽的这张表
# 吐槽的parent_id为None,评论则有parent_id
from apps.users.models import User


class Spit(models.Model):
    content = RichTextUploadingField(default='')  # 吐槽内容
    publishtime = models.DateTimeField(auto_now_add=True, null=True)  # 发布日期
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 发布人ID
    nickname = models.CharField(max_length=20, null=True)  # 发布人昵称
    visits = models.IntegerField(default=0)  # 浏览量
    thumbup = models.IntegerField(default=0)  # 点赞数
    comment = models.IntegerField(default=0)  # 回复数
    avatar = models.ImageField(null=True, max_length=500)  # 用户的头像
    parent = models.ForeignKey('self', related_name='spits', on_delete=models.SET_NULL, null=True)  # 上级ID
    collected = models.BooleanField(default=False)  # 是否收藏
    hasthumbup = models.BooleanField(default=False)  # 是否点赞

    class Meta:
        db_table = "tb_spit"
        verbose_name = "吐槽"
        ordering = ['-publishtime']

