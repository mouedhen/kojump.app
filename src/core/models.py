# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from slugify import slugify
from django.db import models


class SluggedModel(models.Model):
    label = models.CharField(_('label'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150)

    def generate_slug(self):
        self.slug = slugify(self.label)

    class Meta:
        abstract = True


class DescribedModel(models.Model):
    description = models.TextField(_('description'))

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    created = models.DateTimeField(_('date de création'), auto_now_add=True)
    modified = models.DateTimeField(_('date de modification'), auto_now=True)

    class Meta:
        abstract = True


class ActivatedModel(models.Model):
    is_active = models.BooleanField(_('activer ?'), default=False)

    class Meta:
        abstract = True
