import imaplib
import time
from dbconnector import set_gen_state
from configuration import get_config
import RPi.GPIO as GPIO

receiver_email = get_config('email')
receiver_password = get_config('password')
sleep_time = int(get_config('sleep_time'))
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


if __name__ == '__main__':
    msrvr = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    msrvr.login(receiver_email, receiver_password)
    i = 1
    while i == 1:
        try:
            stat, cnt = msrvr.select('Inbox')
            stat, data = msrvr.fetch(cnt[0], '(UID BODY[TEXT])')
            if 'off' in data[0][1]:
                generator_cmd(cmd='off')
                set_gen_state(True)
                print("Generator is going down")
            elif 'on' in data[0][1]:
                generator_cmd(cmd='on')
                set_gen_state(True)
                print("Generator is going up")
            delete_messages()
            time.sleep(sleep_time)
        except:
            print('no mails')
            time.sleep(sleep_time)
    msrvr.close()
    msrvr.logout()
