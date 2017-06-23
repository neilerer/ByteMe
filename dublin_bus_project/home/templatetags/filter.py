from django import template

register = template.Library()
#functions for accessing dictionary values in index.html
@register.filter
def keyvalue_lat(dict, key):
    return dict[str(key)][0]

@register.filter
def keyvalue_long(dict, key):
    return dict[str(key)][1]
