# ENSO Monitor

## 1. Présentation

ENSO Monitor est une application web de visualisation des données historiques de l'indice climatique RONI (*Relative Oceanic Niño Index*).

L'objectif est de permettre à l'utilisateur de sélectionner une année, de visualiser les 12 valeurs mensuelles associées et de comparer deux années.

## 2. Fonctionnalités prévues

- Consultation des valeurs historiques du RONI.
- Sélection d'une année.
- Visualisation graphique de janvier à décembre.
- Comparaison de deux années.
- Traçabilité de la source et des imports de données.
- Gestion des valeurs manquantes et prévention des doublons.

## 3. Technologies

- Frontend : React, TypeScript et Vite.
- Backend : Python et FastAPI.
- Traitement des données : Python et Pandas.
- Base de données : PostgreSQL.
- Versionnement : Git.

## 4. Architecture

La source NOAA constitue la source de référence des données.
Un processus ETL Python sera chargé de récupérer,
valider, transformer et importer ces données dans PostgreSQL.

L'API FastAPI expose les données au frontend React sous forme de réponses JSON.

Le frontend ne communique pas directement avec PostgreSQL.

## 5. Structure du projet

- `frontend/` : interface React et TypeScript.
- `backend/` : API FastAPI.
- `etl/` : extraction, transformation et chargement des données.
- `database/` : schémas SQL et scripts de base de données.
- `docs/` : architecture, modèle de données et documentation API.
- `tests/` : tests du backend et de l'ETL.
- `requirements.txt` : dépendances Python.

## 6. Installation

### Prérequis

- Python 3.
- Node.js et npm.
- PostgreSQL.
- Git.

### Backend et ETL

À la racine du projet, créer et activer l'environnement virtuel :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Configurer ensuite la variable `DATABASE_URL` dans un fichier `.env` local.

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

### Base de données

Créer une base PostgreSQL nommée `enso_monitor`, puis appliquer le schéma défini dans `database/schema.sql` lorsque celui-ci sera prêt à être exécuté.

## 7. Données et conventions

Source envisagée : NOAA Climate Prediction Center, données RONI.

Les valeurs RONI sont associées à des saisons glissantes de trois mois. Pour la visualisation annuelle, chaque saison est affectée à son mois central.

Les dates sont stockées en base au format SQL `DATE`. Les horodatages techniques utilisent `TIMESTAMPTZ`.

La provenance, la version de la source et les imports doivent être documentés.


### Source des données climatiques

#### Indice utilisé

Relative Oceanic Niño Index (RONI).

#### Source officielle

NOAA - Climate Prediction Center (CPC).

URL :
https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt

Documentation :
https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/

#### Informations sur les données

- Format : ASCII / TXT
- Fréquence : saisonnière glissante (moyenne sur 3 mois)
- Période de référence : 1991-2020
- Version des données SST : ERSSTv6
- Unité : °C (anomalie de température)
- Première année disponible : 1950
- Date d'extraction : 30/10/2026

#### Structure des colonnes

| Colonne | Description |
|---|---|
| SEAS | Saison de trois mois |
| YR | Année de référence |
| ANOM | Anomalie RONI en °C |

#### Traitement

Les données originales sont conservées sans modification
dans `data/raw/RONI.ascii.txt`.

Le script `scripts/inspect_roni.py` permet de :
- Lire les données NOAA avec Pandas.
- Examiner leur structure.
- Détecter les valeurs manquantes.
- Identifier les doublons.
- Produire des statistiques descriptives.

#### Convention temporelle

Les observations NOAA correspondent à des moyennes
glissantes sur trois mois.

Pour la représentation annuelle, chaque saison est
associée à son mois central :

- DJF : janvier
- JFM : février
- FMA : mars
- MAM : avril
- AMJ : mai
- MJJ : juin
- JJA : juillet
- JAS : août
- ASO : septembre
- SON : octobre
- OND : novembre
- NDJ : décembre

Les périodes de trois mois se chevauchent.
Une valeur affichée pour un mois représente donc
une moyenne sur trois mois, et non une mesure
mensuelle indépendante.




## 8. Tests

Les tests automatisés couvriront progressivement :

- Le traitement et la validation des données.
- La prévention des doublons lors des imports.
- Les endpoints et leurs erreurs.
- Les données retournées au frontend.

## 9. Statut

Projet en cours de développement dans le cadre d'un projet de rattrapage HETIC.

## 10. Licence et attribution

La source, la version du jeu de données, les conditions d'utilisation applicables et les éventuelles obligations d'attribution seront précisées avant la publication des données.

