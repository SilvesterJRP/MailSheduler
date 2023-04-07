import smtplib
import datetime as dt
import time
import sys
from email.mime.multipart import MIMEMultipart
from cryptography.fernet import Fernet
from datetime import datetime 
from configparser import ConfigParser
config = ConfigParser()
config.read("AppConfig.ini")


def SetMailHeader():

    message = MIMEMultipart()
    message['From'] = config.get("UserSettings", "senderMail")
    message['To'] = config.get("UserSettings", "receiverEmail")
    message['Subject'] = config.get("MailSettings", "subjectTxt")
    return message

    
def SetUpSMTP(senderMail):
    
    # creates SMTP session
    gmSmtp = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    gmSmtp.starttls()
    token = config.get("UserSettings", "token") 
    fernet = Fernet(token)
    loginPwd = fernet.decrypt(config.get("UserSettings", "loginPwd")).decode()

    try: 
        # Authentication
        gmSmtp.login(senderMail, loginPwd)
    except:
        print("Login Failed")
    return gmSmtp


def GetMailBody():
    mailBody = "<html><body>"
    mailBody = mailBody + config.get("MailSettings", "bodyHeader")
    mailBody = mailBody + config.get("MailSettings", "bodyTxt")
    mailBody = mailBody + "<p> Added Image and Video files to verify attachment </p>"
    mailBody = mailBody + config.get("MailSettings", "bodyFooter")
    mailBody = mailBody + "<p> Mail Sent At " + str(dt.datetime.now()) + "</p>"
    mailBody = mailBody + "</body></html>"
    return mailBody


def AttachTheFile(filename, filepath):
    from email import encoders
    from email.mime.base import MIMEBase
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
    from email.mime.text import MIMEText
    message = SetMailHeader()
    message.attach(MIMEText(GetMailBody(), "html"))   
    message.attach(AttachTheFile("Sample.txt", ".\\Files\\"))
    message.attach(AttachTheFile("chatgpt.png", ".\\Files\\"))
    message.attach(AttachTheFile("PDF Sample.pdf", ".\\Files\\"))
    message.attach(AttachTheFile("VideoTest.mp4", ".\\Files\\"))
    smtp = SetUpSMTP(message['From'])
    # sending the mail 
    smtp.send_message(message)
    print("Mail Sent")
    smtp.quit()


def TriggerEmail(SchedTime):
    time.sleep(SchedTime.timestamp() - time.time())
    SendEMail()
    print('email sent on ' + str(SchedTime))


configDateTime = config.get("ScheduleSettings", "startDate") + " " + config.get("ScheduleSettings", "startTime")
startDateTime = datetime.strptime(configDateTime, '%d/%m/%Y %H:%M:%S')
interval = dt.timedelta(minutes=2)  # set the interval for sending the email
isNotSent = True

while isNotSent:
    TriggerEmail(startDateTime)
    startDateTime = startDateTime + interval
    isNotSent = False
        
if (isNotSent is False):
    print("Exiting System")
    sys.exit
