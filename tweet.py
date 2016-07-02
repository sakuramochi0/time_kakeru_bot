#!/usr/bin/env python3
import datetime
from dateutil.parser import parse
import argparse

from get_tweepy import *

def tweet(date=None):
    if date:
        date = parse(date).date() - datetime.timedelta(days=1)
    else:
        date = datetime.date.today() - datetime.timedelta(days=1)
        
    if end_of_century(date):
        end = end_of_century(date)
    elif end_of_year(date):
        end = end_of_year(date)
    elif end_of_month(date):
        end = end_of_month(date)
    elif end_of_week(date):
        end = end_of_week(date)
    elif end_of_holiday(date):
        end = end_of_holiday(date)
    else:
        end = ''

    if end:
        status = '{}は……死んだ……'.format(end)
        api.update_status(status=status)

def end_of_century(date):
    year = date.year
    if (year + 1) % 100 == 0 and date == datetime.date(year, 12, 31):
        return '{}世紀'.format((year + 1) // 100)
    
def end_of_year(date):
    if date == datetime.date(date.year, 12, 31):
        return '{}年'.format(date.year)
    else:
        return False

def end_of_month(date):
    if (date + datetime.timedelta(days=1)).day == 1:
        return '{}年{}月'.format(date.year, date.month)
    else:
        return False

def week_of_month(date):
    date_week = date.isocalendar()[1]
    first_day_of_month_week = date.replace(day=1).isocalendar()[1]
    week = date_week - first_day_of_month_week + 1
    if week > 0:
        return week
    else: # if first day is 53th week of the year
        return week + first_day_of_month_week

def end_of_week(date):
    if date.weekday() == 6:
        return '{}年{}月の第{}週'.format(date.year, date.month, week_of_month(date))
    else:
        return False

def end_of_holiday(date):
    return False
        
if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--date')

    args = parser.parse_args()
     
    # get tweepy api
    if args.debug:
        api = get_api('sakuramochi_pre')
    else:
        api = get_api('time_kakeru_bot')

    tweet(args.date)
