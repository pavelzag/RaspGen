from dbconnector import set_gen_state, get_gen_state, set_initial_db_state, set_time_spent
from configuration import get_config, get_white_list, get_pin
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
    import RPi.GPIO as GPIO
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


def get_current_time():
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
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


def logging_handler(msg):
    print(msg)
    logging.info(msg)


if __name__ == '__main__':
    ip_address = get_machine_ip()
    startup_msg = '{} {}'.format('Machine runs on', ip_address)
    print(startup_msg)
    logging.info(startup_msg)
    send_mail(send_to=owner, subject='Start up Message', text=startup_msg)
    # set_initial_db_state()
    start_time = None
    end_time = None
    i = 1
    while i == 1:
        try:
            uname_debug = 'DietPi'
            msrvr = imaplib.IMAP4_SSL(imap_addr, imap_port)
            login_stat, login_message = msrvr.login(receiver_email, receiver_password)
            if login_stat == 'OK':
                # logging.info(login_message)
                stat, cnt = msrvr.select('Inbox')
                key_command = get_key_command(cnt)
                from_address = get_sender()
                if is_in_white_list(from_address):
                    # current_state = str(get_gen_state())
                    logging_handler("{} {} {}".format(get_current_time(), from_address, white_list))
                    if 'debug' in key_command:
                        print(debug_message)
                        logging.info("{} {}". format(get_current_time(), debug_message))
                        send_mail(send_to=from_address, subject='Debug Message', text=debug_message)
                    elif 'off' in key_command:
                        # if current_state is not 'down':
                        if uname()[1] == 'DietPi':
                        # if uname_debug == 'DietPi':
                            generator_cmd(cmd='off')
                            # set_gen_state(state=False, time_stamp=get_current_time())
                            logging_handler('{} {}'. format(get_current_time(), down_msg))
                            end_time = datetime.datetime.now()
                            # Add 2 minutes (???) compensation for going down
                            time_span = int((datetime.datetime.now() - start_time).total_seconds())
                            how_long, units = calculate_time_span(time_span)
                            msg_to_log = '{} {} {}'.format('The generator was up for:', how_long, units)
                            logging_handler(msg_to_log)
                            mail_msg = '{} {}'.format(down_msg, msg_to_log)
                            send_mail(send_to=from_address, subject='Generator Control Message', text=mail_msg)
                            # set_time_spent(time_span)
                        else:
                            logging_handler('{} {}'.format('This is not a Raspi, this is', uname()[1]))
                    # else:
                    #     logging_handler(already_down_msg)
                    elif 'on' in key_command:
                        # if current_state is not 'up':
                        if uname()[1] == 'DietPi':
                        # if uname_debug == 'DietPi':
                            generator_cmd(cmd='on')
                            # set_gen_state(True, time_stamp=get_current_time())
                            msg = '{} {}'. format(get_current_time(), up_msg)
                            logging_handler(msg)
                            send_mail(send_to=from_address, subject='Generator Control Message', text=up_msg)
                            start_time = datetime.datetime.now()
                        else:
                            logging_handler('{} {}'.format('This is not a Raspi, this is', uname()[1]))
                    # else:
                    #     logging_handler(already_up_msg)
                    elif 'log' in key_command:
                        msg = '{} {} {}'.format(get_current_time(), 'sending logs to', from_address)
                        logging_handler(msg)
                        send_mail(send_to=from_address, subject='Log Message',
                                  text='Logs attached', file=file_logging_path)
                    elif 'status' in key_command:
                        time_span = (datetime.datetime.now() - start_time).total_seconds()
                        how_long, units = calculate_time_span(time_span)
                        # msg = '{} {} {} {} {}'.format('Generator is', current_state, 'for', how_long, units)
                        logging_handler(msg)
                        send_mail(send_to=from_address, subject='Status Message', text=msg)
                    else:
                        msg = '{} {} {}'.format(get_current_time(), ''.join(key_command), 'is an unknown command')
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
            msg = '{} {}'.format(get_current_time(), 'No mails')
            logging_handler(msg)
            time.sleep(sleep_time)
