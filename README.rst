    django-amorphous allows you to store data that you would normally need to
create models for and run migrations against, if there are changes to that
data's structure, in a single JsonField.

    Amorphous makes this possible by defining a data structure that stores the 
fields type and data, as well as any kwargs that are used to instantiate the 
field.

    An example:
    First import the class generator
    >>> from amorphous.forms import amorphous_gen

    Than define the structure of the data
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
    requests and a form instance initialized with data from the DB
    >>> form_class = amorphous_gen(amorphous=json_data)
    >>> form_instance = form_class()
    >>> form_instance = form_class(data=obj.field)

    To store the data, in the format expected by amorphous use the db_amorphous
    form method
    >>> for_db = form.db_amorphous()
    save the object after setting the attribute, where amorphous_field is the
    name of the field that holds the amorphous data on the model
    >>> setattr(model_object, amorphous_field, for_db)


