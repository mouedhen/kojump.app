# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 00:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimeInterval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('MON', 'Lundi'), ('TUE', 'Mardi'), ('WED', 'Mercredi'), ('THU', 'Jeudi'), ('FRI', 'Vendredi'), ('SAT', 'Samedi'), ('SUN', 'Dimanche')], max_length=3, verbose_name='jour de la semaine')),
                ('start_time', models.TimeField(verbose_name='heure d\xe9but')),
                ('end_time', models.TimeField(verbose_name='heure fin')),
            ],
        ),
    ]
