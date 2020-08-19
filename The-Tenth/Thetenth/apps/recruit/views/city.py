from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.recruit.serializers.city import CitySerializer
from apps.recruit.models import City


class CityAPIView(GenericAPIView):

    serializer_class = CitySerializer

    queryset = City.objects.all()


    def get(self, request):

        cities = self.get_queryset().filter(ishot=1)

        serializer = CitySerializer(instance=cities, many=True)

        return Response(serializer.data)


