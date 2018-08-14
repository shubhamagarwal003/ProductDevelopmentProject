from .models import RiskField, Risk, RiskFieldEnumOption
from .enums import RiskTypes, DataTypes
from rest_framework import serializers


class RiskFieldEnumOptionSerializer(serializers.ModelSerializer):
    """
    Serializer for Risk Enum Field Options
    """
    class Meta:
        model = RiskFieldEnumOption
        fields = ['option']


class RiskFieldSerializer(serializers.ModelSerializer):
    """
    Serializer fro Risk Field
    """
    options = RiskFieldEnumOptionSerializer(many=True, read_only=True)
    dtype = serializers.SerializerMethodField()

    class Meta:
        model = RiskField
        fields = ['name', 'description', 'options', 'dtype']

    def get_dtype(self, obj):
        return eval(obj.dtype).value


class RiskSerializer(serializers.ModelSerializer):
    """
    Serializer for Risk
    """
    fields = RiskFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Risk
        fields = ['name', 'id', 'fields']
