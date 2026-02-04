import smtplib
import os
from email.mime.text import MIMEText


EMAIL = os.getenv("proteinperks@gmail.com")
PASSWORD = os.getenv("ghzq kbze pzzp lpwn")


def send_order_email(message):

    msg = MIMEText(message)
    msg["Subject"] = "🛒 New Order - ProteinPerks"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)

    server.send_message(msg)
    server.quit()
