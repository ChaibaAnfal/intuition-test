# test_email.py
from adapters.email_adapter import EmailAdapter
from config import EMAIL_CONFIG

def test_send_email():
    # Récupère les informations d'email depuis la configuration
    from_email = EMAIL_CONFIG["from_email"]
    password = EMAIL_CONFIG["password"]

    # Instancie l'adaptateur email
    email_adapter = EmailAdapter(email=from_email, password=password)

    # Définit les détails de l'email
    to_email = "destinataire@gmail.com"  # Remplace par l'adresse email du destinataire
    subject = "Test d'envoi d'email"
    body = "Ceci est un test d'envoi d'email depuis Crypto Alerts."

    # Envoie l'email
    email_adapter.send_email(to_email, subject, body)
    print("Email envoyé avec succès !")

if __name__ == "__main__":
    test_send_email()