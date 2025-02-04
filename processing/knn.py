
import pandas as pd
from processing.knn_backup import indices_path, recommander_montures_knn, joblib
# Fonction pour recommander des montures similaires à une liste de montures favorites
def recommander_par_favoris(favoris_ids, n=5):
    # Charger le dataset
    file_path = "processing/knn_file/dataset.csv"  # Remplace par ton chemin de fichier
    df = pd.read_csv(file_path, sep=";")
    similar_montures_set = set()
    indices = joblib.load(indices_path)

    for monture_id in favoris_ids:
        if monture_id in indices:
            similar_montures = recommander_montures_knn(monture_id, n)
            similar_montures_set.update(similar_montures["monture_id"].tolist())

    # Supprimer les favoris de la liste des recommandations
    similar_montures_set.difference_update(favoris_ids)

    # Filtrer le dataset pour récupérer les informations des montures recommandées
    # Supposons que ton DataFrame recommandations soit déjà filtré comme ci-dessous :
    recommandations = df[df["monture_id"].isin(similar_montures_set)][[
        "monture_id", "marque", "type", "forme", "materiau", "couleur", "style", "prix"
    ]]

    # Regrouper par 'monture_id' et transformer en un tableau d'objets (dictionnaires)
    tableau_objets = (
        recommandations.groupby("monture_id")
        .apply(lambda x: x.to_dict(orient="records"))
        .reset_index()
        .rename(columns={0: "items"})
        .to_dict(orient="records")
    )

    # Trier par une colonne spécifique, par exemple 'prix' (on prend le prix du premier item du plateau)
    tableau_objets = recommandations.to_dict(orient="records")

    return tableau_objets

# # 🛠️ Test de la fonction
# favoris = ["MON11976", "MON17107"]  # Exemple de montures favorites
# recommandations = recommander_par_favoris(favoris)
# print(recommandations)
# # Afficher les recommandations
