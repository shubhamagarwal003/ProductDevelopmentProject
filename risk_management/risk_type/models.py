from django.db import models
from .enums import RiskTypes, DataTypes
from django.core.exceptions import ValidationError
# Create your models here.


class Risk(models.Model):
    """ORM Class for different Risk Type. This is a individual template. 
       Params :
            name - Name of the Risk Type
            risk_type - Risk Type enum (automobiles, houses, etc.)
    """
    name = models.CharField(max_length=50, default="")
    risk_type = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in RiskTypes])


class Insurance(models.Model):
    """ORM Class for actual insurance based on a template
    """
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE)


class RiskField(models.Model):
    """ORM class for storing field names and other metadata for Risk Type
       Params: 
            name - Name of the field
            dtype - Data Type for the field. Can be enum
            risk - Foreign Key to Risk table
            description - Description about the field.
    """
    # Any other metadata for field can be added here
    name = models.CharField(max_length=50, default="")
    dtype = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in DataTypes])
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name='fields')
    description = models.TextField(default="")


class RiskFieldSuCl(models.Model):
    """A Super Class for each RiskField Data Type"""
    risk_field = models.ForeignKey(RiskField, on_delete=models.CASCADE)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)

    def clean(self):
        super(RiskFieldSuCl, self).clean()

    def save(self, **kwargs):
        self.clean()
        return super(RiskFieldSuCl, self).save(**kwargs)


class RiskFieldText(RiskFieldSuCl):
    """ORM class for storing Text Field Data"""
    value = models.TextField()

    def clean(self):
        super(RiskFieldText, self).clean()
        if not validate_dtype(self.risk_field, DataTypes.TE):
            raise ValidationError("Risk Field Type is not Text")


class RiskFieldDate(RiskFieldSuCl):
    """ORM class for storing Date Field Data"""
    value = models.DateField()

    def clean(self):
        super(RiskFieldDate, self).clean()
        if not validate_dtype(self.risk_field, DataTypes.DA):
            raise ValidationError("Risk Field Type is not Date")


class RiskFieldNumber(RiskFieldSuCl):
    """ORM class for storing Number Field Data"""
    value = models.FloatField()

    def clean(self):
        super(RiskFieldNumber, self).clean()
        if not validate_dtype(self.risk_field, DataTypes.NU):
            raise ValidationError("Risk Field Type is not Number(Float)")


class RiskFieldEnumOption(models.Model):
    """ORM class for storing Enum Field Choice"""
    option = models.CharField(max_length=10)
    risk_field = models.ForeignKey(RiskField, on_delete=models.CASCADE, related_name='options')

    def clean(self):
        super(RiskFieldEnumOption, self).clean()
        if not validate_dtype(self.risk_field, DataTypes.EN):
            raise ValidationError("Risk Field Type is not Enum")

    def save(self, **kwargs):
        self.clean()
        return super(RiskFieldEnumOption, self).save(**kwargs)


class RiskFieldEnum(RiskFieldSuCl):
    """ORM class for storing Enum Field Data"""
    value = models.ForeignKey(RiskFieldEnumOption, on_delete=models.CASCADE)

    def clean(self):
        super(RiskFieldEnum, self).clean()
        if not validate_dtype(self.risk_field, DataTypes.EN):
            raise ValidationError("Risk Field Type is not Enum")


def validate_dtype(field, dtype):
    if (field.dtype == dtype or eval(field.dtype) == dtype):
        return True
    return False
