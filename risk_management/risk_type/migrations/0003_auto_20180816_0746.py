# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-08-16 07:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('risk_type', '0002_auto_20180814_0645'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='risk_type.Risk')),
            ],
        ),
        migrations.AlterField(
            model_name='riskfieldenum',
            name='value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='risk_type.RiskFieldEnumOption'),
        ),
        migrations.AddField(
            model_name='riskfieldsucl',
            name='insurance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='risk_type.Insurance'),
            preserve_default=False,
        ),
    ]
