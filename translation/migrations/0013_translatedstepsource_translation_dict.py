# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 14:57
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0012_change_type_of_type_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='translatedstepsource',
            name='translation_dict',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]
