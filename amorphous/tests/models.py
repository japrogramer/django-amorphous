# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.postgres.fields import JSONField


class TestModel(models.Model):
    # we only need one field
    metadata = JSONField(default=dict())

    def get_absolute_url(self):
        return '/one/'
