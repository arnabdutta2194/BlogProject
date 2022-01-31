from urllib.parse import quote_plus
from django import template

register = template.Library()

#--- This Filter Can Be Used Inside Templates
@register.filter
def urlify(value):
    return quote_plus(value)