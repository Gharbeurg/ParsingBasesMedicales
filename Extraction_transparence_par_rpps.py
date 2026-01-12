import csv

# Chemins des fichiers
fichier_identifiants = "C:/PYTHON/.entree/liste_rpps_hematologie.txt"          # fichier A
fichier_transparence = "C:/PYTHON/.entree/declarations.csv"
fichier_sortie = "C:/PYTHON/.data/declarations_filtres.txt"

# 1. Charger les identifiants du fichier A
with open(fichier_identifiants, "r", encoding="utf-8") as f:
    identifiants = {ligne.strip() for ligne in f if ligne.strip()}

# 2. Parcourir le fichier transparence et filtrer
lignes_selectionnees = []

with open(fichier_transparence, "r", encoding="utf-8") as f:
    lecteur = csv.DictReader(f, delimiter=";")
    for row in lecteur:
        if row["beneficiaire_identifiant"] in identifiants:
            lignes_selectionnees.append(row)

# 3. Écrire les lignes trouvées dans un fichier texte
with open(fichier_sortie, "w", encoding="utf-8") as f:
    for row in lignes_selectionnees:
        f.write(";".join(row.values()) + "\n")

print(f"Nombre de lignes sélectionnées : {len(lignes_selectionnees)}")
print(f"Résultat écrit dans : {fichier_sortie}")
