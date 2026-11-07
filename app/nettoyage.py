
import pandas as pd
import os

journal = []


def nettoyer_prix(prix, description=""):

    if pd.isna(prix):
        return None

    prix = str(prix)
    prix = prix.replace("FCFA", "")
    prix = prix.replace(" ", "")
    prix = prix.replace("\u202f", "")
    prix = prix.replace("\u00a0", "")

    try:
        return int(float(prix))
    except (ValueError, TypeError):
        journal.append(
            "Prix incorrect : " + description + " - " + prix
        )
        return None


def nettoyer_marche(marche):

    marche = marche.copy()

    # Détecter les références en double
    doublons = marche[marche.duplicated(
        subset=["reference"], keep=False
    )]

    for reference in doublons["reference"].unique():
        journal.append(
            "Référence en double au Marché Lagune : " + str(reference)
        )

    # Supprimer les doublons en conservant la première ligne
    marche = marche.drop_duplicates(
        subset=["reference"],
        keep="first"
    ).copy()

    # Nettoyer les prix actuels et anciens
    marche["prix"] = marche.apply(
        lambda ligne: nettoyer_prix(
            ligne["prix"], str(ligne["designation"])
        ),
        axis=1
    )

    marche["ancien_prix"] = marche.apply(
        lambda ligne: nettoyer_prix(
            ligne["ancien_prix"],
            "Ancien prix de " + str(ligne["designation"])
        ),
        axis=1
    )

    # Détecter les prix actuels anormalement élevés
    anomalies = marche[
        marche["prix"].notna()
        & marche["ancien_prix"].notna()
        & (marche["prix"] >= marche["ancien_prix"] * 2)
    ]

    for _, ligne in anomalies.iterrows():
        journal.append(
            "Prix anormalement élevé : "
            + str(ligne["designation"])
            + " | Prix actuel : "
            + str(ligne["prix"])
            + " FCFA | Ancien prix : "
            + str(ligne["ancien_prix"])
            + " FCFA"
        )

    # Déterminer la disponibilité
    marche["disponible"] = (
        (marche["disponibilite"].astype(str).str.strip().str.lower() != "rupture")
        & marche["prix"].notna()
    )

    journal.append("Nettoyage du Marché Lagune terminé.")

    return marche


def nettoyer_baobab(baobab):

    for produit in baobab["items"]:

        prix = produit["pricing"].get("amount")
        livraison = produit["pricing"].get("delivery_fee", 0)

        if prix is not None:
            prix = nettoyer_prix(
                prix, produit.get("title", "Baobab Shop")
            )
            livraison = nettoyer_prix(
                livraison, "Frais de livraison Baobab Shop"
            )

            if prix is not None and livraison is not None:
                produit["prix_paye"] = prix + livraison
            else:
                produit["prix_paye"] = None

        else:
            produit["prix_paye"] = None
            journal.append(
                "Prix manquant chez Baobab Shop : "
                + str(produit.get("title", "Produit inconnu"))
            )

        produit["disponible"] = (
            produit.get("stock", 0) > 0
            and produit["prix_paye"] is not None
        )

    journal.append("Nettoyage de Baobab Shop terminé.")

    return baobab


def nettoyer_comptoir(comptoir):

    comptoir = comptoir.copy()

    # Nettoyer les prix catalogue
    comptoir["prix_catalogue"] = (
        comptoir["Prix catalogue (FCFA)"]
        .apply(nettoyer_prix)
    )

    # Convertir les remises en nombres
    remise = pd.to_numeric(
        comptoir["Remise (%)"],
        errors="coerce"
    ).fillna(0)

    # Calculer le prix réellement payé après remise
    comptoir["prix_paye"] = (
        comptoir["prix_catalogue"] * (1 - remise / 100)
    ).round().astype("Int64")

    # Vérifier les quantités disponibles
    quantite = pd.to_numeric(
        comptoir["Quantité en rayon"],
        errors="coerce"
    ).fillna(0)

    comptoir["disponible"] = (
        (quantite > 0)
        & comptoir["prix_paye"].notna()
    )

    journal.append("Nettoyage du Comptoir Ivoire terminé.")

    return comptoir


def nettoyer_historique(historique):

    historique = historique.copy()

    historique["date"] = pd.to_datetime(
        historique["date"],
        errors="coerce"
    )

    historique["prix_fcfa"] = pd.to_numeric(
        historique["prix_fcfa"],
        errors="coerce"
    )

    historique = historique.dropna(
        subset=["date", "prix_fcfa"]
    )

    journal.append("Nettoyage de l'historique terminé.")

    return historique


def sauvegarder_journal():

    os.makedirs("resultats", exist_ok=True)

    with open(
        "resultats/journal_nettoyage.txt",
        "w",
        encoding="utf-8"
    ) as fichier:

        for ligne in journal:
            fichier.write(ligne + "\n")
