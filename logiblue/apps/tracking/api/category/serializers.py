from rest_framework import serializers

from apps.tracking.models import Category


class CategorySerializer(serializers.ModelSerializer):
    country = serializers.CharField(source='country.iso_code')

    class Meta:
        model = Category
        fields = '__all__'
