# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-06 12:52
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeoLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(blank=True, max_length=254, verbose_name='adresse (1\xe8re ligne')),
                ('street_address2', models.CharField(blank=True, max_length=254, verbose_name='adresse (2\xe8me ligne')),
                ('postal_code', models.CharField(blank=True, max_length=10, verbose_name='code postal')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='ville')),
                ('country', models.CharField(blank=True, max_length=100, verbose_name='pays')),
                ('gps_coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='coordonn\xe9es GPS')),
            ],
            options={
                'verbose_name': 'emplacement g\xe9ographique',
                'verbose_name_plural': 'emplacements g\xe9ographiques',
            },
        ),
    ]
