import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
to = 'nhjax-dev@'
gmail_user = 'rpiwxbox@gmail.com'
gmail_password = 'ZAQ!2wsx'
smtpserver = smtplib.SMTP('smtp.gmail.com',587)
smtpserver.ehlo()
smtpserver.starttls()
smtpserver.ehlo
smtpserver.login(gmail_user, gmail_password)
today = datetime.date.today()
brg='iwgetid -r'
s=subprocess.Popen(brg,shell=True,stdout=subprocess.PIPE)
ssid = s.communicate()
arg='ip route list'
p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
data = p.communicate()
split_data = data[0].split()
ipaddr = split_data[split_data.index('src')+1]   
my_ssid = "NMRTC JAX RPI is connected to '{0}' IP address is '{1}'" .format(ssid, ipaddr)
msg = MIMEText(my_ssid)
msg['Subject'] = 'IP For NMRTC JAX RaspberryPi on %s' % today.strftime('%b %d %Y')
msg['From'] = gmail_user
msg['To'] = to
smtpserver.sendmail(gmail_user, [to], msg.as_string())
smtpserver.quit()
