from .models import RiskField, Risk, RiskFieldEnumOption
from .enums import RiskTypes, DataTypes
from rest_framework import serializers


class RiskFieldEnumOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskFieldEnumOption
        fields = ['option']


class RiskFieldSerializer(serializers.ModelSerializer):
    # options = serializers.SerializerMethodField()
    options = RiskFieldEnumOptionSerializer(many=True, read_only=True)
    dtype = serializers.SerializerMethodField()

    class Meta:
        model = RiskField
        fields = ['name', 'description', 'options', 'dtype']

    def get_dtype(self, obj):
        return eval(obj.dtype).value


class RiskSerializer(serializers.ModelSerializer):
    fields = RiskFieldSerializer(many=True, read_only=True)

    class Meta:
        model = Risk
        fields = ['name', 'id', 'fields']
