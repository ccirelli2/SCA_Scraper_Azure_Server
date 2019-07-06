# Documentation
'https://codehandbook.org/how-to-read-email-from-gmail-using-python/'

# Import Libraries
import imaplib 
import base64
import os
import email


FROM_EMAIL = 'intellisurance@gmail.com'
FROM_PWD  = 'Work4starr'
SMTP_SERVER = 'imap.gmail.com'
SMTP_PORT = 993

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL, FROM_PWD)

mail.select('inbox')


type, data = mail.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
first_email_id = id_list[0]
typ, data_1 = mail.fetch(first_email_id, '(RFC822)')

email_body = data_1[0][1]
print(email_body[:500])



