import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version


class Send_MAIL():

	def __init__(self, recipients, subject, text):
		server = 'SMTP'
		user = 'login'
		password = 'passwoer'


		self.recipients = recipients
		sender = user
		self.subject = subject
		self.text = text
		html = '<html><head></head><body><p>' + text + '</p></body></html>'
		
		print(recipients, user, subject, text)


		msg = MIMEMultipart('alternative')
		msg['Subject'] = subject
		msg['From'] = 'NAME <' + sender + '>'
		msg['To'] = ', '.join(recipients)
		msg['Reply-To'] = sender
		msg['Return-Path'] = sender
		msg['X-Mailer'] = 'Python/' + (python_version())

		part_text = MIMEText(text, 'plain')
		part_html = MIMEText(html, 'html')
		
		
		msg.attach(part_text)
		msg.attach(part_html)
		
		#print(msg.as_string())
		
		mail = smtplib.SMTP_SSL(server)
		mail.login(user, password)
		mail.sendmail(sender, recipients, msg.as_string())
		mail.quit()

