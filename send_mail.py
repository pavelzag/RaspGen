import smtplib
from configuration import get_config


def send_mail(recipient='zagalsky@gmail.com', msg="Hi"):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    sender_email = get_config('email')
    sender_password = get_config('password')
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient, msg)