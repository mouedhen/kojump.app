# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

from django.contrib.auth.models import User


GENDER_CHOICES = (
    ('M', _('Homme')),
    ('F', _('Femme')),
    ('N', _('Non spécifié')),
)


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='profile')

    phone_number = models.CharField(_('téléphone'), max_length=16, blank=True, null=True)
    mobile_number = models.CharField(_('mobile'), max_length=16, blank=True, null=True)
    fax_number = models.CharField(_('fax'), max_length=16, blank=True, null=True)

    street_address = models.CharField(_('adresse (1ère ligne)'), max_length=254, blank=True)
    street_address2 = models.CharField(_('adresse (2ème ligne)'), max_length=254, blank=True)
    postal_code = models.CharField(_('code postal'), max_length=10, blank=True)
    city = models.CharField(_('ville'), max_length=100, blank=True)
    country = models.CharField(_('pays'), max_length=100, blank=True)

    photo = models.ImageField(_('Image de profil'), upload_to='users/%Y/%m/%d', blank=True)
    birth_date = models.DateField(_('date de naissance'), blank=True, null=True)
    gender = models.CharField(_('sexe'), max_length=1, choices=GENDER_CHOICES, default='N')
    bio = models.TextField(_('biographie'), max_length=1024, null=True, blank=True)

    email_confirmed = models.BooleanField(_('adresse e-mail confirmé ?'), default=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'profil utilisateur'
        verbose_name_plural = 'profils utilisateurs'
