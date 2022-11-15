import time
from datetime import datetime, timedelta


def get_before_today_start_timestamp(days):
    d = datetime.today().date() - timedelta(days=days)
    dt = int(time.mktime(time.strptime(str(d), '%Y-%m-%d')))
    return dt


def get_before_today_end_timestamp(days):
    d = datetime.today().date() - timedelta(days=days-1)
    dt = int(time.mktime(time.strptime(str(d), '%Y-%m-%d')))
    return dt
