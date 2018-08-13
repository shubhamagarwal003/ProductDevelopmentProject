from django.contrib import admin
from .models import (
    Risk,
    RiskField,
    RiskFieldText,
    RiskFieldDate,
    RiskFieldNumber,
    RiskFieldEnum
)
# Register your models here.
admin.site.register(Risk)
admin.site.register(RiskField)
admin.site.register(RiskFieldText)
admin.site.register(RiskFieldDate)
admin.site.register(RiskFieldNumber)
admin.site.register(RiskFieldEnum)
