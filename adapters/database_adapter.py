import sqlite3

from domain.models import User


class DatabaseAdapter:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()  # Initialise la base de données

    def _init_db(self):
        """
        Initialise la base de données en créant les tables si elles n'existent pas.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    asset_id TEXT,
                    target_price REAL,
                    percentage_change REAL,
                    reference_price REAL,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)

    def next_id(self):
        """
        Génère un ID unique pour un nouvel utilisateur en trouvant l'ID maximum actuel et en ajoutant 1.
        Si la table est vide, retourne 1.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT MAX(user_id) FROM users")
            row = cursor.fetchone()
            if row and row[0] is not None:
                return row[0] + 1  # Retourne l'ID maximum + 1
            return 1  # Si la table est vide, commence à 1

    def save_user(self, user):
        """
        Enregistre un nouvel utilisateur dans la base de données.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, user.password))

    def find_user_by_username(self, username):
        """
        Recherche un utilisateur par son nom d'utilisateur.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
            row = cursor.fetchone()
            if row:
                return User(row[0], row[1], row[2])
            return None

    def save_alert(self, alert):
        """
        Enregistre une alerte dans la base de données.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO alerts (user_id, asset_id, target_price, percentage_change, reference_price)
                VALUES (?, ?, ?, ?, ?)
            """, (alert["user_id"], alert["asset_id"], alert["target_price"], alert["percentage_change"], alert["reference_price"]))

    def find_alerts_by_user(self, user_id):
        """
        Récupère toutes les alertes d'un utilisateur spécifique.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM alerts WHERE user_id = ?", (user_id,))
            alerts = []
            for row in cursor.fetchall():
                alert = {
                    "alert_id": row[0],
                    "user_id": row[1],
                    "asset_id": row[2],
                    "target_price": row[3],
                    "percentage_change": row[4],
                    "reference_price": row[5],
                }
                alerts.append(alert)
            return alerts
        

    def update_alert(self, alert):
        """
        Met à jour une alerte dans la base de données.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE alerts
                SET target_price = ?, percentage_change = ?
                WHERE alert_id = ?
            """, (alert["target_price"], alert["percentage_change"], alert["alert_id"]))

    def delete_alert(self, alert_id):
        """
        Supprime une alerte de la base de données.
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM alerts WHERE alert_id = ?", (alert_id,))

    def find_alert_by_id(self, alert_id):
        """
        Récupère une alerte par son ID.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM alerts WHERE alert_id = ?", (alert_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "alert_id": row[0],
                    "user_id": row[1],
                    "asset_id": row[2],
                    "target_price": row[3],
                    "percentage_change": row[4],
                    "reference_price": row[5],
                }
            return None
        
    def find_all_alerts(self):
        """
        Récupère toutes les alertes de la base de données.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM alerts")
            alerts = []
            for row in cursor.fetchall():
                alert = {
                    "alert_id": row[0],
                    "user_id": row[1],
                    "asset_id": row[2],
                    "target_price": row[3],
                    "percentage_change": row[4],
                    "reference_price": row[5],
                }
                alerts.append(alert)
            return alerts