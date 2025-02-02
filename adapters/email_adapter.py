# adapters/email_adapter.py
import smtplib
from email.mime.text import MIMEText

class EmailAdapter:
    def __init__(self, email, password):
        """
        Initialise l'adaptateur email avec l'adresse email et le mot de passe.
        """
        self.email = email
        self.password = password

    def send_email(self, to_email, subject, body):
        """
        Envoie un email.
        """
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, to_email, msg.as_string())