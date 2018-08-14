import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import RiskField, Risk, RiskFieldEnumOption
from .enums import RiskTypes, DataTypes
from .serializer import RiskSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def get_risk(request, risk_id):
    try:
        risk = Risk.objects.filter(id=risk_id).prefetch_related('fields', 'fields__options')
        if(len(risk) > 0):
            response = RiskSerializer(risk[0]).data
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            response = {"message": "Invalid Id. No entry Found"}
            return HttpResponse(json.dumps(response), content_type="application/json",
                     status=404)
    except Exception as e:
        raise e
        response = {"message": "Unknown Error Occurred. Please try again"}
        return HttpResponse(json.dumps(response), content_type="application/json",
                 status=500)


def get_all_risk(request):
    risks = Risk.objects.all().prefetch_related('fields', 'fields__options')
    response = [RiskSerializer(r).data for r in risks]
    return HttpResponse(json.dumps(response), content_type="application/json")
