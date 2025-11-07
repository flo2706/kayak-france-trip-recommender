<h1 align="center">Jedha's ML Engineer Certificate</h1>
<h2 align="center">Bloc 1 : Construire et gérer une infrastructure de données</h2>

<p align="center"><strong>Une étude de cas :</strong></p>

<p align="center">
  Projet Kayak — <em>Infrastructure & Pipeline de Données pour la Recommandation Touristique</em><br>
</p>


---

## Contexte du projet  

L’objectif du projet est de concevoir une **infrastructure de données automatisée** permettant d’aider l’équipe marketing de **Kayak** à recommander les **meilleures destinations touristiques en France**, en se basant sur :  

- Le top 35 des villes à visiter selon **One Week In**,  
- Les **conditions météorologiques** (API OpenWeather),  
- Les **notes et disponibilités des hôtels** (scraping Booking).  

Le projet couvre l’ensemble d’un **pipeline ETL complet** :  
1️⃣ Extraction des données → Scraping Booking + APIs OpenWeather & Nominatim  
2️⃣ Transformation et nettoyage → Pandas & Python  
3️⃣ Chargement → AWS S3 (Data Lake) & PostgreSQL sur AWS RDS (Data Warehouse)  
4️⃣ Visualisation → Streamlit & Plotly

---

## Objectifs principaux  

- Mettre en place une **infrastructure cloud scalable** sur AWS (S3 + RDS).  
- Centraliser, nettoyer et structurer les données issues de sources hétérogènes.  
- Créer une **application interactive** permettant d’explorer les meilleurs hôtels par ville.  
- Identifier les **meilleures destinations météo** grâce à un score combiné.  
- Assurer la **conformité RGPD** à toutes les étapes du traitement.  

---

## Stack technique  

| Catégorie | Technologies |
|------------|--------------|
| **Langage principal** | Python |
| **Librairies Data** | Pandas, Requests, Asyncio, Psycopg2 |
| **Scraping & APIs** | Scrapy, OpenWeather OneCall 3.0, Nominatim (OpenStreetMap) |
| **Base de données** | PostgreSQL (hébergée sur AWS RDS) |
| **Data Lake** | AWS S3 |
| **Visualisation** | Plotly & Streamlit |

---

## Résultats & visualisations  

### Application Streamlit  
- Visualisation des **meilleurs hôtels par ville** selon les avis clients Booking.  
- Filtres dynamiques : **note minimale** et **nombre d’hôtels à afficher**.  
- Affichage d’une **carte interactive** avec description, note et **lien Booking**.  

### Visualisation Plotly  
- **Carte météo** des **Top 5 villes françaises** avec le meilleur score météo combiné.   

_(Les captures d’écran sont disponibles dans le dossier `/Livrables/maps`.)_

---

## Conformité RGPD  

- Données **Booking** utilisées en **sample** uniquement.  
- Aucune donnée personnelle n’est stockée ni diffusée.  
- Respect des principes de **minimisation** et de **sécurité** des données.  

---

## Configuration  

Le projet utilise un fichier `.env` pour stocker les clés et identifiants nécessaires :  

```ini
# AWS
AWS_KEY=VOTRE_AWS_KEY  
AWS_SECRET_KEY=VOTRE_AWS_SECRET_KEY  

# OpenWeather
OPENWEATHER_API_KEY=VOTRE_CLE_API  

# PostgreSQL
DBNAME=postgres  
USERNAME=mon_utilisateur  
PASSWORD=mon_mot_de_passe  
HOSTNAME=mon-instance-rds.amazonaws.com  
PORT=5432  

# User-Agent (obligatoire pour Nominatim)
USER_AGENT=KayakTripPlanner/1.0 (votre_email@example.com)
