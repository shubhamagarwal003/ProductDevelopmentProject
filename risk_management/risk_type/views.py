import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import RiskField, Risk
from .enums import RiskTypes, DataTypes
# from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def get_risk(request, risk_id):
    try:
        risk = Risk.objects.get(id=risk_id)
        risk_fields = RiskField.objects.filter(risk=risk)
        fields = [{
            "name": f.name,
            "type": eval(f.dtype).value,
            "description": f.description
        } for f in risk_fields]
        response = {
            "id": risk.id,
            "name": risk.name,
            "type": eval(risk.risk_type).value,
            "fields": fields
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
    except ObjectDoesNotExist:
        response = {"message": "Invalid Id. No entry Found"}
        return HttpResponse(json.dumps(response), content_type="application/json",
                 status=404)
    except Exception:
        response = {"message": "Unknown Error Occurred. Please try again"}
        return HttpResponse(json.dumps(response), content_type="application/json",
                 status=500)


def get_all_risk(request):
    risks = Risk.objects.all()
    risk_fields = RiskField.objects.filter(risk__in=risks)
    response = [{
        "id": r.id,
        "name": r.name,
        "type": eval(r.risk_type).value,
        "fields": [{
                "name": f.name,
                "type": eval(f.dtype).value,
                "description": f.description
                } for f in risk_fields if f.risk_id == r.id]
    } for r in risks]

    return HttpResponse(json.dumps(response), content_type="application/json")
