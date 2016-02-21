# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from django.apps import apps
from amorphous.forms import amorphous_gen
from amorphous.views import AmorphousView
from amorphous.tests.models import TestModel


class TestAmorphousForm(TestCase):

    def setUp(self):
        self.json_data = {
                'first': [
                    'BooleanField',
                    {
                        'initial': True,
                        'required': False}, ],
                'second': [
                    'CharField',
                    {'initial': 'This is a test'}]}

        self.data = {
                'first': False,
                'second': 'new text'}

        self.test_form_class = amorphous_gen(amorphous=self.json_data)

    def test_creates_fields(self):
        test_form = self.test_form_class()
        ordered = test_form.fields
        for key, value in ordered.items():
            json_initial = self.json_data[key][1]
            self.assertEqual(value.initial, json_initial['initial'])

    def test_form_validates(self):
        test_form = self.test_form_class(self.data)
        self.assertTrue(test_form.is_bound)
        self.assertTrue(test_form.is_valid())

    def test_forms_output(self):
        test_form = self.test_form_class(self.data)
        self.assertTrue(test_form.is_valid())
        # get the data that would be written to the db
        db_data = test_form.cleaned_data
        test_2form = self.test_form_class(db_data)
        self.assertTrue(test_2form.is_valid())
        self.assertEqual(db_data, test_2form.cleaned_data)

    def test_db_amorphous(self):
        test_form = self.test_form_class(self.data)
        self.assertTrue(test_form.is_valid())
        db_data = test_form.db_amorphous()
        for key, value in self.json_data.items():
            self.assertTrue(key in db_data)


class TestAmorphousView(TestCase):

    def setUp(self):
        self.json_data = {
                'first': [
                    'BooleanField',
                    {
                        'initial': True,
                        'required': False}, ],
                'second': [
                    'CharField',
                    {'initial': 'This is a test'}]}

        self.data = {
                'first': False,
                'second': 'new text'}

        self.test_form_class = amorphous_gen(amorphous=self.json_data)
        self.test_model = TestModel.objects.create(metadata=self.json_data)
        self.factory = RequestFactory()

    def test_view(self):
        request = self.factory.get('/?pk=%s' % self.test_model.pk)

        # lets make a view
        view = AmorphousView.as_view(
                template_name='amorphous_test/model_amo.html',
                model=TestModel,
                form_class=self.test_form_class,
                amorphous_field='metadata')
        response = view(request, **request.GET.dict())

        # assert view is processed correctly
        self.assertEqual(response.status_code, 200)

        # this is the post response part
        data = self.data
        request_post = self.factory.post('/?pk=%s' % self.test_model.pk, data)
        response_post = view(request_post, **{**request_post.GET.dict(), **request_post.POST.dict()})
        changed_object = TestModel.objects.get(pk=self.test_model.pk).metadata
        # Did the view make the changes?
        self.assertEqual(response.status_code, 200)
        for key, value in self.data.items():
            self.assertEqual(self.data[key], changed_object[key][1]['initial'])
