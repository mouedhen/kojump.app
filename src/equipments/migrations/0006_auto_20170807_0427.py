# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0005_sportdiscipline_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sportdiscipline',
            name='id',
        ),
        migrations.AddField(
            model_name='sportdiscipline',
            name='reference',
            field=models.PositiveIntegerField(default=0, primary_key=True, serialize=False, verbose_name='ref\xe9rence unique'),
        ),
    ]
