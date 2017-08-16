# -*- coding: utf-8 -*-
import logging
from slugify import slugify

from .core import ABSCoreCommandImporter

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class BaseImporter(ABSCoreCommandImporter):

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        id = row['reference'].encode('utf-8')
        label = row['label'].encode('utf-8')
        slug = slugify(row['label'])
        logger.info('[SUCCESS][SERIALIZE] {} - {}'.format(id, label))
        return self.model(id=id, label=label, slug=slug)


class SluggedModelImporter(ABSCoreCommandImporter):

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        label = row['label'].encode('utf-8')
        slug = slugify(row['label'])
        logger.info('[SUCCESS][SERIALIZE] {}'.format(label))
        return self.model(label=label, slug=slug)
