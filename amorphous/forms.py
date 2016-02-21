# -*- coding: utf-8 -*-
from django import forms


class AmorphousForm(forms.Form):
    amorphous = None

    def _db_field_data(self):
        new_amorphous = self.amorphous
        if self.amorphous is not None:
            for key, _ in self.fields.items():
                value = self.amorphous[key]
                rhs = value[1]
                rhs['initial'] = self.cleaned_data[key]
                new_amorphous[key][1] = rhs
        return new_amorphous

    def db_amorphous(self):
        # print(self.cleaned_data)
        return self._db_field_data()


def amorphous_gen(amorphous=None, form=AmorphousForm):
    # in this function i will set the attributes to the form and return
    # the form
    setattr(form, 'amorphous', amorphous)

    fields = []
    declared_fields = []
    for key, value in amorphous.items():
        fields.append(key)

        field_type = value[0]
        field_kwargs = value[1]
        field_instance = getattr(forms, field_type, None)(**field_kwargs)
        declared_fields.append((key, field_instance))

    setattr(form, 'declared_fields', declared_fields)

    attrs = {'fields': fields}

    # If parent form class already has an inner Meta, the Meta we're
    # creating needs to inherit from the parent's inner meta.
    parent = (object,)
    if hasattr(form, 'Meta'):
        parent = (form.Meta, object)
    Meta = type(str('Meta'), parent, attrs)

    # Give this new form class a reasonable name.
    class_name = form.__name__

    # Class attributes for the new form class.
    form_class_attrs = {
        'Meta': Meta,
    }

    # return the generated class
    # Instantiate type(form) in order to use the same metaclass as form.
    return type(form)(class_name, (AmorphousForm,), form_class_attrs)
