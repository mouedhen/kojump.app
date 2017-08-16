# -*- coding: utf-8 -*-
import logging
from abc import ABCMeta, abstractmethod, abstractproperty
from unicodecsv import DictReader

from slugify import slugify

from django.db import models

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ABSCoreCommandImporter:

    __metaclass__ = ABCMeta

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        self.filename = filename
        self.model = model

    def filename(self, filename):
        """
        Set filename property.
        :param filename: str
        :return: None
        """
        self.filename = filename

    def model(self, model):
        """
        Set model property.
        :param model: models.Model
        :return: None
        """
        self.model = model

    @abstractmethod
    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        pass

    def append_records(self, records, row):
        records.append(self.serialize(row=row))

    def prepare(self, reader):
        """
        Prepare a list of records.
        :param reader:
        :return: list
        """
        records = []
        for row in reader:
            records.append(self.serialize(row=row))
        return records

    def populate(self):
        try:
            with open(self.filename, 'r') as csv_file:
                reader = DictReader(csvfile=csv_file, delimiter=',', encoding='utf-8')
                records = self.prepare(reader)
            initial_len = len(records)
            records = filter(None, records)
            self.model.objects.bulk_create(records)
            logger.info('[SUCCESS][CREATE] {} Records / {} was been created'.format(len(records), initial_len))
        except IOError as error:
            logger.error('Data file unreachable, please check the filename path.')
            logger.info(error)
        except AttributeError as error:
            logger.error('Attribute error, please check the serialization method.')
            logger.info(error)
        return True

    def clean(self):
        self.model.objects.all().delete()
        logger.info('[SUCCESS][DELETE] Records was been deleted')
