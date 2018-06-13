from django import template

register = template.Library()


def filter_accepted(value):
    return value.filter(validation_status='ValidationStatus.Act')


register.filter('filter_accepted', filter_accepted)
