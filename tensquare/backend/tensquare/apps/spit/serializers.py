from mongoengine import  ValidationError
from rest_framework_mongoengine import serializers

from spit.models import Spit


class SpitSerializer(serializers.DocumentSerializer):

    class Meta:
        model = Spit
        fields = "__all__"

    def create(self, validated_data):
        spit = super().create(validated_data)

        try:
            user = self.context["request"].user
        except:
            user = None

        #    判断是否是评论别人
        if spit.parent:
            # 评论别人必须登陆
            if user and user.is_authenticated:
                spit.userid = str(user.id)
                spit.nickname = user.nickname if user.nickname else user.username
                spit.avatar = user.avatar
                spit.save()
                spit.parent.comment += 1
                spit.parent.save()
                return spit
            else:
                raise ValidationError('未登录')
        else:
            return spit

