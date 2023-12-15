from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.tracking.libs.raja_ongkir import RajaOngkir
from .serializers import CitySerializer, CalculateSerializer


class CityListAPIView(APIView):
    serializer_class = CitySerializer
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        ro = RajaOngkir()
        search = request.query_params.get('search', None)
        data = ro.get_cities(search)
        return Response(data, status=data.get('status_code', 406))


class CalculateAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = CalculateSerializer

    def create(self, request, *args, **kwargs):
        ro = RajaOngkir()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            weight = serializer.data.get('weight', 0)
            country_code = serializer.data.get('country_code', None)
            category_id = serializer.data.get('category_id', 0)
            destination_id = serializer.data.get('destination_id', 0)

            ret = ro.calculate(
                country_code,
                category_id,
                weight,
                destination_id
            )
            if ret is None:
                return Response(
                    {'message': 'Country not found.'},
                    status=404
                )
            return Response(ret)
        return Response({'message': 'Something wrong'}, status=406)
