from django import template

register = template.Library()

@register.filter
def return_item(l, key):
    try:
        return l.get(key)
    except:
        return None
