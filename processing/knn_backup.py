import joblib
import os

# Définir les chemins de sauvegarde
tfidf_path = "processing/knn_file/tfidf_matrix.pkl"
vectorizer_path = "processing/knn_file/vectorizer.pkl"
knn_path = "processing/knn_file/knn_model.pkl"
indices_path = "processing/knn_file/indices.pkl"


import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


def prepare_knn():
    # Charger le dataset
    file_path = "processing/knn_file/dataset.csv"  # Remplace par ton chemin de fichier
    df = pd.read_csv(file_path, sep=";")
    if os.path.exists(tfidf_path) and os.path.exists(vectorizer_path) and os.path.exists(knn_path) and os.path.exists(indices_path):
        print("✅ Chargement des modèles existants...")
        tfidf_matrix = joblib.load(tfidf_path)
        vectorizer = joblib.load(vectorizer_path)
        knn = joblib.load(knn_path)
        indices = joblib.load(indices_path)
    else:
        print("⚠️ Fichiers manquants, recalcul des modèles...")
        # Construire une représentation textuelle des montures à partir de caractéristiques clés
        df["features"] = df[["marque", "type", "forme", "materiau", "couleur", "style"]].astype(str).agg(" ".join, axis=1)

        # Transformer les caractéristiques en vecteurs TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(df["features"])

        # Utilisation d'un modèle KNN pour rechercher les montures les plus similaires
        knn = NearestNeighbors(n_neighbors=6, metric="cosine", algorithm="auto")
        knn.fit(tfidf_matrix)

        # Stocker la correspondance entre indices et Monture_ID
        indices = pd.Series(df.index, index=df["monture_id"]).drop_duplicates()

    
        # Sauvegarder les objets
        joblib.dump(tfidf_matrix, tfidf_path)
        joblib.dump(vectorizer, vectorizer_path)
        joblib.dump(knn, knn_path)
        joblib.dump(indices, indices_path)
        print("✅ Modèle et matrices sauvegardés avec succès.")
        return tfidf_matrix, vectorizer, knn, indices




# Fonction pour recommander des montures similaires à une seule monture
def recommander_montures_knn(monture_id, n=5):
    # Charger le dataset
    file_path = "processing/knn_file/dataset.csv"  # Remplace par ton chemin de fichier
    df = pd.read_csv(file_path, sep=";")
    tfidf_matrix = joblib.load(tfidf_path)
    vectorizer = joblib.load(vectorizer_path)
    knn = joblib.load(knn_path)
    indices = joblib.load(indices_path)
    if monture_id not in indices:
        return f"La monture {monture_id} n'est pas dans le dataset."
    
    idx = indices[monture_id]
    distances, indices_knn = knn.kneighbors(tfidf_matrix[idx], n_neighbors=n+1)
    
    # Exclure la monture elle-même (première recommandation)
    similar_indices = indices_knn[0][1:]
    
    similar_montures = df.iloc[similar_indices][["monture_id", "marque", "type", "forme", "materiau", "couleur", "style", "prix"]]
    
    return similar_montures








