from django import template
import jalali

register = template.Library()


def convert_week_day(value):
    if value == 'WeekDay.Sat':
        return 'شنبه'
    if value == 'WeekDay.Sun':
        return 'یکشنبه'
    if value == 'WeekDay.Mon':
        return 'دوشنبه'
    if value == 'WeekDay.Tue':
        return 'سه‌شنبه'
    if value == 'WeekDay.Wed':
        return 'چهارشنبه'
    if value == 'WeekDay.Thu':
        return 'پنجشنبه'
    if value == 'WeekDay.Fri':
        return 'جمعه'


def convert_date(date):
    date_str = date.strftime('%Y-%m-%d')
    res = jalali.Gregorian(date_str).persian_string()
    res_arr = res.split('-')
    return res_arr[2] + "-" + res_arr[1] + "-" + res_arr[0]


register.filter('convert_week_day', convert_week_day)
register.filter('convert_date', convert_date)
