#!/usr/bin/python

import sys
import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
from datetime import datetime


def SendMail(toMail, subject, content):
    
    print 'SendMail', toMail, subject, content
    smtpHost = 'smtp.exmail.qq.com'
    # smtpPort = '25'
    sslPort = '465'
    fromMail = 'monitor@tuyoogame.com'
    # toMail = 'zouyi@tuyoogame.com'
    username = 'monitor@tuyoogame.com'
    password = 'jiankong!@#20140617'
    
    # subject = u'[Notice]hello'
    # body    = u'hello,this is a mail from '
    
    encoding = 'utf-8'
    mail = MIMEText(content.encode(encoding), 'plain', encoding)
    mail['Subject'] = Header(subject, encoding)
    mail['From'] = fromMail
    mail['To'] = toMail
    mail['Date'] = formatdate()
    try:
        smtp = smtplib.SMTP_SSL(smtpHost, sslPort)
        smtp.ehlo()
        smtp.login(username, password)
        smtp.sendmail(fromMail, toMail, mail.as_string())
        smtp.close()
        print 'SEND Mail OK'
    
    except Exception:
        print 'ERROR:unable to send mail'

if __name__ == "__main__":

    nowtime = str(datetime.now())
    toAdd = sys.argv[1]
    subject = sys.argv[2]
    message = sys.argv[3]
    content = message + "\n" + nowtime
    
    toAdds = toAdd.split(';')
    for toadd in toAdds:
        toadd = toadd.strip()
        if len(toadd) > 0 :
            SendMail(toadd, subject, content)
