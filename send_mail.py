from configuration import get_config
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from logger import logging_handler


def send_mail(send_from = 'zagalsky@gmail.com', send_to='', subject='hi', text='text', file=None,
              server="smtp.gmail.com"):
    logging_handler('{} {} {} {}'.format('Sending', text, 'mail to:',send_to))
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    if file is not None:
        with open(file, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(file)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        msg.attach(part)

    smtp = smtplib.SMTP(server, 587)
    smtp.ehlo()
    smtp.starttls()
    sender_email = get_config('email')
    sender_password = get_config('password')
    result = smtp.login(sender_email, sender_password)[1]
    logging_handler('{} {}'.format('Connection to SMTP result:', result))
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()