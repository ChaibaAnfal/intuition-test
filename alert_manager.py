class AlertManager:
    def __init__(self):
        self.alerts = []  # Utilise une base de données pour une solution plus robuste

    def create_alert(self, asset_id, target_price=None, percentage_change=None):
        if target_price is None and percentage_change is None:
            raise ValueError("Une alerte doit avoir un prix cible ou un pourcentage de changement.")

        alert = {
            "asset_id": asset_id,
            "target_price": target_price,
            "percentage_change": percentage_change,
            "reference_price": None,  # Sera défini lors de la création de l'alerte
        }
        self.alerts.append(alert)
        return alert

    def list_alerts(self, asset_id=None):
        if asset_id:
            return [alert for alert in self.alerts if alert["asset_id"] == asset_id]
        return self.alerts

    def delete_alert(self, alert_id):
        if 0 <= alert_id < len(self.alerts):
            return self.alerts.pop(alert_id)
        return None