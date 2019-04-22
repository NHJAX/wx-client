import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
to = 'nhjax-dev@gmail.com'
gmail_user = 'rpiwxbox@gmail.com'
gmail_password = 'ZAQ!2wsx'
smtpserver = smtplib.SMTP('smtp.gmail.com',587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()
my_ssid = "NMRTC JAX RPI is connected"
msg = MIMEText(my_ssid)
msg['Subject'] = 'IP For NMRTC JAX RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
