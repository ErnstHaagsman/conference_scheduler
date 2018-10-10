import pytz


def force_tz(date, tz):
    naive_date = date.replace(tzinfo=None)
    return pytz.timezone(tz).localize(naive_date)