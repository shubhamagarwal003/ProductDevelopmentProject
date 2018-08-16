import json
from django.http import HttpResponse
from .models import Risk
from .serializer import RiskSerializer
# Create your views here.


def get_risk(request, risk_id):
    # Returns a single risk type based on id
    try:
        risk = Risk.objects.filter(id=risk_id).prefetch_related('fields', 'fields__options')
        if(len(risk)):
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
    # Returns all risk types
    risks = Risk.objects.all().prefetch_related('fields', 'fields__options')
    response = [RiskSerializer(r).data for r in risks]
    return HttpResponse(json.dumps(response), content_type="application/json")
