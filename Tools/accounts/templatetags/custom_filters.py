from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.filter
def get_url(module):
    try:
        return reverse(module.url_name)
    except NoReverseMatch:
        return '#'
    
@register.filter
def startswith(text, starts):
    if isinstance(text, str) and isinstance(starts, str):
        return text.startswith(starts)
    return False