# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jlynn_site', '0003_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]