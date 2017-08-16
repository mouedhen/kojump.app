# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('street_address', 'street_address2', 'postal_code',
                  'city', 'country', 'photo', 'birth_date', 'gender')
