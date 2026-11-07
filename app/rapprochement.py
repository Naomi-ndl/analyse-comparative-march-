
import unicodedata
import re
import pandas as pd

from app.nettoyage import journal


# Uniformiser les noms des produits
def normaliser(texte):

    if pd.isna(texte):
        return ""

    texte = str(texte).strip().upper()

    texte = unicodedata.normalize("NFD", texte)

    texte = "".join(
        caractere for caractere in texte
        if unicodedata.category(caractere) != "Mn"
    )

    texte = re.sub(r"[^A-Z0-9]", "", texte)

    return texte


# Enregistrer les produits non reconnus
def enregistrer_non_reconnu(nom, magasin):

    if pd.isna(nom) or not str(nom).strip():
        return

    journal.append(
        f"Produit non reconnu chez {magasin} : {nom}"
    )


# Correspondances du Marché Lagune
CORRESPONDANCES_MARCHE = {
    "SAMSUNG GALAXY A15 (128GB)": "P01",
    "SAMSUNG GALAXY A25 (128GB)": "P02",
    "SAMSUNG GALAXY A55 (256GB)": "P03",
    "TECNO SPARK 20 - 128GB": "P04",
    "TECNO CAMON 30 - 256GB": "P05",
    "INFINIX HOT 40I 128GB": "P06",
    "INFINIX NOTE 40 256GB": "P07",
    "ITEL A70 64GB": "P08",
    "IPHONE 13 128GB": "P09",
    "XIAOMI REDMI NOTE 13 128GB": "P10",
    "PC PORTABLE HP 250 G9 I5 8GB/512GB": "P11",
    "PC PORTABLE LENOVO IDEAPAD 3 I3 8GB/256GB": "P12",
    "PC PORTABLE DELL INSPIRON 15 I5 16GB/512GB": "P13",
    "CLE USB SANDISK 64GB": "P14",
    "DISQUE DUR EXTERNE SEAGATE 1TB": "P15",
    "SOURIS SANS FIL LOGITECH M185": "P16",
    "IMPRIMANTE HP DESKJET 2720E": "P17",
    "ECRAN SAMSUNG 24": "P19",
    "REFRIGERATEUR HISENSE 205L": "P20",
    "CONGELATEUR NASCO 200L": "P21",
    "TV SAMSUNG 43 CRYSTAL UHD 4K": "P22",
    "TV HISENSE 32": "P23",
    "CLIMATISEUR LG 1CV": "P24",
    "VENTILATEUR BINATONE 16": "P25",
    "MIXEUR MOULINEX 1.5L": "P26",
    "FER A REPASSER PHILIPS": "P27",
    "MICRO-ONDES SAMSUNG 23L": "P28",
    "CLIMATISEUR HISENSE 1.5CV": "P30"
}


# Correspondances de Baobab Shop
CORRESPONDANCES_BAOBAB = {
    "Galaxy A15 128GB - Samsung": "P01",
    "Galaxy A25 128GB - Samsung": "P02",
    "Galaxy A55 256GB - Samsung": "P03",
    "Spark 20 128GB - Tecno": "P04",
    "Camon 30 256GB - Tecno": "P05",
    "Hot 40i 128GB - Infinix": "P06",
    "Note 40 256GB - Infinix": "P07",
    "iPhone 13 128GB - Apple": "P09",
    "Redmi Note 13 128GB - Xiaomi": "P10",
    "HP Laptop 250 G9 (i5, 8GB, 512GB SSD)": "P11",
    "Lenovo IdeaPad 3 (i3, 8GB, 256GB SSD)": "P12",
    "SanDisk Ultra USB 64GB": "P14",
    "Seagate Expansion 1TB": "P15",
    "Logitech M185 Wireless Mouse": "P16",
    "HP DeskJet 2720e Printer": "P17",
    "TP-Link Archer C6 AC1200": "P18",
    "Samsung 24\" Monitor": "P19",
    "Hisense Fridge 205L": "P20",
    "Samsung 43\" Crystal UHD TV": "P22",
    "Hisense 32\" TV": "P23",
    "LG Air Conditioner 1HP": "P24",
    "Moulinex Blender 1.5L": "P26",
    "Philips Steam Iron": "P27",
    "Samsung Microwave 23L": "P28",
    "Electric Kettle 1.7L": "P29",
    "Hisense Air Conditioner 1.5HP": "P30"
}


# Correspondances du Comptoir Ivoire
CORRESPONDANCES_COMPTOIR = {
    "Samsun Galaxy A15 128Go": "P01",
    "Samsung A25 128Go": "P02",
    "Tecno Spark 20": "P04",
    "Infinix Hot 40i": "P06",
    "Itel A70": "P08",
    "iPhone 13 128Go": "P09",
    "HP 250 G9 i5": "P11",
    "Lenovo IdeaPad 3 i3": "P12",
    "Dell Inspiron 15 i5": "P13",
    "Clé USB SanDisk 64Go": "P14",
    "DD externe Seagate 1To": "P15",
    "Souris Logitech M185": "P16",
    "Frigo Hisense 205L": "P20",
    "Congélateur Nasco 200L": "P21",
    "TV Samsung 43\"": "P22",
    "TV Hisense 32\"": "P23",
    "Clim LG 1CV": "P24",
    "Ventilo Binatone 16\"": "P25",
    "Mixeur Moulinex": "P26",
    "Fer Philips": "P27",
    "Micro-ondes Samsung 23L": "P28",
    "Bouilloire 1,7L": "P29"
}


# Normaliser les clés des dictionnaires
CORRESPONDANCES_MARCHE = {
    normaliser(cle): valeur
    for cle, valeur in CORRESPONDANCES_MARCHE.items()
}

CORRESPONDANCES_BAOBAB = {
    normaliser(cle): valeur
    for cle, valeur in CORRESPONDANCES_BAOBAB.items()
}

CORRESPONDANCES_COMPTOIR = {
    normaliser(cle): valeur
    for cle, valeur in CORRESPONDANCES_COMPTOIR.items()
}


# Rapprocher les produits des trois magasins
def rapprocher_tous(marche, baobab, comptoir, catalogue=None):

    marche = marche.copy()
    comptoir = comptoir.copy()

    # Marché Lagune
    marche["produit_id"] = marche["designation"].apply(
        lambda nom: CORRESPONDANCES_MARCHE.get(normaliser(nom))
    )

    # Baobab Shop
    for produit in baobab["items"]:

        produit["produit_id"] = CORRESPONDANCES_BAOBAB.get(
            normaliser(produit.get("title"))
        )

    # Comptoir Ivoire
    comptoir["produit_id"] = comptoir["Article"].apply(
        lambda nom: CORRESPONDANCES_COMPTOIR.get(normaliser(nom))
    )

    # Vérifier les identifiants avec le catalogue officiel
    if catalogue is not None:

        identifiants_valides = set(
            catalogue["produit_id"].dropna().astype(str)
        )

        marche.loc[
            ~marche["produit_id"].isin(identifiants_valides),
            "produit_id"
        ] = None

        comptoir.loc[
            ~comptoir["produit_id"].isin(identifiants_valides),
            "produit_id"
        ] = None

        for produit in baobab["items"]:

            if str(produit.get("produit_id")) not in identifiants_valides:
                produit["produit_id"] = None

    # Enregistrer les produits non reconnus du Marché Lagune
    for _, produit in marche[
        marche["produit_id"].isna()
    ].iterrows():

        enregistrer_non_reconnu(
            produit["designation"],
            "Marché Lagune"
        )

    # Enregistrer les produits non reconnus de Baobab Shop
    for produit in baobab["items"]:

        if produit.get("produit_id") is None:

            enregistrer_non_reconnu(
                produit.get("title"),
                "Baobab Shop"
            )

    # Enregistrer les produits non reconnus du Comptoir Ivoire
    for _, produit in comptoir[
        comptoir["produit_id"].isna()
    ].iterrows():

        enregistrer_non_reconnu(
            produit["Article"],
            "Comptoir Ivoire"
        )

    return marche, baobab, comptoir
