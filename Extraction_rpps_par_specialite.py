import csv

# valeur recherchée dans la colonne "Libellé profession"
profession_cible = "pneumologie"

# chemins des fichiers
fichier_entree = "C:/DATA/code/.params/ps-libreacces-personne-activite.txt"
fichier_sortie = "C:/DATA/code/.data/liste_rpps.txt"

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