# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 02:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conversations', '0007_auto_20171030_1921'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('author', 'comment')]),
        ),
    ]
