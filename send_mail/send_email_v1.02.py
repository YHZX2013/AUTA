#coding:utf-8

import smtplib  
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from time import sleep
import sys

mail_host="smtp.163.com"  
mail_user="******" 
mail_pass="******" 
mail_postfix="163.com"

failed_str = '''同学您好！
很遗憾的通知您，您的简历未通过联盟的初步审核。
建议您也尝试论坛上其他的内推渠道，若有疑问，请回复给我们。
同时，衷心的感谢您对北邮联盟的支持，并祝愿您学业有成，工作顺利！
'''

success_str = '''同学您好！
恭喜您通过了联盟的内推基准，获得2016春招内推资格！
您将在近期收到官网完善简历的短信和邮件通知→简历评估→安排电话/视频面试。
若有疑问，请回复给我们。衷心的感谢您对北邮联盟的支持，并祝愿您学业有成，工作顺利！
请加入春招AUTA内推群获取最新内推信息，群号：457046181
'''

def send_mail(to_list, content):  
    sender='阿里巴巴高校技术联盟'+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    sub = '2016阿里北邮高校技术联盟内推评议结果' 
    msg['Subject'] = sub
    msg['From'] = sender  
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)
        server.sendmail(sender, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False

def send_mail_all(to_list_file, content):
    g_success = 0
    g_failed = 0
    
    f = open(to_list_file, 'r')

    lines = f.readlines()
    for l in lines:
        if len(l.strip()) == 0:
            continue
        
        if send_mail([l.strip()], content):
            print 'sendto: '+ l.strip() + ' ' + sys.argv[2] + ' ok!'
            g_success += 1
        else:
            print 'sendto: '+ l.strip() + ' ' + sys.argv[2] + ' failed!'
            g_failed += 1
        
        sleep(1)

    if g_success != 0:
        print ('Send success ok total number: %d' % g_success)

    if g_failed != 0:
        print ('Send failed ok total number: %d' % g_failed)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage send_mail.py mail.txt \'success\\failed\''
    else:
        if sys.argv[2] == 'success':
            send_mail_all(sys.argv[1], success_str)
        elif sys.argv[2] == 'failed':
            send_mail_all(sys.argv[1], failed_str)
        else:
            print sys.argv[2] + ' error!'

