# -*- coding: utf-8 -*-
from django.apps import AppConfig


# Because i don't want to have my test models
# show up in production
class AmorphousTestConfig(AppConfig):
    name = 'amorphous.tests'
    verbose_name = 'Tests for Amorphous'
