# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegistrationView(CreateView):
    queryset = Profile.objects
    form_class = UserCreationForm
    template_name = 'accounts/register.html'

    def get_success_url(self):
        return reverse('home.page')


def user_profile(request):
    return HttpResponse(_('Dashboard'))
