import click
from domain.users import UserService
from domain.alerts import AlertManager
from adapters.database_adapter import DatabaseAdapter
from adapters.coinapi_adapter import CoinAPIClient
from domain.models import User
from .monitor import monitor_alerts

@click.group()
def cli():
    pass

@cli.command()
@click.argument("username")
@click.argument("password")
def sign_up(username, password):
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user_service.sign_up(username, password)
        click.echo(f"Utilisateur {username} créé avec succès.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")

@cli.command()
@click.argument("username")
@click.argument("password")
def login(username, password):
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
        return user
    except ValueError as e:
        click.echo(f"Erreur : {e}")
@cli.command()
@click.argument("asset_id")
@click.option("--target-price", type=float, help="Prix cible pour l'alerte")
@click.option("--percentage-change", type=float, help="Pourcentage de changement pour l'alerte")
def create_alert(asset_id, target_price, percentage_change):
    # Demande à l'utilisateur de se connecter
    username = click.prompt("Nom d'utilisateur")
    password = click.prompt("Mot de passe", hide_input=True)

    # Connexion de l'utilisateur
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
        return

    # Récupère le prix actuel de la cryptomonnaie
    api_key = "b6605be9-4488-4876-b84b-47ee05187b9f"
    client = CoinAPIClient(api_key)
    current_price = client.get_price(asset_id)

    # Crée l'alerte avec l'ID de l'utilisateur
    alert = {
        "user_id": user.user_id,  # Ajoute l'ID de l'utilisateur
        "asset_id": asset_id,
        "target_price": target_price,
        "percentage_change": percentage_change,
        "reference_price": current_price,
    }

    # Enregistre l'alerte
    alert_manager = AlertManager(db_adapter)
    alert_manager.create_alert(alert)
    click.echo(f"Alerte créée : {alert}")

@cli.command()
def list_alerts():
    # Demande à l'utilisateur de se connecter
    username = click.prompt("Nom d'utilisateur")
    password = click.prompt("Mot de passe", hide_input=True)

    # Connexion de l'utilisateur
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
        return

    # Récupère les alertes de l'utilisateur
    alert_manager = AlertManager(db_adapter)
    alerts = alert_manager.list_alerts(user.user_id)
    for alert in alerts:
        click.echo(alert)

@cli.command()
@click.argument("alert_id", type=int)
def delete_alert(alert_id):
    # Demande à l'utilisateur de se connecter
    username = click.prompt("Nom d'utilisateur")
    password = click.prompt("Mot de passe", hide_input=True)

    # Connexion de l'utilisateur
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
        return

    # Supprime l'alerte
    alert_manager = AlertManager(db_adapter)
    alert_manager.delete_alert(alert_id)
    click.echo(f"Alerte {alert_id} supprimée avec succès.")
# app/cli.py

@cli.command()
def start_monitoring():
    """
    Lance la surveillance des alertes.
    """
    monitor_alerts()

# app/cli.py
@cli.command()
def list_alerts():
    """
    Liste toutes les alertes de l'utilisateur connecté.
    """
    # Demande à l'utilisateur de se connecter
    username = click.prompt("Nom d'utilisateur")
    password = click.prompt("Mot de passe", hide_input=True)

    # Connexion de l'utilisateur
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
        return

    # Récupère les alertes de l'utilisateur
    alert_manager = AlertManager(db_adapter)
    alerts = alert_manager.list_alerts(user.user_id)
    for alert in alerts:
        click.echo(f"""
        Alerte ID: {alert['alert_id']}
        Cryptomonnaie: {alert['asset_id']}
        Prix cible: {alert['target_price']}
        Changement en pourcentage: {alert['percentage_change']}
        Prix de référence: {alert['reference_price']}
        """)
# app/cli.py
@cli.command()
@click.argument("alert_id", type=int)
def delete_alert(alert_id):
    """
    Supprime une alerte par son ID.
    """
    # Demande à l'utilisateur de se connecter
    username = click.prompt("Nom d'utilisateur")
    password = click.prompt("Mot de passe", hide_input=True)

    # Connexion de l'utilisateur
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
        return

    # Supprime l'alerte
    alert_manager = AlertManager(db_adapter)
    alert_manager.delete_alert(alert_id)
    click.echo(f"Alerte {alert_id} supprimée avec succès.")

@cli.command()
@click.argument("alert_id", type=int)
@click.option("--target-price", type=float, help="Nouveau prix cible pour l'alerte")
@click.option("--percentage-change", type=float, help="Nouveau pourcentage de changement pour l'alerte")
def update_alert(alert_id, target_price, percentage_change):
    """
    Met à jour une alerte existante.
    """
    # Demande à l'utilisateur de se connecter
    username = click.prompt("Nom d'utilisateur")
    password = click.prompt("Mot de passe", hide_input=True)

    # Connexion de l'utilisateur
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
        return

    # Met à jour l'alerte
    alert_manager = AlertManager(db_adapter)
    try:
        alert_manager.update_alert(alert_id, target_price, percentage_change)
        click.echo(f"Alerte {alert_id} mise à jour avec succès.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")

@cli.command()
@click.argument("alert_id", type=int)
def delete_alert(alert_id):
    """
    Supprime une alerte existante.
    """
    # Demande à l'utilisateur de se connecter
    username = click.prompt("Nom d'utilisateur")
    password = click.prompt("Mot de passe", hide_input=True)

    # Connexion de l'utilisateur
    db_adapter = DatabaseAdapter("crypto_alerts.db")
    user_service = UserService(db_adapter)
    try:
        user = user_service.login(username, password)
        click.echo(f"Connecté en tant que {username}.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
        return

    # Supprime l'alerte
    alert_manager = AlertManager(db_adapter)
    try:
        alert_manager.delete_alert(alert_id)
        click.echo(f"Alerte {alert_id} supprimée avec succès.")
    except ValueError as e:
        click.echo(f"Erreur : {e}")
    
    

if __name__ == "__main__":
    cli()