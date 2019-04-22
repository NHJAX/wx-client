import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
to = 'nhjaxdev@gmail.com'
gmail_user = 'rpiwxbox@gmail.com'
gmail_password = 'ZAQ!2wsx'
smtpserver = smtplib.SMTP('smtp.gmail.com',587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()
my_ssid = "DoItLikeERR"
msg = MIMEText(my_ssid)
msg['Subject'] = 'WX BOX BROKE ON  %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
