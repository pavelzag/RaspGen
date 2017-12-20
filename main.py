from dbconnector import set_gen_state, get_gen_state, get_time_spent, set_initial_db_state, set_time_spent
from configuration import get_config, get_white_list, get_pin
from logger import logging_handler
from send_mail import send_mail
import datetime
import email
import imaplib
import logging
from os import path, uname
import re
import socket
import time

imap_addr = 'imap.gmail.com'
imap_port = 993
receiver_email = get_config('email')
receiver_password = get_config('password')
owner = get_config('owner')
sleep_time = int(get_config('sleep_time'))
dir_path = path.dirname(path.realpath(__file__))
file_logging_path = path.join(dir_path, 'generator.txt')
logging.basicConfig(filename=file_logging_path,level=logging.INFO)
down_msg = 'Generator is going down.'
up_msg = 'Generator is going up.'
already_up_msg = 'Generator is already up.'
already_down_msg = 'Generator is already down.'
debug_message = 'Debugging message.'
not_white_list = 'is not in the white list.'
white_list = 'is in the white list.'
pin = int(get_pin())


def generator_cmd(cmd):
    if uname()[1] == 'DietPi':
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        if cmd == 'on':
            GPIO.output(pin, False)
        elif cmd == 'off':
            GPIO.output(pin, True)
    else:
        logging_handler('test mode. generator is not going up')


def delete_messages():
    msrvr.select('Inbox')
    typ, data = msrvr.search(None, 'ALL')
    for num in data[0].split():
       msrvr.store(num, '+FLAGS', '\\Deleted')
    msrvr.expunge()


def get_machine_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_key_command(cnt):
    count, data = msrvr.fetch(cnt[0], '(UID BODY[TEXT])')
    for i in cnt:
        typ, msg_data = msrvr.fetch(str(i), '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
    body = get_body_word(data[0][1])
    subject = msg['subject'].lower()
    return subject, body


def get_if_same_status():
    pass


def get_sender():
    from_data = msrvr.fetch(cnt[0], '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
    header_data = from_data[1][0][1]
    return ''.join(re.findall(r'<(.+?)>', header_data))


def get_body_word(body):
    cut_word = re.findall(r'^.*$', body, re.MULTILINE)[3][:-1].lower()
    return cut_word


def get_current_time(date=False, datetime_format=False):
    ts = time.time()
    if not date:
        if datetime_format:
            time_stamp = datetime.datetime.fromtimestamp(ts)
        else:
            time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    else:
        if datetime_format:
            time_stamp = datetime.datetime.fromtimestamp(ts)
        else:
            time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    return time_stamp



def calculate_time_span(time_span):
    #TODO Add Hours
    if time_span > 60:
        return time.strftime("%M:%S", time.gmtime(time_span)), 'minutes'
    else:
        return int(time_span), 'seconds'


def is_in_white_list(mail_sender):
    if mail_sender in get_white_list():
        return True
    else:
        return False


def has_numbers(string):
    return any(char.isdigit() for char in string)


def extract_timeout_frame(command):
    return int(command.split("on",1)[1])


def chop_microseconds(timeframe):
    return timeframe - datetime.timedelta(microseconds=timeframe.microseconds)


def calculate_daily_usage(month):
    time_spent = get_time_spent(12)
    return time_spent


if __name__ == '__main__':
    ip_address = get_machine_ip()
    startup_msg = '{} {}'.format('Machine runs on', ip_address)
    print(startup_msg)
    logging.info(startup_msg)
    send_mail(send_to=owner, subject='Start up Message', text=startup_msg)
    set_initial_db_state()
    start_time = None
    end_time = None
    i = 1
    while i == 1:
        try:
            uname_debug = 'DietPi'
            msrvr = imaplib.IMAP4_SSL(imap_addr, imap_port)
            login_stat, login_message = msrvr.login(receiver_email, receiver_password)
            if login_stat == 'OK':
                stat, cnt = msrvr.select('Inbox')
                key_command = ''.join(get_key_command(cnt))
                from_address = get_sender()
                if is_in_white_list(from_address):
                    current_state = get_gen_state()
                    logging_handler('{} {}'.format(from_address, white_list))
                    if 'debug' in key_command:
                        print(debug_message)
                        logging.info("{} {}". format(get_current_time(), debug_message))
                        send_mail(send_to=from_address, subject='Debug Message', text=debug_message)
                    elif 'off' in key_command:
                        if get_gen_state() is not 'down':
                            # if uname()[1] == 'DietPi':
                            if uname_debug == 'DietPi':
                                generator_cmd(cmd='off')
                                set_gen_state(state=False, time_stamp=get_current_time())
                                logging_handler(down_msg)
                                end_time = datetime.datetime.now()
                                # Add 2 minutes (???) compensation for going down
                                time_span = int((datetime.datetime.now() - start_time).total_seconds())
                                how_long, units = calculate_time_span(time_span)
                                msg_to_log = '{} {} {}'.format('The generator was up for:', how_long, units)
                                logging_handler(msg_to_log)
                                mail_msg = '{} {}'.format(down_msg, msg_to_log)
                                send_mail(send_to=from_address, subject='Generator Control Message', text=mail_msg)
                                set_time_spent(time_stamp=get_current_time(date=True, datetime_format=True),
                                               time_span=time_span)
                            else:
                                logging_handler('{} {}'.format('This is not a Raspi, this is', uname()[1]))
                        else:
                            logging_handler(already_down_msg)
                    elif 'on' in key_command:
                        if get_gen_state() is not 'up':
                            # if uname()[1] == 'DietPi':
                            if uname_debug == 'DietPi':
                                current_time_stamp = get_current_time()
                                start_time = datetime.datetime.now()
                                if not has_numbers(key_command):
                                    generator_cmd(cmd='on')
                                    logging_handler(up_msg)
                                    set_gen_state(True, time_stamp=get_current_time())
                                    send_mail(send_to=from_address, subject='Generator Control Message', text=up_msg)
                                else:
                                    timeout_frame = extract_timeout_frame(key_command)
                                    timeout_stamp = datetime.datetime.now() + datetime.timedelta(0, 0, 0, 0, timeout_frame)
                                    generator_cmd(cmd='on')
                                    mail_msg = '{} {} {} {}'.format(up_msg, 'for ',
                                                                  timeout_frame, 'minutes')
                                    logger_msg = '{} {} {} {}'.format(up_msg, 'for ',
                                                                  timeout_frame, 'minutes')
                                    logging_handler(logger_msg)
                                    set_gen_state(True, time_stamp=get_current_time())
                                    send_mail(send_to=from_address, subject='Generator Control Message', text=mail_msg)
                                    delete_messages()
                                    while timeout_stamp > datetime.datetime.now():
                                        time_left = timeout_stamp - datetime.datetime.now()
                                        time.sleep(sleep_time)
                                        msg = ('{} {} {}'.format('Generator is on for the next',
                                                                    chop_microseconds(time_left), 'minutes'))
                                        logging_handler(msg)
                                        try:
                                            stat, cnt = msrvr.select('Inbox')
                                            key_command = ''.join(get_key_command(cnt))
                                            if 'off' in key_command:
                                                generator_cmd(cmd='off')
                                                on_time = chop_microseconds(datetime.timedelta(0, 0, 0, 0, timeout_frame) - time_left).seconds
                                                mail_msg = '{} {} {}'.format('Generator is going down after',
                                                                             on_time, 'minutes')

                                                logging_handler(down_msg)
                                                send_mail(send_to=from_address, subject='Generator Control Message',
                                                          text=mail_msg)
                                                set_gen_state(False, time_stamp=get_current_time())
                                                set_time_spent(time_stamp=get_current_time(date=True, datetime_format=True),
                                                               time_span=on_time)
                                                break
                                            elif 'status' in key_command:
                                                if start_time:
                                                    time_span = (datetime.datetime.now() - start_time).total_seconds()
                                                    how_long, units = calculate_time_span(time_span)
                                                    msg = '{} {} {} {} {}'.format('Generator is', get_gen_state(),
                                                                                  'for', how_long, units)
                                                else:
                                                    msg = '{} {}'.format('Generator is', get_gen_state())
                                                logging_handler(msg)
                                                send_mail(send_to=from_address, subject='Status Message', text=msg)
                                                delete_messages()
                                            elif 'log' in key_command:
                                                msg = '{} {} {}'.format(get_current_time(), 'sending logs to',
                                                                        from_address)
                                                logging_handler(msg)
                                                send_mail(send_to=from_address, subject='Log Message',
                                                          text='Logs attached', file=file_logging_path)
                                                delete_messages()
                                        except:
                                            pass
                                    if get_gen_state() == 'up':
                                        generator_cmd(cmd='off')
                                        mail_msg = '{} {} {}'.format('Generator is going down after', timeout_frame, 'minutes')
                                        logging_handler(down_msg)
                                        send_mail(send_to=from_address, subject='Generator Control Message', text=mail_msg)
                                        set_gen_state(False, time_stamp=get_current_time())
                                        on_time = chop_microseconds(timeout_stamp - start_time).seconds
                                        set_time_spent(time_stamp=get_current_time(date=True, datetime_format=True),
                                                       time_span=on_time)
                            else:
                                logging_handler('{} {}'.format('This is not a Raspi, this is', uname()[1]))
                        else:
                            logging_handler(already_up_msg)
                    elif 'log' in key_command:
                        msg = '{} {} {}'.format(get_current_time(), 'sending logs to', from_address)
                        logging_handler(msg)
                        send_mail(send_to=from_address, subject='Log Message',
                                  text='Logs attached', file=file_logging_path)
                    elif 'status' in key_command:
                        if start_time:
                            time_span = (datetime.datetime.now() - start_time).total_seconds()
                            how_long, units = calculate_time_span(time_span)
                            msg = '{} {} {} {} {}'.format('Generator is', get_gen_state(), 'for', how_long, units)
                        else:
                            msg = '{} {}'.format('Generator is', get_gen_state())
                        logging_handler(msg)
                        send_mail(send_to=from_address, subject='Status Message', text=msg)
                    elif 'usage':
                        daily_usage = calculate_daily_usage(12)
                        usage_time = str(datetime.timedelta(seconds=daily_usage))
                        msg = '{} {} {}'.format\
                            ('Generator has been working for', usage_time, 'this month')
                        send_mail(send_to=from_address, subject='Generator Usage Message', text=msg)
                    else:
                        msg = '{} {}'.format(''.join(key_command), 'is an unknown command')
                        logging_handler(msg)
                        send_mail(send_to=from_address, text=msg)
                else:
                    msg = '{} {}'.format(from_address, not_white_list)
                    logging_handler(msg)
                delete_messages()
                time.sleep(sleep_time)
            else:
                msg = '{} {}'.format('Connection failed due to', login_message)
                logging_handler(msg)
        except:
            msg = 'No mails'
            logging_handler(msg)
            time.sleep(sleep_time)
