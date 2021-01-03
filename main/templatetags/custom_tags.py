from django import template

register = template.Library()


@register.filter(name='is_string')
def is_string(value):
    return isinstance(value, str)
