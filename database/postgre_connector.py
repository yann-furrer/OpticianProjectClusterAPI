import psycopg2
import pandas as pd
import os 
from dotenv import load_dotenv
load_dotenv()
# Paramètres de connexion
DB_HOST = "autorack.proxy.rlwy.net"  # Remplace par l'adresse du serveur PostgreSQL
DB_NAME = "railway"    # Remplace par le nom de ta base de données
DB_USER = "postgres"   # Remplace par ton nom d'utilisateur
DB_PASSWORD = "cchOGELMaFogfbQOBOsxEYLgkXcRnZTX"  # Remplace par ton mot de passe
DB_PORT = "26152"       # Port PostgreSQL par défaut


def test_connection() -> bool:
    """
    Fonction pour tester la connexion à PostgreSQL et exécuter une requête simple.
    """
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        print("✅ Connexion à PostgreSQL réussie !")

        # Création du curseur
        cur = conn.cursor()

        # Exécution d'une requête de test
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"📌 Version de PostgreSQL : {db_version[0]}")

        # Fermeture propre des connexions
        cur.close()
        conn.close()
        print("✅ Connexion fermée proprement.")

        return True

    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
        return False


def get_data_for_knn() -> list :
    """
    Fonction pour récupérer les données de la db de modèle pour le KNN.
    """
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )

        # Création d'un curseur pour exécuter des requêtes
        cur = conn.cursor()
    
        cur.execute("SELECT * from public.montures INNER JOIN public.commandes ON public.montures.monture_id = public.commandes.monture_id WHERE public.montures.monture_id IS NOT NULL; ")
       
        data = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]

        df = pd.DataFrame(data[1:], columns=col_names)  # Enlever les titres de colonnes pour les mettre en header
        
        df.to_csv("processing/knn_file/dataset.csv", index=False, sep=";")



    except Exception as e:
        print(f"Erreur : {e}")
        conn.close()


