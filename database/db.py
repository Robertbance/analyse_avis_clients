import mysql.connector
from mysql.connector import Error

from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


def get_db_connection():
    """
    Crée et retourne une connexion MySQL
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except Error as e:
        print("Erreur de connexion à MySQL :", e)
        return None
