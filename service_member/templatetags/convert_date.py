from django import template
import jalali
import datetime

register = template.Library()


def convert_day(value):
    return convert_week_day("WeekDay.{}".format(value))


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
    return res_arr[0] + "/" + res_arr[1] + "/" + res_arr[2]


def get_datetime_relative_str(value):
    if value is None:
        return ""
    elif value.date() != datetime.datetime.now().date():
        return "در تاریخ " + convert_date(value.date())
    elif value.time().hour != datetime.datetime.now().time().hour:
        return str(datetime.datetime.now().time().hour - value.time().hour) + " ساعت پیش"
    elif value.time().minute != datetime.datetime.now().time().minute:
        return str(datetime.datetime.now().time().minute - value.time().minute) + " دقیقه پیش"
    else:
        return "جخ تازه"


register.filter('convert_week_day', convert_week_day)
register.filter('convert_date', convert_date)
register.filter('convert_day', convert_day)
register.filter('get_datetime_relative_str', get_datetime_relative_str)

