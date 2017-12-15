from datetime import datetime, timedelta
import time
from dbconnector import get_keep_alive
from logger import logging_handler

failure = False
sleep_time = 30
keep_alive_threshold = 10


def check_time_delta(keep_alive_ts):
    s2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(s2, time_format) - datetime.strptime(keep_alive_ts, time_format)

if __name__ == '__main__':
    while not failure:
        keep_alive_ts = get_keep_alive()['time_stamp']
        time_delta = check_time_delta(keep_alive_ts)
        logging_handler(str(time_delta))
        if time_delta > timedelta(minutes=keep_alive_threshold):
            failure = True
            logging_handler('No keep alive for over 10 minutes')
        else:
            logging_handler('Keep alive successful')
            time.sleep(30)