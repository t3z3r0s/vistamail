import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Smtp:
    def __init__(self, host=None, user=None, password=None, port=587):
        self.host     = host
        self.user     = user
        self.password = password
        self.port     = port

    def configure(self, host, user, password, port=587):
        self.host     = host
        self.user     = user
        self.password = password
        self.port     = port

    def send_email(self, to, subject, body):
        msg = MIMEMultipart()
        msg["From"]    = self.user
        msg["To"]      = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if self.port == 465:
            with smtplib.SMTP_SSL(self.host, self.port) as server:
                server.login(self.user, self.password)
                server.sendmail(self.user, to, msg.as_string())
        else:
            with smtplib.SMTP(self.host, self.port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(self.user, self.password)
                server.sendmail(self.user, to, msg.as_string())