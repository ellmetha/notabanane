from collections import namedtuple

from django import forms

from notabanane.common.db.models.fields import ChoiceArrayField


class TestChoiceArrayField:
    def test_formfield_returns_a_multiple_choice_form_field(self):
        TestField = namedtuple('TestField', ['choices'])
        field = TestField(choices=[('', 'Default'), ('c1', 'Choice 1')])
        formfield = ChoiceArrayField(field).formfield()
        assert isinstance(formfield, forms.MultipleChoiceField)
        assert formfield.choices == [('', 'Default'), ('c1', 'Choice 1')]
