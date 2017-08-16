# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.gis.db import models


@python_2_unicode_compatible
class GeoLocation(models.Model):

    street_address = models.CharField(_('adresse (1ère ligne)'), max_length=254, blank=True)
    street_address2 = models.CharField(_('adresse (2ème ligne)'), max_length=254, blank=True)
    postal_code = models.CharField(_('code postal'), max_length=10, blank=True)
    city = models.CharField(_('ville'), max_length=100, blank=True)
    country = models.CharField(_('pays'), max_length=100, blank=True)

    gps_coordinates = models.PointField(_('coordonnées GPS'))

    class Meta:
        verbose_name = _('emplacement géographique')
        verbose_name_plural = _('emplacements géographiques')
        abstract = True

    def __str__(self):
        return str(self.gps_coordinates)
