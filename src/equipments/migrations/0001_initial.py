# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-07 01:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('description', models.TextField(verbose_name='description')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date de cr\xe9ation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('thumbnail', models.ImageField(blank=True, default='default-activity-thumbnail.png', null=True, upload_to='activity/thumbnail', verbose_name='image')),
            ],
            options={
                'verbose_name': 'activit\xe9 sportive',
                'verbose_name_plural': 'activit\xe9s sportives',
            },
        ),
        migrations.CreateModel(
            name='ActivityLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
            ],
            options={
                'verbose_name': "level de l'activit\xe9",
                'verbose_name_plural': 'levels des activit\xe9s',
            },
        ),
        migrations.CreateModel(
            name='Commune',
            fields=[
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('code_insee', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='code INSEE')),
            ],
            options={
                'verbose_name': 'commune',
                'verbose_name_plural': 'communes',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('code', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='code')),
            ],
            options={
                'verbose_name': 'd\xe9partement',
                'verbose_name_plural': 'd\xe9partements',
            },
        ),
        migrations.CreateModel(
            name='EquipmentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date de cr\xe9ation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
            ],
            options={
                'verbose_name': "cat\xe9gorie d'\xe9quipements",
                'verbose_name_plural': "cat\xe9gories d'\xe9quipements",
            },
        ),
        migrations.CreateModel(
            name='EquipmentCategoryFamily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date de cr\xe9ation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
            ],
            options={
                'verbose_name': "famille d'\xe9quipements",
                'verbose_name_plural': "famille d'\xe9quipements",
            },
        ),
        migrations.CreateModel(
            name='EquipmentTarget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'publique cible',
                'verbose_name_plural': 'publique cibles',
            },
        ),
        migrations.CreateModel(
            name='ManagerCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('is_public', models.CharField(choices=[('NOT_DEFINED', 'non d\xe9finie'), ('IS_PUBLIC', 'oui'), ('NOT_PUBLIC', 'non')], default='NOT_DEFINED', max_length=15, verbose_name='est publique ?')),
            ],
            options={
                'verbose_name': 'categorie du gestionnaire',
                'verbose_name_plural': 'categories des gestionnaires',
            },
        ),
        migrations.CreateModel(
            name='SiteEnvironment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'environnement du site',
                'verbose_name_plural': 'environnements des sites',
            },
        ),
        migrations.CreateModel(
            name='SiteGround',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'type du sol',
                'verbose_name_plural': 'types des sols',
            },
        ),
        migrations.CreateModel(
            name='SpecialInstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'institution sp\xe9ciale',
                'verbose_name_plural': 'institutions sp\xe9ciales',
            },
        ),
        migrations.CreateModel(
            name='SportDiscipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='date de cr\xe9ation')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sports_disciplines', to='equipments.Activity')),
            ],
            options={
                'verbose_name': 'discipline sportive',
                'verbose_name_plural': 'disciplines sportives',
            },
        ),
        migrations.CreateModel(
            name='UsageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=150, verbose_name='label')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
            ],
            options={
                'verbose_name': "type d'utilisation",
                'verbose_name_plural': "types d'utilisation",
            },
        ),
        migrations.AlterUniqueTogether(
            name='usagetype',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='specialinstitution',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='siteground',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='siteenvironment',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='managercategory',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='equipmenttarget',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='equipmentcategoryfamily',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AddField(
            model_name='equipmentcategory',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='equipments.EquipmentCategoryFamily'),
        ),
        migrations.AddField(
            model_name='commune',
            name='department',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='communes', to='equipments.Department'),
        ),
        migrations.AlterUniqueTogether(
            name='activitylevel',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='sportdiscipline',
            unique_together=set([('label', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='equipmentcategory',
            unique_together=set([('label', 'slug')]),
        ),
    ]