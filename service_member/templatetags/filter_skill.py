from django import template

register = template.Library()


def filter_accepted(value):
    return value.filter(validation_status='ValidationStatus.Act')


def filter_has_skill_accepted(value):
    return value.filter(status='ValidationStatus.Act')


def filter_by_name(value, arg):
    return value.filter(skill_type__name=arg)


def filter_by_date(value, arg):
    return value.filter(requirement__date__exact=arg)


def filter_by_time(value, arg):
    return value.filter(requirement__time__exact=arg)


def filter_by_username(value, arg):
    return value.filter(benefactor__member__username__exact=arg)


def get_names(value):
    ans = []
    for has_skill in value:
        ans.append(has_skill.skill_type.name)
    return ans


register.filter('filter_accepted', filter_accepted)
register.filter('filter_has_skill_accepted', filter_has_skill_accepted)
register.filter('filter_by_name', filter_by_name)
register.filter('filter_by_date', filter_by_date)
register.filter('filter_by_time', filter_by_time)
register.filter('filter_by_username', filter_by_username)
register.filter('get_names', get_names)
