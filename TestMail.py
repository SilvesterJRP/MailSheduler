import smtplib
import sys
from datetime import datetime
import time
from configparser import ConfigParser
config = ConfigParser()
config.read("AppConfig.ini")
configDateTime = config.get("ScheduleSettings","startDate") + " " + config.get("ScheduleSettings","startTime")
startDateTime = datetime.strptime(configDateTime, '%d/%m/%Y %H:%M:%S' )
print(str(startDateTime))
sys.exit
senderMail = config.get("UserSettings","senderMail") #"botemail845@gmail.com"
print(senderMail)
loginPwd = config.get("UserSettings","loginPwd") #"xoioipjmdepfzppl"
print(loginPwd)
receiverEmail = config.get("UserSettings","receiverEmail") #"rajuclintons3@gmail.com"
subjectTxt = config.get("MailSettings","subjectTxt") #"Automated Mail From python Mailer App"
bodyTxt = config.get("MailSettings","bodyTxt") #"This is a auto generated mail from Python. Meant for testing only"
def SetUpSMTP():

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()

    try: 
    # Authentication
        s.login(senderMail, loginPwd)
    except:
        print("Login Failed")
    return s


def GetMailBody():
    mailBody = "<html><body>"
    mailBody = mailBody + config.get("MailSettings","bodyHeader")
    mailBody = mailBody + config.get("MailSettings","bodyTxt")
    mailBody = mailBody + config.get("MailSettings","bodyFooter")
    mailBody = mailBody + "</body></html>"
    return mailBody


def AttachTheFile(filename, filepath):
    from email import encoders
    from email.mime.base import MIMEBase
    print("FilePath = " + filepath)
    attachment = open(filepath + filename, "r+b")
  
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    
    # encode into base64
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    return p
    

def SendEMail():

    # import EmailMessage method
    from email.message import EmailMessage
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    
    # message to be sent
    #message = EmailMessage()
    message = MIMEMultipart()
    message['From'] = senderMail
    message['To'] = receiverEmail
    message['Subject'] =  subjectTxt
    #message['msg'] = bodyTxt
    message.attach (MIMEText(GetMailBody(),"html"))
   
    message.attach(AttachTheFile("Sample.txt",".\\Files\\") )

    

    smtp = SetUpSMTP()
    # sending the mail
    #smtp.sendmail(senderMail, receiverEmail, message)
    #smtp.sendmail(message)
    smtp.send_message(message)
    print("Mail Sent")
    smtp.quit()

SendEMail()


 
# terminating the session
