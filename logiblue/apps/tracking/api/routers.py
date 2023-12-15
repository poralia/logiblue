from django.urls import path

from .country.views import CountryListAPIView
from .category.views import CategoryListAPIView
from .destination.views import CityListAPIView, CalculateAPIView

urlpatterns = [
    path('countries/', CountryListAPIView.as_view(), name='countries_search'),
    path('cities/', CityListAPIView.as_view(), name='cities_search'),
    path('calculate/', CalculateAPIView.as_view(), name='calculate'),
    path('categories/', CategoryListAPIView.as_view(), name='categories_search'),  # noqa
]
