from django import template

register = template.Library()


@register.filter
def get(d, key):
    return d.get(key, '')


@register.filter
def meta(model):
    return model._meta
