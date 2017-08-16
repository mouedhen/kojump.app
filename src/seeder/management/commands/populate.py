# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import logging

from django.core.management.base import BaseCommand

from django.contrib.auth.models import User
from ..helpers.base import BaseImporter, SluggedModelImporter
from ..helpers.models_importer import ManagerImporter, DepartmentImporter, CommuneImporter, InstitutionImporter
from ..helpers.activity import ActivityImporter
from ..helpers.category import CategoryImporter
from ..helpers.discipline import DisciplineImporter
from ..helpers.equipment import EquipmentImporter
from ..helpers.equipments_activities import EquipmentActivityAssociationImporter

from equipments.models import *
from django.conf import settings


logger = logging.getLogger(__name__)
DEFAULT_ADMIN_PASSWORD = 'GRatiCaTICAtEdiS'


class Command(BaseCommand):
    help = 'Command to populate database\'s table from directory data'

    def add_arguments(self, parser):
        parser.add_argument('--users', action='store_true', dest='users', default=False, help='super admin')
        parser.add_argument('--all', action='store_true', dest='all', default=False, help='database tables')
        parser.add_argument('--families', action='store_true', dest='families', default=False, help='families')
        parser.add_argument('--categories', action='store_true', dest='categories', default=False, help='categories')
        parser.add_argument('--activities', action='store_true', dest='activities', default=False, help='activities')
        parser.add_argument('--disciplines', action='store_true', dest='disciplines', default=False, help='disciplines')
        parser.add_argument('--slug', action='store_true', dest='slug', default=False, help='slug')
        parser.add_argument('--managers', action='store_true', dest='managers', default=False, help='managers')
        parser.add_argument('--departments', action='store_true', dest='departments', default=False, help='departments')
        parser.add_argument('--communes', action='store_true', dest='communes', default=False, help='communes')
        parser.add_argument('--installations', action='store_true', dest='installations', default=False, help='installations')
        parser.add_argument('--equipments', action='store_true', dest='equipments', default=False, help='equipments')
        parser.add_argument('--associate', action='store_true', dest='associate', default=False, help='associate')
        parser.add_argument('--delete', action='store_true', dest='delete', default=False, help='delete')

    def handle(self, *args, **options):
        logger.debug('[SEEDER] start populating database tables')

        if options['users']:
            logger.debug('[SEEDER] populating users table')
            user = User(username='admin', email='chams-med@hotmail.fr',
                        first_name='Mohamed Chams Eddin', last_name='Mouedhen',
                        is_superuser=True, is_staff=True, is_active=True)
            user.set_password(DEFAULT_ADMIN_PASSWORD)
            user.save()
            logger.debug('[SEEDER] user "{}" was created successfully'.format(user.username))
        if options['families']:
            families_importer = BaseImporter(
                filename=os.path.join(settings.BASE_DIR, '..', 'data', '1.categories_families.csv'),
                model=EquipmentCategoryFamily
            )
            families_importer.populate()
            logger.info('[SEEDER][POPULATING] families end')
        if options['categories']:
            category_importer = CategoryImporter()
            category_importer.populate()
            logger.info('[SEEDER][POPULATING] categories end')
        if options['activities']:
            activity_importer = ActivityImporter()
            activity_importer.populate()
            logger.info('[SEEDER][POPULATING] activities end')
        if options['disciplines']:
            sport_discipline_importer = DisciplineImporter()
            sport_discipline_importer.populate()
            logger.info('[SEEDER][POPULATING] disciplines end')
        if options['slug']:
            activity_level_importer = SluggedModelImporter(
                filename=os.path.join(settings.BASE_DIR, '..', 'data', '5.activities_levels.csv'),
                model=ActivityLevel
            )
            activity_level_importer.populate()
            logger.info('[SEEDER][POPULATING] levels end')

            site_environment_importer = SluggedModelImporter(
                filename=os.path.join(settings.BASE_DIR, '..', 'data', '6.sites_environments.csv'),
                model=SiteEnvironment
            )
            site_environment_importer.populate()
            logger.info('[SEEDER][POPULATING] environments end')

            site_ground_importer = SluggedModelImporter(
                filename=os.path.join(settings.BASE_DIR, '..', 'data', '7.sites_grounds.csv'),
                model=SiteGround
            )
            site_ground_importer.populate()
            logger.info('[SEEDER][POPULATING] grounds end')

            usage_type_importer = SluggedModelImporter(
                filename=os.path.join(settings.BASE_DIR, '..', 'data', '8.usages_types.csv'),
                model=UsageType
            )
            usage_type_importer.populate()
            logger.info('[SEEDER][POPULATING] usages type end')

            equipment_target_importer = SluggedModelImporter(
                filename=os.path.join(settings.BASE_DIR, '..', 'data', '9.equipments_targets.csv'),
                model=EquipmentTarget
            )
            equipment_target_importer.populate()
            logger.info('[SEEDER][POPULATING] targets end')

            special_institution_importer = SluggedModelImporter(
                filename=os.path.join(settings.BASE_DIR, '..', 'data', '11.special_institutions.csv'),
                model=SpecialInstitution
            )
            special_institution_importer.populate()
            logger.info('[SEEDER][POPULATING] specials end')
        if options['managers']:
            managers_category_importer = ManagerImporter()
            managers_category_importer.populate()
            logger.info('[SEEDER][POPULATING] managers end')

        if options['departments']:
            department_importer = DepartmentImporter()
            department_importer.populate()
            logger.info('[SEEDER][POPULATING] departments end')

        if options['communes']:
            commune_importer = CommuneImporter()
            commune_importer.populate()
            logger.info('[SEEDER][POPULATING] communes end')

        if options['installations']:
            installation_importer = InstitutionImporter()
            installation_importer.populate()
            logger.info('[SEEDER][POPULATING] installations end')

        if options['equipments']:
            equipment_importer = EquipmentImporter()
            equipment_importer.populate()
            logger.info('[SEEDER][POPULATING] equipments end')

        if options['associate']:
            association_importer = EquipmentActivityAssociationImporter()
            association_importer.populate()
            logger.info('[SEEDER][POPULATING] association end')

        if options['delete']:
            Equipment.objects.all().delete()
