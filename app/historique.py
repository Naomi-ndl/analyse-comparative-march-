
import pandas as pd
import time
import os


def analyser_historique(historique, catalogue):

    debut = time.perf_counter()

    # Définir les périodes à comparer
    debut_annee = "2025-11-01"
    fin_annee = "2026-10-31"

    debut_black_friday = "2025-11-24"
    fin_black_friday = "2025-11-30"

    # Garder uniquement la période annuelle
    historique = historique[
        (historique["date"] >= debut_annee)
        & (historique["date"] <= fin_annee)
    ].copy()

    # Calculer le prix moyen annuel par magasin et produit
    moyenne_annuelle = historique.groupby(
        ["source", "produit_id"]
    )["prix_fcfa"].mean().reset_index()

    moyenne_annuelle = moyenne_annuelle.rename(
        columns={"prix_fcfa": "prix_moyen_annuel"}
    )

    # Extraire les prix de la semaine du Black Friday
    black_friday = historique[
        (historique["date"] >= debut_black_friday)
        & (historique["date"] <= fin_black_friday)
    ]

    moyenne_bf = black_friday.groupby(
        ["source", "produit_id"]
    )["prix_fcfa"].mean().reset_index()

    moyenne_bf = moyenne_bf.rename(
        columns={"prix_fcfa": "prix_moyen_black_friday"}
    )

    # Comparer les deux moyennes
    analyse = pd.merge(
        moyenne_annuelle,
        moyenne_bf,
        on=["source", "produit_id"],
        how="left"
    )

    # Calculer l'économie réalisée pendant le Black Friday
    analyse["ecart_fcfa"] = (
        analyse["prix_moyen_annuel"]
        - analyse["prix_moyen_black_friday"]
    )

    analyse["reduction_pourcentage"] = (
        analyse["ecart_fcfa"]
        / analyse["prix_moyen_annuel"] * 100
    ).round(2)

    # Donner un conseil selon les résultats
    def donner_conseil(ligne):

        if pd.isna(ligne["prix_moyen_black_friday"]):
            return "Aucune donnée Black Friday"

        if ligne["ecart_fcfa"] > 0:
            return "Acheter pendant le Black Friday"

        elif ligne["ecart_fcfa"] < 0:
            return "Comparer les prix hors Black Friday"

        else:
            return "Prix identiques"

    analyse["conseil"] = analyse.apply(
        donner_conseil,
        axis=1
    )

    # Ajouter les noms des produits
    noms = catalogue.set_index("produit_id")["nom"]

    analyse["nom_produit"] = analyse["produit_id"].map(noms)

    # Résumé par magasin
    resume = analyse.groupby("source").agg(
        nombre_produits=("produit_id", "count"),
        economie_moyenne=("reduction_pourcentage", "mean")
    ).reset_index()

    resume["economie_moyenne"] = (
        resume["economie_moyenne"].round(2)
    )

    # Mesurer le temps d'exécution
    fin = time.perf_counter()
    duree = fin - debut

    os.makedirs("resultats", exist_ok=True)

    analyse.to_csv(
        "resultats/analyse_historique.csv",
        index=False,
        encoding="utf-8-sig"
    )

    resume.to_csv(
        "resultats/resume_historique.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return analyse, resume, duree
