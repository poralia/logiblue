from django.urls import path

from .country.views import CountryListAPIView
from .category.views import CategoryListAPIView

urlpatterns = [
    path('countries/', CountryListAPIView.as_view(), name='countries_search'),
    path('categories/', CategoryListAPIView.as_view(), name='categories_search'),
]
