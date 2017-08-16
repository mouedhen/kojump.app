# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.contrib.auth.models import User
from .models import Profile

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        UserProfileInline
    ]
