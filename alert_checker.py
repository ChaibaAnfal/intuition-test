def check_alerts(alerts, current_price):
    triggered_alerts = []
    for alert in alerts:
        if alert["target_price"] is not None:
            # Vérifie les alertes basées sur un prix cible
            if alert["target_price"] >= current_price:
                triggered_alerts.append(alert)
        elif alert["percentage_change"] is not None:
            # Vérifie les alertes basées sur un pourcentage de changement
            reference_price = alert["reference_price"]
            percentage_change = ((current_price - reference_price) / reference_price) * 100
            if alert["percentage_change"] < 0 and percentage_change <= alert["percentage_change"]:
                # Alerte pour une baisse (ex : -20 %)
                triggered_alerts.append(alert)
            elif alert["percentage_change"] > 0 and percentage_change >= alert["percentage_change"]:
                # Alerte pour une hausse (ex : +20 %)
                triggered_alerts.append(alert)
    return triggered_alerts