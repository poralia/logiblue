from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.tracking.models import Category
from .serializers import CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        queryset = Category.objects.all()
        request = self.request
        search = request.query_params.get('search', None)
        country_code = request.query_params.get('country_code', None)

        if search is not None:
            queryset = queryset.filter(title__icontains=search)

        if country_code is not None:
            queryset = queryset \
                .prefetch_related('country') \
                .select_related('country') \
                .filter(country__iso_code=country_code)

        return queryset
