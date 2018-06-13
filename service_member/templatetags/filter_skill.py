from django import template

register = template.Library()


def filter_accepted(value):
    return value.filter(validation_status='ValidationStatus.Act')


def filter_by_name(value, arg):
    return value.filter(skill_type__name=arg)


def get_names(value):
    ans = []
    for has_skill in value:
        ans.append(has_skill.skill_type.name)
    return ans


register.filter('filter_accepted', filter_accepted)
register.filter('filter_by_name', filter_by_name)
register.filter('get_names', get_names)
