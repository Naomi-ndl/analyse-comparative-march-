# Analyse comparative de marché

## Présentation du projet

Ce projet consiste à développer une application en Python permettant de comparer les prix de plusieurs magasins afin d'aider les consommateurs à identifier les offres les plus avantageuses.

Les trois magasins étudiés sont :

- Marché Lagune
- Baobab Shop
- Comptoir Ivoire

## Objectifs

- Charger les données provenant de plusieurs sources.
- Nettoyer et organiser les données.
- Identifier les produits communs aux différents magasins.
- Comparer les prix et déterminer les magasins les moins chers.
- Calculer les économies possibles sur un panier de produits.
- Analyser l'évolution historique des prix.
- Mesurer les temps d'exécution du programme.

## Technologies utilisées

- Python
- Pandas
- OpenPyXL
- JSON
- CSV
- Excel

## Structure du projet
```
ANALYSE_COMPARATIVE/
│
├── Data/
│   ├── baobab_shop.json
│   ├── catalogue_reference.csv
│   ├── comptoir_ivoire.xlsx
│   ├── historique_prix.csv
│   └── marche_lagune.csv
│
├── app/
│   ├── chargement.py
│   ├── comparaison.py
│   ├── historique.py
│   ├── journal.py
│   ├── nettoyage.py
│   ├── panier.py
│   ├── rapprochement.py
│   └── synthese.py
│
├── resultats/
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. \

## Exécution du programme

Lancer l'application avec :
```
python main.py
```

## Résultats

Les résultats des analyses sont enregistrés dans le dossier `resultats/`, notamment :

- Comparaison des prix.
- Synthèse des magasins.
- Classement des magasins.
- Analyse historique des prix.
- Calcul du panier par magasin.
- Calcul du panier mixte.
- Journal de nettoyage des données.
