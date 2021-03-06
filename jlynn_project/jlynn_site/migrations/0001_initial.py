# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('length', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('media', models.TextField(max_length=1000)),
                ('status', models.BooleanField(default=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo_small', models.ImageField(blank=True, upload_to='images/small/')),
                ('photo_large', models.ImageField(blank=True, upload_to='images/large/')),
            ],
        ),
    ]
