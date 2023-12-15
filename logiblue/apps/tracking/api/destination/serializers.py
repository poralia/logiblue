from rest_framework import serializers


class CitySerializer(serializers.Serializer):
    city_id = serializers.CharField()
    city_name = serializers.CharField()
    province_id = serializers.CharField()
    province = serializers.CharField()
    type = serializers.CharField()
    postal_code = serializers.CharField()


class CalculateSerializer(serializers.Serializer):
    country_code = serializers.CharField()
    category_id = serializers.CharField()
    destination_id = serializers.CharField()
    weight = serializers.FloatField()
