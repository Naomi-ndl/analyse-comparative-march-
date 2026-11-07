
import pandas as pd

# Produits demandés dans le panier
PANIER = {
    "P04": 1,  # Tecno Spark 20
    "P12": 1,  # Lenovo IdeaPad 3
    "P14": 2,  # Clés USB SanDisk
    "P15": 1,  # Disque dur Seagate
    "P28": 1   # Micro-ondes Samsung
}


def calculer_panier(marche, baobab, comptoir, catalogue):

    offres = []

    # Récupérer les offres du Marché Lagune
    for _, produit in marche.iterrows():
        offres.append({
            "produit_id": produit["produit_id"],
            "magasin": "Marché Lagune",
            "prix": produit["prix"],
            "disponible": produit["disponible"]
        })

    # Récupérer les offres de Baobab Shop
    for produit in baobab["items"]:
        offres.append({
            "produit_id": produit["produit_id"],
            "magasin": "Baobab Shop",
            "prix": produit["prix_paye"],
            "disponible": produit["disponible"]
        })

    # Récupérer les offres du Comptoir Ivoire
    for _, produit in comptoir.iterrows():
        offres.append({
            "produit_id": produit["produit_id"],
            "magasin": "Comptoir Ivoire",
            "prix": produit["prix_paye"],
            "disponible": produit["disponible"]
        })

    donnees = pd.DataFrame(offres)

    donnees = donnees[
        donnees["produit_id"].notna()
        & donnees["disponible"]
        & donnees["prix"].notna()
    ]

    noms = catalogue.set_index("produit_id")["nom"].to_dict()

    # Dictionnaire pour retrouver rapidement le prix d'un produit
    prix_par_produit = {}

    for _, ligne in donnees.iterrows():
        cle = (ligne["produit_id"], ligne["magasin"])
        prix = ligne["prix"]

        if cle not in prix_par_produit:
            prix_par_produit[cle] = prix
        else:
            prix_par_produit[cle] = min(
                prix_par_produit[cle], prix
            )

    magasins = [
        "Marché Lagune",
        "Baobab Shop",
        "Comptoir Ivoire"
    ]

    # Calcul du panier complet dans chaque magasin
    resultats_magasins = []

    for magasin in magasins:
        total = 0
        complet = True

        for produit_id, quantite in PANIER.items():
            cle = (produit_id, magasin)

            if cle in prix_par_produit:
                total += prix_par_produit[cle] * quantite
            else:
                complet = False
                break

        if complet:
            resultats_magasins.append({
                "magasin": magasin,
                "total_fcfa": total
            })

    panier_magasins = pd.DataFrame(resultats_magasins)

    # Calcul du panier mixte
    resultats_mixtes = []
    total_mixte = 0
    panier_complet = True

    for produit_id, quantite in PANIER.items():

        offres_produit = []

        for magasin in magasins:
            cle = (produit_id, magasin)

            if cle in prix_par_produit:
                offres_produit.append({
                    "magasin": magasin,
                    "prix": prix_par_produit[cle]
                })

        if offres_produit:
            meilleure_offre = min(
                offres_produit,
                key=lambda offre: offre["prix"]
            )

            prix = meilleure_offre["prix"]
            magasin = meilleure_offre["magasin"]

            total_mixte += prix * quantite

        else:
            prix = None
            magasin = "Indisponible"
            panier_complet = False

        resultats_mixtes.append({
            "produit_id": produit_id,
            "nom_produit": noms.get(produit_id, produit_id),
            "quantite": quantite,
            "magasin": magasin,
            "prix_unitaire": prix
        })

    panier_mixte = pd.DataFrame(resultats_mixtes)

    if not panier_complet:
        total_mixte = None

    return panier_magasins, panier_mixte, total_mixte
