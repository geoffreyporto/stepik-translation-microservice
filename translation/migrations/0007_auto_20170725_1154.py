# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0006_auto_20170725_1142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='translationservice',
            name='api_key',
        ),
        migrations.AlterField(
            model_name='translationservice',
            name='service_name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]