# app/monitor.py
import time
from adapters.coinapi_adapter import CoinAPIClient
from adapters.database_adapter import DatabaseAdapter
from adapters.email_adapter import EmailAdapter
from domain.alerts import AlertManager
from config import EMAIL_CONFIG

def monitor_alerts():
    api_key = "b6605be9-4488-4876-b84b-47ee05187b9f"
    client = CoinAPIClient(api_key)
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    alert_manager = AlertManager(db_adapter)
    email_adapter = EmailAdapter(EMAIL_CONFIG["from_email"], EMAIL_CONFIG["password"])

    while True:
        # Récupère toutes les alertes
        alerts = alert_manager.list_alerts()

        for alert in alerts:
            # Récupère le prix actuel de la cryptomonnaie
            current_price = client.get_price(alert["asset_id"])

            # Vérifie si l'alerte est déclenchée
            if alert["target_price"] is not None and current_price <= alert["target_price"]:
                message = f"🚨 Alerte déclenchée pour {alert['asset_id']} : Le prix est descendu en dessous de {alert['target_price']} USD."
                print(message)
                email_adapter.send_email("destinataire@gmail.com", "Alerte Cryptomonnaie", message)
            elif alert["percentage_change"] is not None:
                percentage_change = ((current_price - alert["reference_price"]) / alert["reference_price"]) * 100
                if alert["percentage_change"] < 0 and percentage_change <= alert["percentage_change"]:
                    message = f"🚨 Alerte déclenchée pour {alert['asset_id']} : Le prix a baissé de {alert['percentage_change']} %."
                    print(message)
                    email_adapter.send_email("destinataire@gmail.com", "Alerte Cryptomonnaie", message)
                elif alert["percentage_change"] > 0 and percentage_change >= alert["percentage_change"]:
                    message = f"🚨 Alerte déclenchée pour {alert['asset_id']} : Le prix a augmenté de {alert['percentage_change']} %."
                    print(message)
                    email_adapter.send_email("destinataire@gmail.com", "Alerte Cryptomonnaie", message)

        # Attend 60 secondes avant de vérifier à nouveau
        time.sleep(60)

if __name__ == "__main__":
    monitor_alerts()