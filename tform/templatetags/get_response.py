from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()


@register.simple_tag(takes_context=True)
def get_response(context, value):
    try:
        response = value.get(form_response=context['response'])
    except ObjectDoesNotExist:
        return ""
    return response
