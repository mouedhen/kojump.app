# -*- coding: utf-8 -*-
import os
import logging
from slugify import slugify

from django.conf import settings

from .core import ABSCoreCommandImporter
from equipments.models import EquipmentCategoryFamily, EquipmentCategory
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CategoryImporter(ABSCoreCommandImporter):

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        if filename is None:
            filename = os.path.join(settings.BASE_DIR, '..', 'data', '2.categories.csv')
        if model is None:
            model = EquipmentCategory
        super(CategoryImporter, self).__init__(filename, model)

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        id = row['reference'].encode('utf-8')
        label = row['label'].encode('utf-8')
        slug = slugify(row['label'])
        family_id = row['family_reference'].encode('utf-8')
        # family = EquipmentCategoryFamily.objects.get(reference=family_ref)
        logger.info('[SUCCESS][SERIALIZE] {} - {}'.format(id, label))
        return self.model(id=id, label=label, slug=slug, family_id=family_id)
