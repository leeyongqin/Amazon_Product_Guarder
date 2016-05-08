#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib, datetime
from email.mime.text import MIMEText
from email.header import Header


def send_mail(html_file=None):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    mail_host = "smtp.qiye.163.com"
    mail_user = "de-email-1@jetech-design.com"
    mail_pass = "JETech-1"

    sender = "de-email-1@jetech-design.com"
    receiver = ["853523500@qq.com", "822284070@qq.com"]

    message_body = "<h1>%s</h1>" % now
    message = MIMEText(message_body, 'html', 'utf-8')
    message["From"] = Header(
        "Guarder<de-email-1@jetech-design.com>", "utf-8")
    message["To"] = Header("; ".join(receiver), "utf-8")
    subject = "%s: 亚马逊|Buybox|跟买|" % now
    message["Subject"] = Header(subject, "utf-8")

    try:
        smtpobj = smtplib.SMTP()
        smtpobj.connect(mail_host, 25)
        smtpobj.login(mail_user, mail_pass)
        smtpobj.sendmail(sender, receiver, message.as_string())
        print 'Send Mail Success: %s' % now
    except smtplib.SMTPException:
        print 'Send Failed: %s' % now
        