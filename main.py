import os.path
import imaplib
import logging
import re
import time
import datetime
from dbconnector import set_gen_state
from configuration import get_config, get_white_list
import RPi.GPIO as GPIO

receiver_email = get_config('email')
receiver_password = get_config('password')
sleep_time = int(get_config('sleep_time'))
ts = time.time()
time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
dir_path = os.path.dirname(os.path.realpath(__file__))
file_logging_path = os.path.join(dir_path, 'generator.log')
logging.basicConfig(filename=file_logging_path,level=logging.INFO)

pin = 2


def generator_cmd(cmd):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    if cmd == 'on':
        GPIO.output(pin, False)
    elif cmd == 'off':
        GPIO.output(pin, True)


def delete_messages():
    msrvr.select('Inbox')
    typ, data = msrvr.search(None, 'ALL')
    for num in data[0].split():
       msrvr.store(num, '+FLAGS', '\\Deleted')
    msrvr.expunge()


def get_body(cnt):
    cnt, data = msrvr.fetch(cnt[0], '(UID BODY[TEXT])')
    return data[0][1]


def get_sender():
    from_data = msrvr.fetch(cnt[0], '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
    header_data = from_data[1][0][1]
    return ''.join(re.findall(r'<(.+?)>', header_data))


def is_in_white_list(from_address):
    if from_address in get_white_list():
        return True
    else:
        return False


if __name__ == '__main__':
    msrvr = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    msrvr.login(receiver_email, receiver_password)
    i = 1
    while i == 1:
        try:
            stat, cnt = msrvr.select('Inbox')
            body = get_body(cnt)
            from_address = get_sender()
            if is_in_white_list(from_address):
                print("{} {} {}".format(time_stamp, from_address, "is in the white list"))
                logging.info("{} {} {}".format(time_stamp, from_address, "is in the white list"))
                if 'off' in body:
                    generator_cmd(cmd='off')
                    set_gen_state(True)
                    print("Generator is going down")
                    logging.info("Generator is going down")
                elif 'on' in body:
                    generator_cmd(cmd='on')
                    set_gen_state(True)
                    print("Generator is going up")
                    logging.info("Generator is going up")
            else:
                print("{} {}".format(from_address,"is not in the white list"))
                logging.info("{} {}".format(from_address,"is not in the white list"))
            delete_messages()
            time.sleep(sleep_time)
        except:
            print("{} {}".format(time_stamp, "No mails"))
            logging.info("{} {}".format(time_stamp, "No mails"))
            time.sleep(sleep_time)
    msrvr.close()
    msrvr.logout()
