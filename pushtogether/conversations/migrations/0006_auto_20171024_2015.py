# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 22:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversations', '0005_auto_20171024_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='comment_nudge',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='conversation',
            name='comment_nudge_interval',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
