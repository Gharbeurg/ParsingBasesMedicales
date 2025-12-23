import os
import csv
from datetime import datetime

# --- Paramètres ---
fichier_entree = "C:/DATA/code/.data/declarations.csv"
fichier_sortie = "C:/DATA/code/.data/declarations_filtre.csv"

colonnes_a_garder = [
    "entreprise_id",
    "lien_interet",
    "motif_lien_interet_code",
    "motif_lien_interet",
    "autre_motif",
    "montant",
    "date",
    "id_beneficiaire",
    "beneficiaire_categorie_code",
    "beneficiaire_identifiant",
    "profession_libelle",
    "code_postal",
    "raison_sociale",
    "secteur_activite",
    "beneficiaire_nom_prenom_com_name",
]

# Si tu connais déjà le séparateur, mets par ex. delimiter=';' ici.
# Sinon laisse delimiter=None pour auto-détection.
delimiter = ";"
encoding = "utf-8"   # adapte si besoin (ex. "cp1252")


def filtrer_csv_streaming(path_in, path_out, colonnes, delimiter=delimiter, encoding="utf-8", progress_toutes=100_000):
    """Lit et écrit en flux (streaming), sans charger tout le fichier en mémoire.
    - colonnes : liste des noms de colonnes à conserver
    - delimiter : si None, auto-détection via csv.Sniffer
    - progress_toutes : affiche un point d’avancement tous les N enregistrements
    """
    # Auto-détection du séparateur si demandé
    writer_kwargs = {}
    reader_kwargs = {}

    reader_kwargs["delimiter"] = delimiter
    writer_kwargs["delimiter"] = delimiter

    # Ouverture des fichiers
    with open(path_in, "r", encoding=encoding, newline="") as fin, \
         open(path_out, "w", encoding=encoding, newline="") as fout:

        lecteur = csv.DictReader(fin, **reader_kwargs)

        # Vérifie les colonnes demandées
        colonnes_absentes = [c for c in colonnes if c not in lecteur.fieldnames]
        if colonnes_absentes:
            raise ValueError(f"Colonnes introuvables dans l'entrée : {colonnes_absentes}\n"
                             f"Colonnes disponibles : {lecteur.fieldnames}")

        # Écrit l’en-tête filtré
        ecrivain = csv.DictWriter(fout, fieldnames=colonnes, **writer_kwargs)
        ecrivain.writeheader()

        # Parcours et écriture au fil de l’eau
        n = 0
        for row in lecteur:
            # Construit une ligne réduite aux colonnes voulues
            ligne_filtre = {c: row.get(c, "") for c in colonnes}
            ecrivain.writerow(ligne_filtre)
            n += 1
            if progress_toutes and (n % progress_toutes == 0):
                print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Progression : {n} lignes traitées...")

    return n  # nombre de lignes écrites (hors en-tête)


if __name__ == "__main__":
    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Démarrage")
    if os.path.exists(fichier_sortie):
        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Suppression du fichier de sortie")
        os.remove(fichier_sortie)

    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Filtrage ligne par ligne")
    nb = filtrer_csv_streaming(
        fichier_entree,
        fichier_sortie,
        colonnes_a_garder,
        delimiter=delimiter,   # mets ';' ici si ton CSV est au point-virgule
        encoding=encoding,
        progress_toutes=200_000  # ajuste la fréquence d’affichage
    )

    print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} - Terminé. Lignes écrites (hors en-tête) : {nb}")
