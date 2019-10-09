"""
    Project GraphQL form converter
    ==============================

    This module define form converter helpers allowing to convert specific form fields to the
    appropriate representation on the GraphQL side.

"""

import graphene
from django import forms
from graphene_django.forms.converter import convert_form_field


@convert_form_field.register(forms.MultipleChoiceField)
def convert_form_muliple_choice_field_to_string_list(field):
    return graphene.List(graphene.String, description=field.help_text, required=field.required)
