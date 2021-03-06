from django import template


register = template.Library()


@register.inclusion_tag(('types/icon.html'))
def node_type_icon(choice, size):
    return {
        'choice': choice,
        'size': size,
    }
