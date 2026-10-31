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
- Gestion des valeurs manquantes.
- Prévention des doublons lors des imports.

## 3. Technologies

- **Frontend :** React, TypeScript et Vite.
- **Backend :** Python et FastAPI.
- **Traitement des données :** Python, Pandas et NumPy.
- **Base de données :** PostgreSQL.
- **Versionnement :** Git.

## 4. Architecture

La source NOAA constitue la source de référence des données.

Un processus ETL (*Extract, Transform, Load*) Python est chargé de récupérer, inspecter, valider, transformer et importer les données dans PostgreSQL.

L'API FastAPI expose les données au frontend React sous forme de réponses JSON.

Le frontend ne communique pas directement avec PostgreSQL.

Le flux général des données est le suivant :

1. Récupération des données depuis la source NOAA.
2. Inspection et validation des données brutes.
3. Nettoyage et transformation des observations.
4. Importation des données validées dans PostgreSQL.
5. Exposition des données par l'API FastAPI.
6. Affichage et visualisation dans l'interface React.

## 5. Structure du projet

- `frontend/` : interface React et TypeScript.
- `backend/` : API FastAPI.
- `etl/` : emplacement prévu pour les traitements ETL si ceux-ci sont regroupés ultérieurement.
- `scripts/` : scripts Python d'inspection et de transformation des données.
- `data/raw/` : données originales récupérées depuis NOAA.
- `data/processed/` : données nettoyées et transformées.
- `database/` : schémas SQL et scripts de base de données.
- `docs/` : architecture, modèle de données et documentation API.
- `tests/` : tests du backend et de l'ETL.
- `requirements.txt` : dépendances Python.

### Organisation actuelle des données

```text
data/
├── raw/
│   └── RONI.ascii.txt
│
└── processed/
    ├── roni_clean.csv
    └── roni_rejected.csv
```

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

### 7.1 Source des données climatiques

#### Indice utilisé

Relative Oceanic Niño Index (RONI).

#### Source officielle

NOAA - Climate Prediction Center (CPC).

**Fichier de données :**

https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt

**Documentation :**

https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso/roni/

#### Informations sur les données

- Format : ASCII / TXT.
- Fréquence : saisonnière glissante (moyenne sur 3 mois).
- Période de référence : 1991-2020.
- Version des données SST : ERSSTv6.
- Unité : °C (anomalie de température).
- Première année disponible : 1950.
- Date d'extraction : 30/10/2026.

#### Structure des colonnes originales

| Colonne | Description |
|---|---|
| `SEAS` | Saison de trois mois |
| `YR` | Année de référence |
| `ANOM` | Anomalie RONI en °C |

### 7.2 Conservation des données brutes

Les données originales sont conservées sans modification dans :

`data/raw/RONI.ascii.txt`

Ce fichier constitue la source de référence utilisée par les scripts de traitement.

Les données brutes ne doivent pas être modifiées directement. Les opérations de nettoyage et de transformation sont réalisées sur une copie chargée en mémoire avec Pandas.

### 7.3 Inspection des données

Le script `scripts/inspect_roni.py` permet de :

- Lire les données NOAA avec Pandas.
- Examiner la structure et les types des colonnes.
- Vérifier les valeurs manquantes.
- Identifier les doublons complets.
- Détecter les saisons invalides.
- Vérifier les doublons par année et saison.
- Examiner les années incomplètes.
- Produire des statistiques descriptives.
- Identifier la période couverte par le jeu de données.

**Commande d'exécution :**

```powershell
python scripts/inspect_roni.py
```

### 7.4 Transformation et nettoyage des données

Le script `scripts/transform_roni.py` réalise le traitement ETL des données NOAA.

Les principales étapes sont :

1. Lecture du fichier original avec Pandas.
2. Vérification des colonnes attendues.
3. Normalisation des libellés des saisons.
4. Validation des années et des valeurs RONI.
5. Identification des données invalides ou manquantes.
6. Détection des valeurs contradictoires pour une même année et saison.
7. Suppression des doublons exacts.
8. Association de chaque saison à son mois central.
9. Création d'une date de référence.
10. Export des données propres et des éventuelles lignes rejetées.

**Commande d'exécution :**

```powershell
python scripts/transform_roni.py
```

#### Fichiers générés

| Fichier | Description |
|---|---|
| `data/processed/roni_clean.csv` | Données validées et transformées, destinées à être exploitées par l'application et importées dans PostgreSQL. |
| `data/processed/roni_rejected.csv` | Lignes rejetées pendant le traitement, accompagnées de leur motif de rejet. |

Le fichier `roni_clean.csv` contient les colonnes suivantes :

| Colonne | Description |
|---|---|
| `date` | Date de référence correspondant au premier jour du mois central. |
| `year` | Année de référence. |
| `month` | Numéro du mois central (1 à 12). |
| `season` | Libellé de la saison NOAA. |
| `roni_value` | Valeur de l'indice RONI en °C. |

### 7.5 Résultats de l'inspection et de la transformation

**État du jeu de données au 31/10/2026 :**

| Indicateur | Résultat |
|---|---:|
| Nombre de lignes initiales | 920 |
| Nombre de lignes conservées | 920 |
| Nombre de lignes rejetées | 0 |
| Valeurs manquantes détectées | 0 |
| Doublons complets détectés | 0 |
| Doublons année/saison détectés | 0 |
| Saisons invalides détectées | 0 |
| Première année disponible | 1950 |
| Dernière année disponible | 2026 |
| Première date transformée | 1950-01-01 |
| Dernière date transformée | 2026-08-01 |

L'année 2026 comporte actuellement 8 observations. Cette situation est considérée comme une disponibilité partielle des données et non comme une anomalie nécessitant la suppression de l'année.

Les résultats seront actualisés lors des prochaines récupérations des données NOAA.

### 7.6 Convention temporelle

Les observations NOAA correspondent à des moyennes glissantes sur trois mois.

Pour la représentation annuelle, chaque saison est associée à son mois central :

| Saison | Mois central |
|---|---|
| DJF | Janvier |
| JFM | Février |
| FMA | Mars |
| MAM | Avril |
| AMJ | Mai |
| MJJ | Juin |
| JJA | Juillet |
| JAS | Août |
| ASO | Septembre |
| SON | Octobre |
| OND | Novembre |
| NDJ | Décembre |

Les périodes de trois mois se chevauchent.

Une valeur affichée pour un mois représente donc une moyenne mobile sur trois mois, et non une mesure mensuelle indépendante.

La date créée lors de la transformation correspond au premier jour du mois central. Elle constitue une date de référence informatique et non la date exacte d'une mesure ponctuelle.

Pour préserver la précision temporelle des observations dans PostgreSQL, les champs `period_start` et `period_end` seront également intégrés au modèle de données. Ils permettront de représenter les dates réelles de début et de fin de chaque période glissante de trois mois.

### 7.7 Stockage et traçabilité

Les dates des observations sont stockées en base au format SQL `DATE`.

Les horodatages techniques utilisent `TIMESTAMPTZ`.

La base de données doit permettre de conserver :

- La valeur RONI.
- La saison et la période correspondantes.
- La source NOAA.
- La date et les informations relatives à l'import.
- La traçabilité des opérations de traitement.

La provenance, la version de la source et les imports doivent être documentés afin de faciliter la vérification et la reproductibilité des données.

## 8. Tests

Les tests automatisés couvriront progressivement :

- Le traitement et la validation des données NOAA.
- La détection des valeurs invalides et des dates incorrectes.
- La prévention des doublons lors des imports.
- La gestion des données contradictoires.
- Les endpoints de l'API et leurs erreurs.
- Les données retournées au frontend.

Les tests de l'ETL devront notamment vérifier le comportement du traitement face aux doublons et aux observations invalides.

## 9. Statut

Projet en cours de développement dans le cadre d'un projet de rattrapage HETIC.

**État d'avancement au 31/10/2026 :**

- [x] Récupération du fichier NOAA RONI.
- [x] Inspection de la structure des données.
- [x] Vérification des valeurs manquantes et des doublons.
- [x] Création du script de transformation ETL.
- [x] Génération du fichier CSV nettoyé.
- [x] Génération du fichier des rejets.
- [ ] Finalisation des champs temporels de la transformation.
- [ ] Importation des données dans PostgreSQL.
- [ ] Connexion de l'API FastAPI à la base de données.
- [ ] Intégration des données dans le frontend React.
- [ ] Mise en place des tests automatisés.

## 10. Licence et attribution

Les données climatiques utilisées par ENSO Monitor proviennent du NOAA Climate Prediction Center.

La source, la version du jeu de données, les conditions d'utilisation applicables et les éventuelles obligations d'attribution seront précisées avant la publication des données.

Les informations relatives à la source officielle sont disponibles dans la documentation du NOAA Climate Prediction Center.

