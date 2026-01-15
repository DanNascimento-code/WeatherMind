from rest_framework import serializers


class ThermalComfortInsightSerializer(serializers.Serializer):
    level = serializers.CharField()
    summary = serializers.CharField()
    factors = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
