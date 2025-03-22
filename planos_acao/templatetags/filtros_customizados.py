import unicodedata
from django import template

register = template.Library()

@register.filter
def remove_acentos(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value) if not unicodedata.combining(c))
