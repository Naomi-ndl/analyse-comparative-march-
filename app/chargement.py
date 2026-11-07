
import pandas as pd
import json

def charger_donnees():

    catalogue = pd.read_csv("data/catalogue_reference.csv")

    marche = pd.read_csv("data/marche_lagune.csv", sep=";")

    with open("data/baobab_shop.json", "r", encoding="utf-8") as fichier:
        baobab = json.load(fichier)

    comptoir = pd.read_excel(
        "data/comptoir_ivoire.xlsx",
        sheet_name="Tarifs octobre 2026",
        header=2
    )

    historique = pd.read_csv("data/historique_prix.csv")

    return catalogue, marche, baobab, comptoir, historique
