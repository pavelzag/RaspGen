from datetime import datetime
from os import remove
from shutil import copyfile
import time

log_file = "generator"


def check_current_time():
    now = datetime.now().time()
    full_time = int(''.join(str(now.hour) + str(now.minute)))
    print(full_time)
    return full_time


def check_current_date():
    date = time.strftime("%d_%m_%Y")
    print(date)
    return date


def copy_generator_file():
    log_file_original = '{}.{}'.format(log_file, 'txt')
    log_file_bk = '{}_{}.{}'.format(log_file,check_current_date(), 'txt')
    copyfile(log_file_original, log_file_bk)
    remove(log_file_original)
    open(log_file_original, "w+")
    print('eh')


def create_timed_rotating_log():
    full_time = check_current_time()
    while full_time != 1647:
        print('do nothing')
        time.sleep(10)
        full_time = check_current_time()
    else:
        print('do some other things')
        copy_generator_file()
        create_timed_rotating_log()


if __name__ == "__main__":
    create_timed_rotating_log()