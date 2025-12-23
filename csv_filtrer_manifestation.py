import os
import csv
from datetime import datetime

# --- Paramètres ---
fichier_entree = "C:/DATA/code/.data/declarations_medecins.csv"
fichier_sortie = "C:/DATA/code/.data/declarations_medecins_IC.csv"

colonne_cible = "motif_lien_interet_code" #Médecin
# colonne_cible = "beneficiaire_nom_prenom_com_name" #fournisseurs
motif = "IC"

delimiter = ";"     # séparateur du CSV
encoding = "utf-8"  # change si ton fichier est en cp1252 ou latin-1


def extraire_lignes(path_in, path_out, colonne, motif, delimiter=";", encoding="utf-8", progress_toutes=100_000):
    """Extrait en streaming les lignes où `colonne` contient `motif` (insensible à la casse)."""
    n_total = 0
    n_matches = 0

    with open(path_in, "r", encoding=encoding, newline="") as fin, \
         open(path_out, "w", encoding=encoding, newline="") as fout:

        lecteur = csv.DictReader(fin, delimiter=delimiter)
        if colonne not in lecteur.fieldnames:
            raise ValueError(f"Colonne '{colonne}' introuvable. Colonnes disponibles : {lecteur.fieldnames}")

        ecrivain = csv.DictWriter(fout, fieldnames=lecteur.fieldnames, delimiter=delimiter)
        ecrivain.writeheader()

        for row in lecteur:
            n_total += 1
            valeur = row.get(colonne, "")
            if valeur and motif.lower() in valeur.lower():
                ecrivain.writerow(row)
                n_matches += 1

            if progress_toutes and n_total % progress_toutes == 0:
                print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - {n_total} lignes lues, {n_matches} extraites...")

    return n_total, n_matches


if __name__ == "__main__":
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Démarrage")

    if os.path.exists(fichier_sortie):
        os.remove(fichier_sortie)
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Fichier de sortie supprimé")

    n_total, n_matches = extraire_lignes(
        fichier_entree,
        fichier_sortie,
        colonne=colonne_cible,
        motif=motif,
        delimiter=delimiter,
        encoding=encoding,
        progress_toutes=200_000
    )

    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Terminé.")
    print(f"Lignes lues : {n_total}")
    print(f"Lignes extraites : {n_matches}")
    print(f"Résultat : {fichier_sortie}")