import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
def sendmail(smtp_username,smtp_password,smtp_port,smtp_server,sender_email,receiver_email,cc_email,bcc_email,subject,message_body,listfilename):
    # # ข้อมูลเชื่อมต่อ SMTP
    # smtp_server = 'inetmail.cloud'
    # smtp_port = 587  # หรือใช้ port 465 หากใช้ SSL/TLS
    # smtp_username = '*'
    # smtp_password = '*'
    #
    # # ข้อมูลผู้ส่ง ผู้รับ และข้อความ
    # sender_email = 'Purisit.to@inetms.co.th'
    # receiver_email = 'purisit007@hotmail.com,Purisit.to@outlook.com'
    # cc_email='tytyty1999ty@hotmail.com'
    # bcc_email=''
    # subject = 'Subject of the email Test1'
    # message_body = 'Body of the email'

    # สร้างออบเจ็กต์ข้อความและกำหนดค่า
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Cc'] = cc_email
    message['Bcc'] = bcc_email
    message['Subject'] = subject

    # เพิ่มข้อความลงในอีเมล
    message.attach(MIMEText(message_body, 'html'))

    # แนบไฟล์
    #listfilename = {'file.txt','my_archive.zip'}
    for filename in listfilename:
        with open(filename, 'rb') as attachment:
            part = MIMEApplication(attachment.read(), Name=os.path.basename(filename))

            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(filename)}"'
            message.attach(part)

    # เชื่อมต่อ SMTP server และส่งอีเมล
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # ใช้ TLS encryption (หากใช้ port 587)
        server.login(smtp_username, smtp_password)
        server.send_message(message)

    print('Email sent successfully!')
