from datetime import datetime, timedelta
import time
from dbconnector import get_keep_alive
from configuration import get_config
from logger import logging_handler
from send_mail import send_mail

failure = False
sleep_time = 30
fail_sleep_time = 2
keep_alive_threshold = 3000
owner = get_config('owner')


def check_time_delta(keep_alive_ts):
    s2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_format = "%Y-%m-%d %H:%M:%S"
    return datetime.strptime(s2, time_format) - datetime.strptime(keep_alive_ts, time_format)

if __name__ == '__main__':
    while 1 == 1:
        keep_alive_ts = get_keep_alive()['time_stamp']
        time_delta = check_time_delta(keep_alive_ts)
        logging_handler(str(time_delta))
        if time_delta > timedelta(minutes=keep_alive_threshold):
            failure = True
            msg = '{} {} {}'.format('No keep alive for over', keep_alive_threshold, 'minutes')
            logging_handler(msg)
            send_mail(send_to=owner, subject='Start up Message', text=msg)
            time.sleep(fail_sleep_time)
        else:
            logging_handler('Keep alive successful')
            time.sleep(sleep_time)