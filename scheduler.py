from database.postgre_connector import test_connection, get_data_for_knn
from processing.knn_backup import *
import os 

def preparing_backup():
    print("Backup en cours...")
    print("Execution de la routine")

    #Suppression des fichiers knn et requetage de la bdd
    test_connection()
    clean_knn_file()
    get_data_for_knn()
    prepare_knn()


    
   
     

def clean_knn_file():
    #supprimer les fichiers knn
    try :
        os.rmdir("processing/knn_file")
        os.mkdir("processing/knn_file")
        return True
    except:
        print("Fichier knn non trouvé")
        return False
    
