from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.tracking.models import Country
from .serializers import CountrySerializer


class CountryListAPIView(generics.ListAPIView):
    serializer_class = CountrySerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        queryset = Country.objects.all().order_by('name')
        request = self.request
        search = request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(name__icontains=search)
        return queryset
