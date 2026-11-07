
import pandas as pd
import os


def creer_synthese(comparaison):

    magasins = [
        "Marché Lagune",
        "Baobab Shop",
        "Comptoir Ivoire"
    ]

    resume = []

    for magasin in magasins:

        prix = comparaison[magasin]

        # Compter le nombre de fois où le magasin est le moins cher
        moins_cher = (
            prix.notna()
            & (prix == comparaison["prix_min"])
        ).sum()

        # Calculer l'écart moyen par rapport au prix minimum
        ecarts = (
            (prix - comparaison["prix_min"])
            / comparaison["prix_min"] * 100
        )

        ecart_moyen = ecarts.mean()

        resume.append({
            "magasin": magasin,
            "fois_moins_cher": int(moins_cher),
            "ecart_moyen_pourcentage": round(ecart_moyen, 2)
            if pd.notna(ecart_moyen) else None
        })

    classement = pd.DataFrame(resume)

    # Trouver les trois produits avec les plus grandes économies possibles
    top3 = comparaison.sort_values(
        by="ecart_fcfa",
        ascending=False
    ).head(3)

    colonnes = [
        "produit_id",
        "nom_produit",
        "magasin_moins_cher",
        "prix_min",
        "prix_max",
        "ecart_fcfa",
        "ecart_pourcentage"
    ]

    top3 = top3[colonnes]

    os.makedirs("resultats", exist_ok=True)

    classement.to_csv(
        "resultats/synthese_enseignes.csv",
        index=False,
        encoding="utf-8-sig"
    )

    top3.to_csv(
        "resultats/top3_economies.csv",
        index=False,
        encoding="utf-8-sig"
    )

    return classement, top3
