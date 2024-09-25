from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from smtplib import SMTP
from ssl import create_default_context

#
# Put an email together in MIMEMultipart and send it off.
#
def send(
    host,
    port,
    username,
    password,
    sender,
    recipient,
    subject,
    html,
    attachments=[]
):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['X-PM-Message-Stream'] = 'broadcast'
    msg.attach(MIMEText(html, 'html'))
    for attachment in attachments:
        msg.attach(attachment)
    # Send it off via smtp.mail.me.com
    context = create_default_context()
    with SMTP(host, port) as smtp:
        smtp.starttls(context=context)
        smtp.login(username, password)
        smtp.sendmail(sender, recipient, msg.as_string())
