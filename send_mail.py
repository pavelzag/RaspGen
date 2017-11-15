from configuration import get_config
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


# def send_mail(recipient='zagalsky@gmail.com', msg="Hi"):
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.ehlo()
#     server.starttls()
#     sender_email = get_config('email')
#     sender_password = get_config('password')
#     server.login(sender_email, sender_password)
#     server.sendmail(sender_email, recipient, msg)


def send_mail(send_from = 'zagalsky@gmail.com', send_to='', subject='hi', text='text', file=None,
              server="smtp.gmail.com"):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))
    if file != None:
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
    smtp.login(sender_email, sender_password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()