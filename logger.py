import datetime
import time
import logging


def get_current_time():
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp


def logging_handler(msg):
    send_out_msg = '{} {}'.format(get_current_time(), msg)
    print(send_out_msg)
    logging.info(send_out_msg)