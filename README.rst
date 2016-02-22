***********************************************
django-amorphous unlocks the power of JsonField
***********************************************

=============
Main Features
=============

django-amorphous allows you to store data that you would normally need to
create models for and run migrations against, if there are changes are made to
their structure, in a **single** JsonField.

Amorphous makes this possible by defining a data structure that stores the
fields type and data, as well as any kwargs that are used to instantiate the
field.

===========
An example:
===========

the code:

.. code-block:: python

    # First import the class generator
    >>> from amorphous.forms import amorphous_gen

    # Than define the structure of the data
    >>> json_data = {
            'first': [
                'BooleanField',
                {
                    'initial': True,
                    'required': False}, ],
            'second': [
                'CharField',
                {'initial': 'This is a test'}]}

Finally generate the form class from there you have two choices:
create an instance of that class
or create a  form with initial values set  with data from the DB:

.. code-block:: python

    >>> form_class = amorphous_gen(amorphous=json_data)
    >>> form_instance = form_class()
    # Using data from object in DB.
    # This creates a form class where the initial values are the values stored
    # in the DB
    # Note: the form is not bound
    >>> form_instance = amorphous_gen(obj.field)
    # this is usefull when dealing with post and get methods


To store the data, in the format expected by amorphous use the db_amorphous
form method:

.. code-block:: python

    >>> for_db = form.db_amorphous()

save the object after setting the attribute, where amorphous_field is the
name of the field that holds the amorphous data on the model:

.. code-block::python

   >>> setattr(model_object, amorphous_field, for_db)

=====
Usage
=====

amorphous contains a CBV, AmorphousView that takes the name of the JsonField
that you wish to store the amorphous data into **amorphous_field** and also
expects the model attribute to be set:

.. code-block:: python

    >>> view = AmorphousView.as_view(
        template_name='amorphous_test/model_amo.html',
        model=TestModel,
        form_class=self.test_form_class,
        amorphous_field='metadata')

This view takes care of displaying, validating and saving the form as expected
and certain methods can be overridden to add or remove functionality like in any
CBV.

=====
Tests
=====
running tests:

.. code-block:: bash

    $ manage.py test amorphous

=================
The possibilities
=================

With this package, you can store different schemas in the same field.
Lets say that one of the data structures you have been storing has changed
but only new data uses the new schema and the old data doesn't need a migration.

Since the Form class is generated on the fly and assuming no restraints are
applied to the JsonField to be used amorphously, the Form can adapt depending on
what version is being used. Consider how the form structure is stored, because of
this, the behavior of having multiple schemas per amorphous field comes nearly
free.

In the real world, this can be used to create a tag, category, or even a
language translation system. Since for this apps you would need to add or remove
items to them dynamically, and a schema binded implementation would make their
implementation difficult. However with an amorphous field, they become trivial.
