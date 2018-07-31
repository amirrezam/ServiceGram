from django import template

from service_requirement.models import HelpNonCash

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


def get_conflicts_non_cash_requirement(value, arg):
    if value.filter(requirement__time__exact=arg.time,
                    requirement__week_day=arg.week_day,
                    requirement__beginning_date__gte=arg.beginning_date,
                    requirement__beginning_date__lte=arg.ending_date,
                    status='ValidationStatus.Act').count() > 0:
        return True

    if value.filter(requirement__time__exact=arg.time,
                    requirement__week_day=arg.week_day,
                    requirement__ending_date__gte=arg.beginning_date,
                    requirement__ending_date__lte=arg.ending_date,
                    status='ValidationStatus.Act').count() > 0:
        return True

    if value.filter(requirement__time__exact=arg.time,
                    requirement__week_day=arg.week_day,
                    requirement__beginning_date__lte=arg.beginning_date,
                    requirement__ending_date__gte=arg.ending_date,
                    status='ValidationStatus.Act').count() > 0:
        return True


def get_institute_mean_score(value):
    sum = 0
    cnt = 0
    for non_cash_requirement in value.non_cash_requirements.all():
        for help_non_cash in non_cash_requirement.helps.all():
            if help_non_cash.institute_score != -1:
                sum += help_non_cash.institute_score
                cnt += 1
    if cnt == 0:
        return 2.5
    else:
        return sum / cnt


def get_benefactor_mean_score(value):
    sum = 0
    cnt = 0
    for help_non_cash in value.non_cash_helps.all():
        if help_non_cash.benefactor_score != -1:
            sum += help_non_cash.benefactor_score
            cnt += 1
    if cnt == 0:
        return 2.5
    else:
        return sum / cnt


def convert_int(value):
    return int(value)


def get_total_donation(cash_requirement):
    s = 0
    for help_cash in cash_requirement.helps.all():
        s += help_cash.amount
    return s


def sort_by(value, arg):
    return value.order_by(arg)


def divide(value, arg):
    if value > arg:
        return 100
    return int(100 * value/arg)


def get_all(value):
    return value.all()


register.filter('filter_accepted', filter_accepted)
register.filter('filter_has_skill_accepted', filter_has_skill_accepted)
register.filter('filter_by_name', filter_by_name)
register.filter('filter_by_date', filter_by_date)
register.filter('filter_by_time', filter_by_time)
register.filter('filter_by_username', filter_by_username)
register.filter('get_names', get_names)
register.filter('get_conflicts_non_cash_requirement', get_conflicts_non_cash_requirement)
register.filter('get_institute_mean_score', get_institute_mean_score)
register.filter('get_benefactor_mean_score', get_benefactor_mean_score)
register.filter('convert_int', convert_int)
register.filter('get_total_donation', get_total_donation)
register.filter('sort_by', sort_by)
register.filter('divide', divide)
register.filter('get_all', get_all)
