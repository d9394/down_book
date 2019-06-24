#!/usr/bin/python
#encoding: utf-8
import os
import smtplib
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText    
#from email.mime.image import MIMEImage 
from email.header import Header 

def send_mail(receiver, files, file_path):
	smtpserver = u'smtp.163.com'
	username = u'33333333333@163.com'     #输入邮箱登陆smtp用户名
	password = u'zzzzzzzzzz'       #输入邮箱smtp发件密码
#	sender= username.decode('utf-8').split('@')[0] + '<' + username.decode('utf-8') + '>'
	receivers = username + ',' + receiver
	msg = MIMEMultipart('mixed') 
	msg['Subject'] = Header(files.decode('utf-8').split('.')[0])
	msg['From'] = username
	msg['To'] = receivers.decode('utf-8')	
	
	#构造附件
	if os.path.isfile(file_path + '/'+ files):
		att1 = MIMEText(u"电子书","plain","utf-8")
		msg.attach(att1)
		print("Adding file %s to email" % (file_path + '/'+ files))
		att2 = MIMEText(open(file_path + '/'+ files, 'rb').read(), 'base64', 'utf-8')
		att2["Content-Type"] = 'application/octet-stream'
#		att2["Content-Type"] = 'multipart/mixed'
		att2.add_header('Content-Disposition', 'attachment', filename=('gb2312','', files.decode('utf-8').encode('gb2312')))
		msg.attach(att2)


	#print msg.as_string()
	try:       
		#发送邮件
		smtp = smtplib.SMTP()    
		smtp.connect(smtpserver)
		#我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
		#smtp.set_debuglevel(1)  
		smtp.login(username, password)
		smtp.sendmail(username, receivers.decode('utf-8').split(',') , msg.as_string()) 
	except smtplib.SMTPException as e:
		print("Send mail error : %s" % e)
	else:
		print("Email sended to %s." % receiver)
