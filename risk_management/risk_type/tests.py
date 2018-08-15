import json
from django.test import TestCase, Client
from .models import Risk, RiskField, RiskFieldEnumOption
from .enums import RiskTypes, DataTypes
from .serializer import RiskSerializer, RiskFieldSerializer, RiskFieldEnumOptionSerializer
# Create your tests here.


class SerializerTest(TestCase):

    def setUp(self):
        self.risk = Risk.objects.create(name='test', risk_type=RiskTypes.AM)
        RiskField.objects.create(name='text_field', dtype=DataTypes.TE, risk=self.risk,
         description='description')
        self.field_date = RiskField.objects.create(name='date_field', dtype=DataTypes.DA,
            risk=self.risk, description='description')
        self.field_enum = RiskField.objects.create(name='enum_field',
            dtype=DataTypes.EN, risk=self.risk, description='description')
        self.option = RiskFieldEnumOption.objects.create(risk_field_id=self.field_enum.id,
            option='option1')
        RiskFieldEnumOption.objects.create(risk_field_id=self.field_enum.id, option='option2')

    def test_risk_field_enum_option_serializer(self):
        opt_srlzr = RiskFieldEnumOptionSerializer(self.option)
        srlzr_data = opt_srlzr.data
        self.assertEqual(srlzr_data['option'], 'option1')

    def test_risk_field_serializer(self):
        fld_srlzr = RiskFieldSerializer(self.field_date)
        srlzr_data = fld_srlzr.data
        self.assertEqual(srlzr_data['name'], 'date_field')
        self.assertEqual(srlzr_data['description'], 'description')
        self.assertEqual(srlzr_data['dtype'], 'date')
        self.assertEqual(len(srlzr_data['options']), 0)

        fld_srlzr = RiskFieldSerializer(self.field_enum)
        srlzr_data = fld_srlzr.data
        self.assertEqual(srlzr_data['name'], 'enum_field')
        self.assertEqual(srlzr_data['description'], 'description')
        self.assertEqual(srlzr_data['dtype'], 'enum')
        self.assertEqual(len(srlzr_data['options']), 2)

    def test_risk_field(self):
        rsk_srlzr = RiskSerializer(self.risk)
        srlzr_data = rsk_srlzr.data
        self.assertEqual(srlzr_data['name'], 'test')
        self.assertEqual(srlzr_data['id'], self.risk.id)
        self.assertEqual(srlzr_data['risk_type'], 'automobile')
        self.assertEqual(len(srlzr_data['fields']), 3)


class ViewTest(TestCase):

    def setUp(self):
        self.risk = Risk.objects.create(name='test', risk_type=RiskTypes.AM)
        RiskField.objects.create(name='text_field', dtype=DataTypes.TE, risk=self.risk,
         description='description')
        self.field_date = RiskField.objects.create(name='date_field', dtype=DataTypes.DA,
            risk=self.risk, description='description')
        self.field_enum = RiskField.objects.create(name='enum_field',
            dtype=DataTypes.EN, risk=self.risk, description='description')
        self.option = RiskFieldEnumOption.objects.create(risk_field_id=self.field_enum.id,
            option='option1')
        RiskFieldEnumOption.objects.create(risk_field_id=self.field_enum.id, option='option2')

    def test_get_risk(self):
        client = Client()
        response = client.get('/get/risk/' + str(self.risk.id) + '/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.check_response(data)

        client = Client()
        response = client.get('/get/risk/' + str(self.risk.id + 10) + '/')
        self.assertEqual(response.status_code, 404)

    def test_get_all_risk(self):
        client = Client()
        response = client.get('/get/risks/')
        data = json.loads(response.content.decode('utf-8'))
        self.assertEqual(len(data), 1)
        self.check_response(data[0])

    def check_response(self, data):
        self.assertEqual(data['name'], 'test')
        self.assertEqual(data['risk_type'], 'automobile')
        self.assertEqual(data['id'], self.risk.id)
        self.assertEqual(len(data['fields']), 3)
        fields = sorted(data['fields'], key=lambda f: f['dtype'])
        self.assertEqual([f['name'] for f in fields], ['date_field', 'enum_field', 'text_field'])
        options = sorted(fields[1]['options'], key=lambda o: o['option'])
        self.assertEqual([o['option'] for o in options], ['option1', 'option2'])
