# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 13:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('translation', '0002_auto_20170711_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='yandextranslator',
            name='count_steps',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yandextranslator',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yandextranslator',
            name='translated_symbols',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='yandextranslator',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='translationstep',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='translation.TranslatedLesson'),
        ),
    ]