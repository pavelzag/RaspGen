import smtplib
from configuration import get_config

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
sender_email = get_config('email')
sender_user = get_config('user')
sender_password = get_config('password')
server.login(sender_email, sender_password)


def send_mail(msg = "Hi"):
    server.sendmail(sender_email, "zagalsky@gmail.com", msg)