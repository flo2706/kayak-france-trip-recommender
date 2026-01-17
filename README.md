<h1 align="center">Kayak France Trip Recommender</h1>

<p align="center">
  <em>Infrastructure & Pipeline de Données pour la Recommandation Touristique</em><br>
</p>

---

Ce projet met en place un pipeline de données permettant d’identifier et de recommander
les meilleures destinations touristiques en France, à partir de données météo
et d’informations hôtelières.

Il s’agit d’un cas d’usage inspiré de la plateforme **Kayak**, combinant ingestion de données
via APIs publiques, scraping web et stockage cloud, dans une logique data engineering.

---

## Problématique

Comment concevoir une infrastructure de données capable :

- d’ingérer des sources hétérogènes (APIs, scraping)
- de structurer et fiabiliser les données
- et d’exposer des indicateurs utiles à la prise de décision touristique ?

---

## Architecture du pipeline

1. **Extraction**
   - Géocodage des villes via Nominatim (OpenStreetMap)
   - Données météo via l’API OpenWeather (prévisions à 7 jours)
   - Données hôtelières via scraping Booking.com

2. **Transformation**
   - Nettoyage et normalisation des données en Python
   - Harmonisation des identifiants de villes
   - Contrôles de qualité (types, doublons, valeurs manquantes)
   - Calcul d’un score météo combiné

3. **Stockage et chargement**
   - Données nettoyées stockées sur AWS S3 (conformément aux consignes du projet)
   - Chargement des données structurées dans PostgreSQL sur AWS RDS

4. **Visualisation**
   - Cartes interactives des meilleures destinations selon un score météo combiné (Plotly) 
   - Application Streamlit pour explorer les hôtels les mieux notés
   - Les visualisations sont disponibles dans le dossier [`Livrables/maps`](Livrables/maps)

---

## Stack technique

| Catégorie | Technologies |
|---------|-------------|
| Langage | Python |
| Traitement de données | Pandas |
| APIs | OpenWeather, Nominatim |
| Scraping | Scrapy |
| Cloud | AWS S3, AWS RDS |
| Base de données | PostgreSQL |
| Visualisation | Plotly, Streamlit |


---

## Éthique & conformité

- Aucune donnée personnelle collectée.
- Données Booking utilisées à des fins pédagogiques et de démonstration.
- Le dépôt GitHub contient uniquement des échantillons (samples) des données,
  afin de ne pas exposer l’intégralité des informations scrappées (scraping limité et respectueux des ressources).
- Application des principes de minimisation et de sécurité des données.

---

## Contexte

Projet réalisé dans le cadre de la certification **« Concepteur Développeur en Science des Données » (RNCP 35288 – Jedha)**  
Bloc 1 : *Construire et gérer une infrastructure de données*. 
