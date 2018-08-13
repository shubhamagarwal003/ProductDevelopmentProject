# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-08-13 11:16
from __future__ import unicode_literals

from django.db import migrations, models
import risk_type.enums


class Migration(migrations.Migration):

    dependencies = [
        ('risk_type', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RiskFieldFloat',
            new_name='RiskFieldNumber',
        ),
        migrations.RemoveField(
            model_name='riskfieldint',
            name='riskfieldsucl_ptr',
        ),
        migrations.AlterField(
            model_name='riskfield',
            name='dtype',
            field=models.CharField(choices=[(risk_type.enums.DataTypes('text'), 'text'), (risk_type.enums.DataTypes('integer'), 'integer'), (risk_type.enums.DataTypes('number'), 'number'), (risk_type.enums.DataTypes('date'), 'date'), (risk_type.enums.DataTypes('enum'), 'enum')], max_length=5),
        ),
        migrations.DeleteModel(
            name='RiskFieldInt',
        ),
    ]
