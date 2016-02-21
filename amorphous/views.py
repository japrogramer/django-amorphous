# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.detail import SingleObjectMixin, SingleObjectTemplateResponseMixin
from django.views.generic.edit import FormMixin, ProcessFormView
from django.http import HttpResponseRedirect
from django.core.exceptions import ImproperlyConfigured

from .forms import amorphous_gen


class BaseAmorphousMixin(SingleObjectMixin, FormMixin):
    # amorphous_gen = amorphous_gen

    def form_valid(self, form):
        # this is the data that will be stored in the models amorphous_field
        for_db = form.db_amorphous()

        # save the object after setting the attribute
        setattr(self.object, self.amorphous_field, for_db)
        self.object.save()

        # do as super would and redirect to a success
        return HttpResponseRedirect(self.get_success_url())

    def get_form_class(self):
        return amorphous_gen(amorphous=self.get_amorphous_data())

    def get_amorphous_field(self):
        if self.amorphous_field:
            return self.amorphous_field
        else:
            raise ImproperlyConfigured

    def get_amorphous_data(self):
        data = {}
        if hasattr(self, 'object') and self.object is not None:
                data = getattr(self.object, self.get_amorphous_field(), '')
        return data

    def get_success_url(self):
        """
        Returns the supplied URL.
        """
        if self.success_url:
            url = self.success_url.format(**self.object.__dict__)
        else:
            try:
                url = self.object.get_absolute_url()
            except AttributeError:
                raise ImproperlyConfigured(
                    "No URL to redirect to.  Either provide a url or define"
                    " a get_absolute_url method on the Model.")
        return url


class BaseAmorphousView(BaseAmorphousMixin, ProcessFormView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class AmorphousView(SingleObjectTemplateResponseMixin, BaseAmorphousView):
    template_name_suffix = '_amorphous'
    amorphous_field = None
