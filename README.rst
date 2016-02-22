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
or form a instance initialized with data from the DB:

.. code-block:: python

    >>> form_class = amorphous_gen(amorphous=json_data)
    >>> form_instance = form_class()
    >>> form_instance = form_class(data=obj.field)

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
