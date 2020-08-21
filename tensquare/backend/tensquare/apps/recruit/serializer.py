from rest_framework import serializers

from recruit.models import Enterprise, Recruit, City


class EnterpriseSerializerSimple(serializers.ModelSerializer):

    class Meta:
        model = Enterprise
        fields = ('id', 'name','labels','logo','recruits','summary')


class RecruitSerializerSimple(serializers.ModelSerializer):
    enterprise = EnterpriseSerializerSimple(read_only=True)

    class Meta:
        model = Recruit
        fields = ('id', 'jobname','salary','condition','education','type','city','createtime','enterprise','labels')


class EnterpriseSerializer(serializers.ModelSerializer):
    recruits = RecruitSerializerSimple(many=True, read_only=True)

    class Meta:
        model = Enterprise
        fields = "__all__"


class RecruitSerializer(serializers.ModelSerializer):
    enterprise = EnterpriseSerializer(read_only=True)

    class Meta:
        model = Recruit
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"
