# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 10:59
from __future__ import unicode_literals

from django.db import migrations
import enumfields.fields
import translation.models.translation


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0011_translatedstepsource'),
    ]

    operations = [
        migrations.AlterField(
            model_name='translatedstepsource',
            name='type',
            field=enumfields.fields.EnumField(enum=translation.models.translation.StepSource, max_length=10),
        ),
    ]
