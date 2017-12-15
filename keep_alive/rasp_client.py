import datetime
import requests
import time
from logger import logging_handler


url = 'http://0.0.0.0:5000/keep_alive'


def get_current_time():
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp


def get_request(url):
    r = requests.get(url)
    return r.status_code


if __name__ == '__main__':
    status_code = get_request(url)
    if '200' in status_code:
        logging_handler('{} {}'.format('something', 'something else'))
