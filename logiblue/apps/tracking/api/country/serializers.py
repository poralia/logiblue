from rest_framework import serializers

from apps.tracking.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'
