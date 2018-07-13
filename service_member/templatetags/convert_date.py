from django import template

register = template.Library()


def convert_week_day(value):
    if value == 'WeekDay.Sat':
        return 'شنبه'
    if value == 'WeekDay.Sun':
        return '۱شنبه'
    if value == 'WeekDay.Mon':
        return '۲شنبه'
    if value == 'WeekDay.Tue':
        return '۳شنبه'
    if value == 'WeekDay.Wed':
        return '۴شنبه'
    if value == 'WeekDay.Thu':
        return '۵شنبه'
    if value == 'WeekDay.Fri':
        return 'جمعه'


register.filter('convert_week_day', convert_week_day)