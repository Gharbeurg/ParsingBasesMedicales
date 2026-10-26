
import csv
import os

# ============================================================
# PARAMÈTRES
# ============================================================

# Spécialité médicale recherchée
# Exemples : "Médecine interne", "Pneumologie", "Cardiologie"
profession_cible = "Cardiologie et maladies vasculaires"

# Chemin du fichier source
fichier_entree = (
    "C:/PYTHON/.entree/basesmedicales/"
    "ps-libreacces-personne-activite_20261013.txt"
)

# Chemin du fichier de sortie
fichier_sortie = "C:/PYTHON/.data/liste_rpps_cardiologues.txt"

# Colonne utilisée pour filtrer les professionnels
colonne_filtre = "Libellé savoir-faire"


# ============================================================
# EXTRACTION
# ============================================================

nombre_lignes = 0

try:
    # Création du dossier de sortie si nécessaire
    dossier_sortie = os.path.dirname(fichier_sortie)

    if dossier_sortie:
        os.makedirs(dossier_sortie, exist_ok=True)

    # Lecture du fichier source
    with open(
        fichier_entree,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as entree:

        lecteur = csv.DictReader(
            entree,
            delimiter="|"
        )

        # Récupération de toutes les colonnes
        colonnes = lecteur.fieldnames

        if not colonnes:
            raise ValueError("Le fichier source est vide.")

        # Vérification de la présence de la colonne recherchée
        if colonne_filtre not in colonnes:
            raise ValueError(
                f"Colonne introuvable : {colonne_filtre}"
            )

        # Création du fichier de sortie
        with open(
            fichier_sortie,
            mode="w",
            encoding="utf-8",
            newline=""
        ) as sortie:

            redacteur = csv.DictWriter(
                sortie,
                fieldnames=colonnes,
                delimiter="|",
                extrasaction="ignore"
            )

            # Écriture de toutes les colonnes d'origine
            redacteur.writeheader()

            # Parcours du fichier source ligne par ligne
            for ligne in lecteur:

                specialite = (
                    ligne.get(colonne_filtre) or ""
                ).strip().casefold()

                # Filtrage sur la spécialité
                if specialite == profession_cible.strip().casefold():

                    # Écriture de la ligne complète
                    redacteur.writerow(ligne)

                    nombre_lignes += 1

    # ========================================================
    # BILAN
    # ========================================================

    print("Extraction terminée.")
    print(f"Spécialité : {profession_cible}")
    print(f"Nombre de lignes extraites : {nombre_lignes}")
    print(f"Nombre de colonnes : {len(colonnes)}")
    print(f"Fichier de sortie : {fichier_sortie}")

except FileNotFoundError:
    print(f"ERREUR : fichier introuvable : {fichier_entree}")

except (OSError, ValueError, csv.Error) as erreur:
    print(f"ERREUR : {erreur}")
