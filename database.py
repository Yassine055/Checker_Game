import mysql.connector

def enregistrer_score(nom_joueur, score_noir, score_blanc, gagnant, niveau_ia):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",        # Utilisateur sans mot de passe
            password="",        # Important : vide !
            database="dame"
        )
        cursor = conn.cursor()
        sql = """
            INSERT INTO scores 
            (nom_joueur, score_noir, score_blanc, gagnant, niveau_ia)
            VALUES (%s, %s, %s, %s, %s)
        """
        valeurs = (nom_joueur, score_noir, score_blanc, gagnant, niveau_ia)
        cursor.execute(sql, valeurs)
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Score enregistré dans la base de données.")
    except Exception as e:
        print("❌ Erreur lors de l'enregistrement :", e)
