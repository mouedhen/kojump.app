# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.db import models


@python_2_unicode_compatible
class TimeInterval(models.Model):

    WEEK_DAYS = (
        ('MON', _('Lundi')),
        ('TUE', _('Mardi')),
        ('WED', _('Mercredi')),
        ('THU', _('Jeudi')),
        ('FRI', _('Vendredi')),
        ('SAT', _('Samedi')),
        ('SUN', _('Dimanche')),
    )

    day = models.CharField(_('jour de la semaine'), max_length=3, choices=WEEK_DAYS)
    start_time = models.TimeField(_('heure début'))
    end_time = models.TimeField(_('heure fin'))

    def __str__(self):
        return '{}: from {} to {}'.format(self.day, self.start_time, self.end_time)
