import csv

# valeur recherchée dans la colonne "Libellé profession"
profession_cible = "Hématologie (option Onco-hématologie)"

# chemins des fichiers
fichier_entree = "C:/PYTHON/.entree/PS_LibreAcces_Personne_activite_202506200837.txt"
fichier_sortie = "C:/PYTHON/.data/liste_rpps_hematologie.txt"

# ouverture du fichier
with open(fichier_entree, encoding="utf-8") as f:
    lecteur = csv.DictReader(f, delimiter="|")
    
    # on récupère uniquement les identifiants correspondant à la profession voulue
    resultats = [
        ligne["Identifiant PP"]
        for ligne in lecteur
        if ligne["Libellé savoir-faire"].strip().lower() == profession_cible.lower()
    ]

# écriture dans le fichier final
with open(fichier_sortie, "w", encoding="utf-8") as f:
    for identifiant in resultats:
        f.write(identifiant + "\n")

print("Extraction terminée. Résultats enregistrés dans", fichier_sortie)

# affichage du nombre de lignes
print(f"Nombre de lignes dans le fichier de sortie : {len(resultats)}")
print("Résultats enregistrés dans", fichier_sortie)