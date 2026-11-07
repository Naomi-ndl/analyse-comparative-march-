import pandas as pd
import os

MAGASINS = [
    "Marché Lagune",
    "Baobab Shop",
    "Comptoir Ivoire"
]


def comparer_prix(marche, baobab, comptoir, catalogue):

    offres = []

    # Offres du Marché Lagune
    for _, produit in marche.iterrows():
        offres.append({
            "produit_id": produit["produit_id"],
            "magasin": "Marché Lagune",
            "prix": produit["prix"],
            "disponible": produit["disponible"]
        })

    # Offres de Baobab Shop
    for produit in baobab["items"]:
        offres.append({
            "produit_id": produit["produit_id"],
            "magasin": "Baobab Shop",
            "prix": produit["prix_paye"],
            "disponible": produit["disponible"]
        })

    # Offres du Comptoir Ivoire
    for _, produit in comptoir.iterrows():
        offres.append({
            "produit_id": produit["produit_id"],
            "magasin": "Comptoir Ivoire",
            "prix": produit["prix_paye"],
            "disponible": produit["disponible"]
        })

    donnees = pd.DataFrame(offres)

    # Garder uniquement les produits identifiés et disponibles
    donnees = donnees[
        donnees["produit_id"].notna()
        & donnees["disponible"]
        & donnees["prix"].notna()
    ]

    # Comparer les prix de chaque produit dans les magasins
    comparaison = donnees.pivot_table(
        index="produit_id",
        columns="magasin",
        values="prix",
        aggfunc="min"
    )

    comparaison = comparaison.reindex(columns=MAGASINS)

    # Garder les produits présents dans au moins deux magasins
    comparaison = comparaison[
        comparaison.notna().sum(axis=1) >= 2
    ]

    # Créer le dossier des résultats
    os.makedirs("resultats", exist_ok=True)

    # Cas où aucun produit n'est comparable
    if comparaison.empty:
        colonnes = [
            "produit_id",
            "Marché Lagune",
            "Baobab Shop",
            "Comptoir Ivoire",
            "prix_min",
            "prix_max",
            "magasin_moins_cher",
            "ecart_fcfa",
            "ecart_pourcentage",
            "nom_produit"
        ]

        comparaison = pd.DataFrame(columns=colonnes)

        comparaison.to_csv(
            "resultats/comparaison_prix.csv",
            index=False,
            encoding="utf-8-sig"
        )

        return comparaison

    # Prix minimum et maximum
    comparaison["prix_min"] = comparaison[MAGASINS].min(axis=1)
    comparaison["prix_max"] = comparaison[MAGASINS].max(axis=1)

    # Magasin le moins cher
    def trouver_moins_cher(ligne):
        magasins_moins_chers = [
            magasin for magasin in MAGASINS
            if ligne[magasin] == ligne["prix_min"]
        ]
        return ", ".join(magasins_moins_chers)

    comparaison["magasin_moins_cher"] = comparaison.apply(
        trouver_moins_cher,
        axis=1
    )

    # Écart entre le prix maximum et le prix minimum
    comparaison["ecart_fcfa"] = (
        comparaison["prix_max"] - comparaison["prix_min"]
    )

    # Écart en pourcentage
    comparaison["ecart_pourcentage"] = (
        comparaison["ecart_fcfa"] / comparaison["prix_min"] * 100
    ).round(2)

    # Ajouter le nom des produits
    noms = catalogue.set_index("produit_id")["nom"]

    comparaison["nom_produit"] = comparaison.index.map(noms)

    comparaison = comparaison.reset_index()

    # Exporter le tableau de comparaison en CSV
    comparaison.to_csv(
        "resultats/comparaison_prix.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return comparaison