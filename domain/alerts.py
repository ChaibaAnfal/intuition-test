class Alert:
    def __init__(self, asset_id, target_price=None, percentage_change=None, reference_price=None):
        self.asset_id = asset_id
        self.target_price = target_price
        self.percentage_change = percentage_change
        self.reference_price = reference_price

    def is_triggered(self, current_price):
        if self.target_price is not None:
            return current_price <= self.target_price
        elif self.percentage_change is not None:
            change = ((current_price - self.reference_price) / self.reference_price) * 100
            if self.percentage_change < 0:
                return change <= self.percentage_change
            else:
                return change >= self.percentage_change
        return False


class AlertService:
    def __init__(self, alert_repository):
        self.alert_repository = alert_repository

    def create_alert(self, alert):
        self.alert_repository.save(alert)

    def list_alerts(self, user_id):
        return self.alert_repository.find_by_user(user_id)

    def check_alerts(self, user_id, current_price):
        alerts = self.list_alerts(user_id)
        triggered_alerts = [alert for alert in alerts if alert.is_triggered(current_price)]
        return triggered_alerts
    

class AlertManager:
    def __init__(self, alert_repository):
        self.alert_repository = alert_repository

    def create_alert(self, alert):
        """
        Crée une nouvelle alerte.
        """
        self.alert_repository.save_alert(alert)

    def list_alerts(self, user_id):
        """
        Récupère toutes les alertes d'un utilisateur spécifique.
        """
        return self.alert_repository.find_alerts_by_user(user_id)

    def list_alerts(self, user_id=None):
        """
        Récupère toutes les alertes d'un utilisateur spécifique ou toutes les alertes si user_id est None.
        """
        if user_id is not None:
            return self.alert_repository.find_alerts_by_user(user_id)
        else:
            return self.alert_repository.find_all_alerts()
    
    def update_alert(self, alert_id, target_price=None, percentage_change=None):
        """
        Met à jour une alerte existante.
        """
        alert = self.alert_repository.find_alert_by_id(alert_id)
        if not alert:
            raise ValueError("Alerte non trouvée.")

        if target_price is not None:
            alert["target_price"] = target_price
        if percentage_change is not None:
            alert["percentage_change"] = percentage_change

        self.alert_repository.update_alert(alert)
    
    def delete_alert(self, alert_id):
        """
        Supprime une alerte existante.
        """
        if not self.alert_repository.find_alert_by_id(alert_id):
            raise ValueError("Alerte non trouvée.")
        self.alert_repository.delete_alert(alert_id)