# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-26 19:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='point',
            old_name='gpx_track',
            new_name='track',
        ),
    ]
