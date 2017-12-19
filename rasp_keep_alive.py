import datetime
import requests
import time
from logger import logging_handler
time_sleep = 60

url = 'https://raspgen-keep-alive.herokuapp.com/keep_alive'


def get_current_time():
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp


def get_request(url):
    r = requests.get(url)
    return r.status_code


if __name__ == '__main__':
    while 1 == 1:
        status_code = get_request(url)
        if status_code == 200:
            msg1 = '{} {}'.format('Keep alive success. Status code is', status_code)
            msg2 = '{} {} {}'.format('Going to sleep for', time_sleep, 'seconds')
            logging_handler(msg1)
            logging_handler(msg2)
            time.sleep(time_sleep)
        else:
            msg1 = '{} {}'.format('Keep alive failure. Status code is', status_code)
            msg2 = '{} {} {}'.format('Going to sleep for', time_sleep, 'seconds')
            logging_handler(msg1)
            logging_handler(msg2)
            time.sleep(time_sleep)
