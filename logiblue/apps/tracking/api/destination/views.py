from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.tracking.libs.raja_ongkir import RajaOngkir
from .serializers import CitySerializer


class CityListAPIView(APIView):
    serializer_class = CitySerializer
    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        ro = RajaOngkir()
        search = request.query_params.get('search', None)
        data = ro.get_cities(search)
        return Response(data, status=data.get('status_code', 406))
