
from datetime import datetime
import os


def enregistrer_journal(message):

    os.makedirs("resultats", exist_ok=True)

    with open(
        "resultats/journal_execution.txt",
        "a",
        encoding="utf-8"
    ) as fichier:

        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        fichier.write(f"[{date}] {message}\n")


def afficher_journal():

    chemin = "resultats/journal_execution.txt"

    if os.path.exists(chemin):

        with open(chemin, "r", encoding="utf-8") as fichier:
            print(fichier.read())

    else:
        print("Aucun journal disponible.")
