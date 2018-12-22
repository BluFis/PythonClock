# coding:UTF-8
import requests
import datetime,time


def get_time():
    time_url = 'http://api.k780.com:88/?app=life.time&appkey=10003&sign=b59bc3ef6191eb9f747dd4e83c99f2a4&format=json'
    try:
        response = requests.get(time_url)
        if response.status_code == 200:
            present_time = {
                'datetime': response.json()['result']['datetime_1'],
                'dayOfWeek': response.json()['result']['week_2']
            }
            return present_time
        else:
            get_local_time()
    except:
        get_local_time()


def get_local_time():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    day_of_week = get_week_day(datetime.datetime.now())
    present_time = {
        'datetime': now_time,
        'dayOfWeek': day_of_week
    }
    return present_time

def get_week_day(date):
   week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
   }
   day = date.weekday()
   return week_day_dict[day]

get_time()