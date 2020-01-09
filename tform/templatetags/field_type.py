from django import template
from tform.models import TextField, McqField, McqChoiceField

register = template.Library()

@register.filter
def field_type(value):
    if type(value) is TextField:
        return 'TextField'
    elif type(value) is McqField:
        return 'McqField'
    elif type(value) is McqChoiceField:
        return 'McqChoiceField'
