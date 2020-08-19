from rest_framework.serializers import ModelSerializer

from apps.talks.models import Spit


class SpitSerializer(ModelSerializer):
    class Meta:
        model = Spit
        fields = '__all__'

    def create(self, validated_data):

        content = validated_data.get('content')
        parent = validated_data.get('parent')
        spit = Spit.objects.create(content=content,
                                   parent=parent)

        if parent:
            spit.parent.comment += 1
            spit.parent.save()

        return spit
