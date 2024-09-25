# smtp-emailer

This is a Python package that provides the function `send`:

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
        msg.attach(MIMEText(html, 'html'))
        for attachment in attachments:
            msg.attach(attachment)
        # Send it off via smtp.mail.me.com
        context = create_default_context()
        with SMTP(host, port) as smtp:
            smtp.starttls(context=context)
            smtp.login(username, password)
            smtp.sendmail(sender, recipient, msg.as_string())

## Installation

    pip install smtp-emailer

## Usage

    from email.mime.application import MIMEApplication
    from smtp_emailer import send

    attachment = MIMEApplication(b"File contents", name="filename.txt")
    attachment['Content-Disposition'] = 'attachment; filename="filename.txt"'

    send(
        "smtp.mail.me.com",
        587,
        "username@icloud.com",
        "<app-specific password>",
        "Service Name <no-reply@example.org>",
        "Recipient Name <recipient@example.org>",
        "Re: Example Subject",
        "<h1>Example email</h1><p>This is an example email.</p>",
        [attachment],
    )
