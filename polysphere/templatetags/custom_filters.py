from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)

@register.filter
def enumerate_filter(iterable):
    return enumerate(iterable)

@register.filter
def tuple_in_positions(pos_tuple, positions):
    return any(pos_tuple in pos_list for pos_list in positions.values())