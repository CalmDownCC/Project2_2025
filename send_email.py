import smtplib
from email.message import EmailMessage


from_email_addr ="1169806185@qq.com"
from_email_pass ="scrmwkpywgleiigf"
to_email_addr ="3851752811@qq.com"


msg = EmailMessage()


body ="Hello from Rasberry Pi"
msg.set_content(body)


msg['From'] = from_email_addr
msg['To'] = to_email_addr


msg['Subject'] = 'TEST EMAIL'


server = smtplib.SMTP('smtp.qq.com', 587)


server.starttls()


server.login(from_email_addr, from_email_pass)


server.send_message(msg)


print ('Email sent')


server.quit()
