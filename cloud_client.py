#!flask/bin/python
from flask import Flask
import time
import datetime

app = Flask(__name__)


def get_current_time():
    ts = time.time()
    time_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return time_stamp


@app.route('/keep_alive')
def keep_alive():
    time_stamp = get_current_time()
    return '{} {}'.format(time_stamp, 'keep on keeping on')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
