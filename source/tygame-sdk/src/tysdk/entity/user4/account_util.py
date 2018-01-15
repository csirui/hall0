#!/usr/bin/python
# ! encoding=utf-8
import smtplib
import sys

from datetime import datetime
from email.Header import Header
from email.MIMEText import MIMEText
from email.Utils import formatdate

from tyframework.context import TyContext


class AccountUtil:
    @classmethod
    def sendMail(cls, toMail, subject, content, **kwargs):
        print 'SendMail', toMail, subject, content
        appId = kwargs.get('appId', '9999')
        mailConfig = TyContext.Configure.get_game_item_json(appId, "emailConfig", {})
        if not mailConfig:
            TyContext.ftlog.error("doSendMail error,cannot find config of appId", appId)
        smtpHost = mailConfig.get('smtpHost')
        sslPort = mailConfig.get('sslPort')
        if not sslPort:
            sslPort = '465'
        if not smtpHost:
            smtpHost = 'smtpdm.aliyun.com'
        fromMail = mailConfig.get('fromMail')
        if not fromMail:
            fromMail = 'noreply@cs.7g.do'
        username = mailConfig.get('username')
        if not username:
            username = fromMail
        password = mailConfig.get('password')
        if not password:
            password = 'qiJido3211'
        encoding = 'utf-8'
        mail = MIMEText(content.encode(encoding), 'html', encoding)
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
            return True
        except Exception:
            return False


if __name__ == "__main__":

    nowtime = str(datetime.now())
    toAdd = sys.argv[1]
    subject = sys.argv[2]
    message = sys.argv[3]
    content = message + "\n" + nowtime

    toAdds = toAdd.split(';')
    for toadd in toAdds:
        toadd = toadd.strip()
        if len(toadd) > 0:
            AccountUtil(toadd, subject, content)
