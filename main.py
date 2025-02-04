from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Depends, Request
#Ajout d'une routine pour mettre a jour les données de recommandation
from processing.knn import recommander_par_favoris
from scheduler import preparing_backup
import schedule, time
import threading
from typing import List
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Tâches avant le lancement de l'API")
    preparing_backup()
    yield
    print("Tâches avant l'arrêt de l'API")
# Exemple de route sécurisée avec Google Auth
app = FastAPI(lifespan=lifespan)


@app.post("/get_fav_montures")
async def secure_endpoint(request: Request ):
    """
    Route protégée : retourne les données sécurisées si le token Google est valide.
    """
    data = await request.json() 
    if "monture_list" not in data:
        raise HTTPException(status_code=400, detail="Aucune monture fournie")
    
    filtered_monture = recommander_par_favoris(data["monture_list"])

    return {"monture": filtered_monture}







# Fonction qui exécute le scheduler en arrière-plan
def run_scheduler():
    print("Démarrage du scheduler")
    schedule.every().day.at("01:00").do(preparing_backup)
    while True:
        schedule.run_pending()
        time.sleep(60)  # Vérifie chaque minute

# Démarrer le scheduler dans un thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()