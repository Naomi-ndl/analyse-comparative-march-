
import time
import pandas as pd

from app.chargement import charger_donnees

from app.nettoyage import (
    nettoyer_marche,
    nettoyer_baobab,
    nettoyer_comptoir,
    nettoyer_historique,
    sauvegarder_journal
)

from app.rapprochement import rapprocher_tous
from app.comparaison import comparer_prix
from app.synthese import creer_synthese
from app.panier import calculer_panier
from app.historique import analyser_historique


# --------------------------------------------------
# AFFICHER LES RESULTATS SANS TABLEAUX
# --------------------------------------------------

def afficher_donnees(titre, donnees):

    print("\n" + titre)
    print("-" * 65)

    if donnees is None:
        print("Aucun résultat disponible.")
        return

    if isinstance(donnees, pd.DataFrame):

        if donnees.empty:
            print("Aucune donnée disponible.")
            return

        for _, ligne in donnees.iterrows():

            elements = []

            for colonne, valeur in ligne.items():

                if pd.isna(valeur):
                    continue

                if isinstance(valeur, float):
                    valeur = round(valeur, 2)

                elements.append(f"{colonne} : {valeur}")

            print(" | ".join(elements))

    else:
        print(donnees)


# --------------------------------------------------
# TRAITEMENT AUTOMATIQUE
# --------------------------------------------------

def executer_analyse():

    temps = {}
    debut_total = time.perf_counter()

    # 1. Chargement
    debut = time.perf_counter()

    catalogue, marche, baobab, comptoir, historique = charger_donnees()

    temps["Chargement"] = time.perf_counter() - debut

    nombre_historique = len(historique)

    # 2. Nettoyage
    debut = time.perf_counter()

    marche = nettoyer_marche(marche)
    baobab = nettoyer_baobab(baobab)
    comptoir = nettoyer_comptoir(comptoir)
    historique = nettoyer_historique(historique)

    temps["Nettoyage"] = time.perf_counter() - debut

    # 3. Rapprochement
    debut = time.perf_counter()

    marche, baobab, comptoir = rapprocher_tous(
        marche,
        baobab,
        comptoir,
        catalogue
    )

    temps["Rapprochement"] = time.perf_counter() - debut

    # Sauvegarder le journal après le nettoyage et le rapprochement
    sauvegarder_journal()

    # 4. Comparaison des prix
    debut = time.perf_counter()

    comparaison = comparer_prix(
        marche,
        baobab,
        comptoir,
        catalogue
    )

    temps["Comparaison"] = time.perf_counter() - debut

    # 5. Synthèse
    debut = time.perf_counter()

    resume, top3 = creer_synthese(comparaison)

    temps["Synthèse"] = time.perf_counter() - debut

    # 6. Panier
    debut = time.perf_counter()

    totaux, panier_mixte, total_mixte = calculer_panier(
        marche,
        baobab,
        comptoir,
        catalogue
    )

    temps["Calcul du panier"] = time.perf_counter() - debut

    # 7. Historique
    debut = time.perf_counter()

    resultat_historique, resume_historique, temps_historique = (
        analyser_historique(historique, catalogue)
    )

    temps["Analyse historique"] = time.perf_counter() - debut
    temps["Temps interne historique"] = temps_historique

    temps["Temps total"] = time.perf_counter() - debut_total

    return {
        "catalogue": catalogue,
        "comparaison": comparaison,
        "resume": resume,
        "top3": top3,
        "totaux": totaux,
        "panier_mixte": panier_mixte,
        "total_mixte": total_mixte,
        "historique": resultat_historique,
        "resume_historique": resume_historique,
        "temps": temps,
        "nombre_historique": nombre_historique
    }


# --------------------------------------------------
# CHOIX 1 : RESULTATS
# --------------------------------------------------

def afficher_resultats(resultats):

    print("\n" + "=" * 65)
    print("              RESULTATS DE L'ANALYSE")
    print("=" * 65)

    afficher_donnees(
        "1. COMPARAISON DES PRIX",
        resultats["comparaison"]
    )

    afficher_donnees(
        "2. SYNTHESE PAR MAGASIN",
        resultats["resume"]
    )

    afficher_donnees(
        "3. TOP 3 DES ECONOMIES",
        resultats["top3"]
    )

    afficher_donnees(
        "4. PANIER PAR MAGASIN",
        resultats["totaux"]
    )

    afficher_donnees(
        "5. DETAIL DU PANIER MIXTE",
        resultats["panier_mixte"]
    )

    if resultats["total_mixte"] is not None:
        print(
            "\nCoût total du panier mixte : "
            f"{resultats['total_mixte']} FCFA"
        )
    else:
        print("\nLe panier mixte est incomplet.")

    afficher_donnees(
        "6. ANALYSE BLACK FRIDAY PAR PRODUIT",
        resultats["historique"]
    )

    afficher_donnees(
        "7. RESUME HISTORIQUE PAR MAGASIN",
        resultats["resume_historique"]
    )

    print(
        "\nLes fichiers détaillés sont enregistrés "
        "dans le dossier resultats."
    )


# --------------------------------------------------
# CHOIX 2 : COMPLEXITE
# --------------------------------------------------

def afficher_complexite(resultats):

    print("\n" + "=" * 65)
    print("          COMPLEXITE ALGORITHMIQUE")
    print("=" * 65)

    print("\nVOLUME DES DONNEES")
    print("-" * 65)

    print(
        "Produits dans le catalogue :",
        len(resultats["catalogue"])
    )

    print(
        "Lignes historiques chargées :",
        resultats["nombre_historique"]
    )

    print("\nTEMPS D'EXECUTION")
    print("-" * 65)

    for operation, duree in resultats["temps"].items():
        print(f"{operation} : {duree:.6f} seconde(s)")

    print("\nCOMPLEXITE DES ALGORITHMES")
    print("-" * 65)

    print("Dictionnaire : O(1) en moyenne pour rechercher un produit.")
    print("Parcours des données : O(n).")
    print("Tri : O(n log n).")
    print("Regroupement Pandas : environ O(n) en moyenne.")
    print("Mémoire : O(n) pour conserver les données en mémoire.")

    print("\nGESTION DES DONNEES HISTORIQUES")
    print("-" * 65)

    print(
        "Les 20 876 lignes historiques sont traitées avec Pandas. "
        "Les filtres et les regroupements permettent d'analyser "
        "les prix par produit et par magasin."
    )

    print(
        "Le dictionnaire sert à retrouver rapidement les produits, "
        "tandis que Pandas facilite le traitement des données."
    )


# --------------------------------------------------
# MENU PRINCIPAL
# --------------------------------------------------

def main():

    print("\nChargement et analyse des données en cours...")

    try:
        resultats = executer_analyse()

    except Exception as erreur:
        print("\nErreur pendant l'analyse :", erreur)
        return

    print("\nAnalyse terminée.")

    while True:

        print("\n" + "=" * 65)
        print("          ANALYSE COMPARATIVE DE MARCHE")
        print("=" * 65)

        print("1. Afficher les résultats de l'analyse")
        print("2. Afficher l'analyse de la complexité algorithmique")
        print("0. Quitter")

        choix = input("\nVotre choix : ").strip()

        if choix == "1":
            afficher_resultats(resultats)

        elif choix == "2":
            afficher_complexite(resultats)

        elif choix == "0":
            print("\nFin du programme.")
            break

        else:
            print("\nChoix invalide. Choisissez 1, 2 ou 0.")


if __name__ == "__main__":
    main()
