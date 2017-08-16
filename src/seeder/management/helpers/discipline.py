# -*- coding: utf-8 -*-
import os
import logging
from slugify import slugify

from django.conf import settings

from .core import ABSCoreCommandImporter
from equipments.models import Activity, SportDiscipline
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class DisciplineImporter(ABSCoreCommandImporter):

    def __init__(self, filename=None, model=None):
        """
        Class constructor.
        :param filename: str
        :param model: models.Model
        """
        if filename is None:
            filename = os.path.join(settings.BASE_DIR, '..', 'data', '4.sports_disciplines.csv')
        if model is None:
            model = SportDiscipline
        super(DisciplineImporter, self).__init__(filename, model)

    def serialize(self, row):
        """
        Serialize row to model
        :param row:
        :return: models.Model
        """
        reference = row['reference'].encode('utf-8')
        label = row['label'].encode('utf-8')
        slug = slugify(row['label'])
        activity_ref = row['activity_reference'].encode('utf-8')
        if int(activity_ref) > 89:
            activity_ref = str(89)
        activity = Activity.objects.get(id=activity_ref)
        is_active = activity.is_active
        logger.info('[SUCCESS][SERIALIZE] {} - {}'.format(reference, label))
        return self.model(reference=reference, label=label, slug=slug, is_active=is_active, activity=activity)
