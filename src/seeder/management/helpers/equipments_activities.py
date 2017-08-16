# -*- coding: utf-8 -*-
import os
import logging
from unicodecsv import DictReader
from django.conf import settings

from equipments.models import Equipment, SportDiscipline

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class EquipmentActivityAssociationImporter:

    def __init__(self, filename=None):
        """
        Class constructor.
        :param filename: str
        """
        if filename is None:
            self.filename = os.path.join(settings.BASE_DIR, '..', 'data', '16.equipments_activities.csv')

    def filename(self, filename):
        """
        Set filename property.
        :param filename: str
        :return: None
        """
        self.filename = filename

    @staticmethod
    def serialize(row):
        equipment = None
        disciplines = None
        if row['EquipementId'].isdecimal():
            try:
                equipment = Equipment.objects.get(code=row['EquipementId'])
                logger.info('retrieve equipment {}'.format(equipment.name.encode('utf-8')))
            except Equipment.DoesNotExist:
                equipment = None
                logger.error('equipment {} does not exist'.format(row['EquipementId']))
        if row['ActCode'].isdecimal():
            try:
                disciplines = SportDiscipline.objects.get(reference=row['ActCode'])
                logger.info('retrieve discipline {}'.format(disciplines.label.encode('utf-8')))
            except SportDiscipline.DoesNotExist:
                disciplines = None
                logger.error('discipline {} does not exist'.format(row['ActCode']))
        return equipment, disciplines

    def process(self, reader):
        """
        Prepare a list of records.
        :param reader:
        :return: bool
        """
        for row in reader:
            equipment, disciplines = self.serialize(row)
            if equipment is None or disciplines is None:
                pass
            else:
                equipment.disciplines.add(disciplines)
        return True

    def populate(self):
        try:
            with open(self.filename, 'r') as csv_file:
                reader = DictReader(csvfile=csv_file, delimiter=',', encoding='utf-8')
                self.process(reader)
        except IOError as error:
            logger.error('Data file unreachable, please check the filename path.')
            logger.info(error)
        except AttributeError as error:
            logger.error('Attribute error, please check the serialization method.')
            logger.info(error)
        return True
