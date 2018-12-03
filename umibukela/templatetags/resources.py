from django import template

register = template.Library()


@register.filter
def type(resource, resource_type):
    """
    We need to check if a specific resource type is greater that 3
    """
    count = 0
    for r in resource:
        if r.resource.name == resource_type:
            count += 1
    return count
