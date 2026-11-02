# ENSO Monitor

## 1. Présentation

ENSO Monitor est une application web de visualisation des données historiques de l'indice climatique RONI (*Relative Oceanic Niño Index*).

L'objectif est de permettre à l'utilisateur de sélectionner une année, de visualiser les 12 valeurs mensuelles associées et de comparer deux années.

L'application s'appuie sur les données historiques officielles de la NOAA, traitées avec Python et Pandas, puis stockées dans une base de données PostgreSQL.

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
- **ORM :** SQLAlchemy.
- **Migrations :** Alembic.
- **Connexion PostgreSQL :** Psycopg.
- **Configuration :** python-dotenv.
- **Versionnement :** Git.

## 4. Architecture

La source NOAA constitue la source de référence des données.

Un processus ETL (*Extract, Transform, Load*) Python est chargé de récupérer, inspecter, valider, transformer et importer les données dans PostgreSQL.

La base PostgreSQL assure le stockage des observations climatiques ainsi que la traçabilité des sources et des opérations d'importation.

SQLAlchemy assure la communication entre Python et PostgreSQL. Alembic permet de gérer les évolutions du schéma relationnel à travers des migrations versionnées.

L'API FastAPI expose les données au frontend React sous forme de réponses JSON.

Le frontend ne communique pas directement avec PostgreSQL.

### Flux général des données

1. Récupération des données depuis la source NOAA.
2. Inspection et validation des données brutes.
3. Nettoyage et transformation des observations.
4. Importation des données validées dans PostgreSQL.
5. Exposition des données par l'API FastAPI.
6. Affichage et visualisation dans l'interface React.

### Technologies et responsabilités

| Composant | Responsabilité |
|---|---|
| NOAA | Fourniture des données climatiques |
| Python / Pandas | Extraction et transformation ETL |
| PostgreSQL | Stockage relationnel |
| SQLAlchemy | Mapping objet-relationnel et accès aux données |
| Alembic | Gestion des migrations |
| FastAPI | Exposition des données par API |
| React / TypeScript | Interface utilisateur et visualisation |

## 5. Structure du projet

```text
enso-monitor/
│
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── alembic.ini
│   │
│   └── app/
│       ├── __init__.py
│       └── db/
│           ├── __init__.py
│           ├── base.py
│           ├── models.py
│           └── session.py
│
├── data/
│   ├── raw/
│   │   └── RONI.ascii.txt
│   │
│   └── processed/
│       ├── roni_clean.csv
│       └── roni_rejected.csv
│
├── database/
│
├── docs/
│   └── data-model.md
│
├── etl/
│
├── frontend/
│
├── scripts/
│   ├── inspect_roni.py
│   ├── transform_roni.py
│   └── import_to_postgres.py
│
├── tests/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Organisation des principaux fichiers

| Fichier / Dossier | Description |
|---|---|
| `backend/app/db/base.py` | Déclaration de la classe de base SQLAlchemy |
| `backend/app/db/models.py` | Définition des modèles relationnels |
| `backend/app/db/session.py` | Configuration de la connexion PostgreSQL et des sessions |
| `backend/alembic/` | Configuration et historique des migrations |
| `backend/alembic/versions/` | Fichiers de migrations versionnés |
| `backend/alembic.ini` | Configuration générale d'Alembic |
| `data/raw/` | Données originales NOAA |
| `data/processed/` | Données nettoyées et transformées |
| `docs/` | Documentation technique du projet |
| `scripts/` | Scripts d'inspection, de transformation et d'importation PostgreSQL |
| `scripts/import_to_postgres.py` | Validation du CSV, gestion des métadonnées et importation transactionnelle des observations dans PostgreSQL |
| `frontend/` | Interface React et TypeScript |
| `tests/` | Tests automatisés |
| `.env` | Variables d'environnement locales |
| `.env.example` | Exemple de configuration des variables d'environnement |
| `requirements.txt` | Dépendances Python |

## 6. Installation et configuration

### 6.1 Prérequis

- Python 3.
- Node.js et npm.
- PostgreSQL.
- pgAdmin 4 (recommandé pour administrer la base).
- Git.

### 6.2 Backend et ETL

À la racine du projet, créer et activer l'environnement virtuel :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

Les principales dépendances Python sont :

- `pandas`
- `numpy`
- `sqlalchemy`
- `alembic`
- `psycopg`
- `python-dotenv`
- `fastapi`

La liste complète des dépendances et leurs versions est conservée dans `requirements.txt`.

### 6.3 Configuration de l'environnement

La connexion à PostgreSQL est configurée dans le fichier `.env`, situé à la racine du projet.

Exemple :

```env
DATABASE_URL=postgresql+psycopg://postgres:CHANGE_ME@localhost:5432/enso_monitor
```

Le fichier `.env.example` fournit un modèle de configuration sans informations confidentielles.

Le fichier `.env` ne doit jamais être versionné sur Git.

### 6.4 Frontend

Depuis le dossier frontend :

```powershell
cd frontend
npm install
npm run dev
```

### 6.5 Base de données PostgreSQL

La base de données utilisée par ENSO Monitor est nommée :

```text
enso_monitor
```

Elle est hébergée localement sur PostgreSQL, avec le port par défaut `5432`.

Le schéma relationnel est défini à travers les modèles SQLAlchemy dans :

```text
backend/app/db/models.py
```

La création et l'évolution des tables sont gérées par Alembic.

Les migrations sont stockées dans :

```text
backend/alembic/versions/
```

La première migration permet de créer le schéma relationnel initial.

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

```text
data/raw/RONI.ascii.txt
```

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

Pour préserver la précision temporelle des observations dans PostgreSQL, les champs `period_start` et `period_end` sont intégrés au modèle de données. Ils permettent de représenter les dates réelles de début et de fin de chaque période glissante de trois mois.

### 7.7 Stockage et traçabilité

Les dates des observations sont stockées en base au format SQL `DATE`.

Les horodatages techniques utilisent `TIMESTAMPTZ`.

La base de données doit permettre de conserver :

- La valeur RONI.
- La saison et la période correspondantes.
- La source NOAA.
- La date d'extraction de la source (`extracted_at`).
- La date de début et de fin de l'importation.
- Le statut de l'importation et le nombre de lignes réellement insérées.
- La traçabilité des opérations de traitement.

La date d'extraction actuellement enregistrée est le 30/10/2026. Seul le jour de récupération étant connu, l'heure technique associée est fixée à 00:00 UTC ; elle ne représente pas une heure de téléchargement constatée.

La provenance, la version de la source et les imports doivent être documentés afin de faciliter la vérification et la reproductibilité des données.

### 7.8 Importation des données dans PostgreSQL

Le script `scripts/import_to_postgres.py` charge les observations validées du fichier `data/processed/roni_clean.csv` dans la base PostgreSQL `enso_monitor`.

#### Responsabilités du script

- Lecture du CSV avec Pandas.
- Vérification des colonnes attendues et des 920 lignes.
- Contrôle des valeurs manquantes, des dates, des saisons et des doublons.
- Recherche ou création de l'indice climatique RONI.
- Recherche ou création de la source NOAA CPC.
- Création d'un enregistrement dans `import_runs` pour chaque exécution.
- Préparation des observations avec leurs dates de période, leur mois central et leur valeur RONI.
- Insertion des observations avec SQLAlchemy et le mécanisme PostgreSQL `ON CONFLICT DO NOTHING`.
- Mise à jour du statut et du nombre de lignes réellement insérées.

#### Traçabilité des importations

Chaque exécution crée un nouvel enregistrement dans `import_runs`.

Les informations conservées comprennent notamment :

- La source NOAA associée.
- La date d'extraction (`extracted_at`).
- La date de début (`started_at`).
- La date de fin (`finished_at`).
- Le statut (`running`, `success` ou `failed`).
- Le nombre de lignes réellement insérées (`rows_imported`).

La date d'extraction de la série importée est le 30/10/2026. L'heure 00:00 UTC utilisée dans le champ technique est une convention, car seule la date de récupération est connue.

#### Transactions et prévention des doublons

La création des métadonnées et de l'enregistrement d'importation est effectuée dans une première transaction. L'insertion des observations et la mise à jour du bilan sont effectuées dans une seconde transaction.

La contrainte d'unicité sur `(index_id, period_start)` permet d'ignorer les observations déjà présentes avec `ON CONFLICT DO NOTHING`.

Le nombre de lignes insérées est calculé à partir des identifiants retournés par PostgreSQL. Un contrôle complémentaire vérifie que les 920 périodes attendues sont présentes dans la base.

En cas d'échec pendant la transaction d'insertion, celle-ci est annulée et le statut de l'importation est enregistré comme `failed` dans une nouvelle transaction.

#### Exécution

Depuis la racine du projet, avec l'environnement virtuel activé :

```powershell
python scripts/import_to_postgres.py
```

#### Résultats des premiers tests

Deux exécutions successives ont été réalisées le 02/11/2026 :

| Indicateur | Première exécution | Deuxième exécution |
|---|---:|---:|
| Lignes lues | 920 | 920 |
| Lignes préparées | 920 | 920 |
| Lignes insérées | 920 | 0 |
| Doublons ignorés | 0 | 920 |
| Observations présentes | 920 | 920 |
| Résultat | success | success |

La première exécution a inséré les 920 observations. La deuxième n'a créé aucune nouvelle observation : les 920 enregistrements existants ont été ignorés.

Ces résultats valident le fonctionnement de l'importation et son idempotence sur le jeu de données testé.

---

## 8. Modèle relationnel PostgreSQL

### 8.1 Présentation

Le modèle relationnel de la base `enso_monitor` repose sur quatre tables principales :

- `indices`
- `sources`
- `import_runs`
- `observations`

La table `observations` constitue le cœur du stockage des données climatiques.

Les autres tables permettent de structurer les indices disponibles, les sources de données et l'historique des imports.

### 8.2 Description des tables

#### Table `indices`

Répertorie les indices climatiques disponibles dans l'application.

| Colonne | Type PostgreSQL | Contraintes |
|---|---|---|
| `id` | INTEGER | PK |
| `code` | VARCHAR(20) | UNIQUE, NOT NULL |
| `name` | VARCHAR(100) | NOT NULL |
| `description` | TEXT | NULL autorisé |
| `unit` | VARCHAR(20) | NOT NULL |

L'indice RONI est enregistré dans cette table.

#### Table `sources`

Conserve les informations relatives à la provenance des données.

| Colonne | Type PostgreSQL | Contraintes |
|---|---|---|
| `id` | INTEGER | PK |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL |
| `url` | TEXT | NULL autorisé |
| `description` | TEXT | NULL autorisé |

La NOAA constitue la première source enregistrée.

#### Table `import_runs`

Conserve l'historique des opérations d'importation.

| Colonne | Type PostgreSQL | Contraintes |
|---|---|---|
| `id` | INTEGER | PK |
| `source_id` | INTEGER | FK vers `sources.id`, NOT NULL |
| `extracted_at` | TIMESTAMPTZ | NULL autorisé |
| `started_at` | TIMESTAMPTZ | NOT NULL, valeur par défaut : NOW() |
| `finished_at` | TIMESTAMPTZ | NULL autorisé |
| `status` | VARCHAR(20) | NOT NULL, valeur par défaut : running |
| `rows_imported` | INTEGER | NOT NULL, valeur par défaut : 0 |

Les statuts autorisés sont :

- `running`
- `success`
- `failed`

Les contraintes vérifient également que le nombre de lignes importées est positif ou nul et que la date de fin ne précède pas la date de début.

#### Table `observations`

Stocke les observations historiques de l'indice RONI.

| Colonne | Type PostgreSQL | Contraintes |
|---|---|---|
| `id` | INTEGER | PK |
| `index_id` | INTEGER | FK vers `indices.id`, NOT NULL |
| `source_id` | INTEGER | FK vers `sources.id`, NOT NULL |
| `import_run_id` | INTEGER | FK vers `import_runs.id`, NOT NULL |
| `period_start` | DATE | NOT NULL |
| `period_end` | DATE | NOT NULL |
| `observation_date` | DATE | NOT NULL |
| `year` | SMALLINT | NOT NULL |
| `month` | SMALLINT | NOT NULL |
| `season_label` | VARCHAR(3) | NOT NULL |
| `value` | NUMERIC(5,2) | NOT NULL |

`observation_date` représente le premier jour du mois central de la saison NOAA.

`period_start` et `period_end` permettent de conserver les bornes de la moyenne glissante sur trois mois.

### 8.3 Relations entre les tables

Le modèle relationnel repose sur les relations suivantes :

- Un indice peut posséder plusieurs observations.
- Une source peut être associée à plusieurs imports.
- Une source peut être associée à plusieurs observations.
- Un import peut contenir plusieurs observations.

Schéma relationnel simplifié :

```mermaid
erDiagram
    INDICES ||--o{ OBSERVATIONS : contient
    SOURCES ||--o{ IMPORT_RUNS : alimente
    SOURCES ||--o{ OBSERVATIONS : fournit
    IMPORT_RUNS ||--o{ OBSERVATIONS : importe
```

### 8.4 Contraintes d'intégrité

Les contraintes suivantes assurent la cohérence des données :

- Clés primaires sur les quatre tables.
- Clés étrangères pour garantir les relations.
- Unicité du code des indices.
- Unicité du nom des sources.
- Unicité d'une observation par indice et date de début de période.
- Vérification de la validité des périodes.
- Vérification du mois entre 1 et 12.
- Vérification des libellés de saisons NOAA.
- Vérification de la cohérence entre `observation_date`, `year` et `month`.
- Vérification du statut des imports.
- Vérification du nombre de lignes importées.
- Protection contre la suppression des éléments encore référencés grâce à `ON DELETE RESTRICT`.

### 8.5 Indexation temporelle

Un index B-tree est créé sur la colonne :

```text
observations.period_start
```

Nom de l'index :

```text
idx_observations_period_start
```

Cet index permet d'améliorer les performances des recherches temporelles, notamment pour récupérer les observations comprises dans une période donnée.

Une contrainte UNIQUE sur `(index_id, period_start)` crée également un index permettant de prévenir les doublons pour un même indice et une même période.

### 8.6 Choix des types de données

| Type | Utilisation | Justification |
|---|---|---|
| INTEGER | Identifiants et compteurs | Nombres entiers |
| SMALLINT | Année et mois | Valeurs numériques limitées |
| VARCHAR | Codes et libellés | Textes de longueur définie |
| TEXT | Descriptions et URL | Textes de longueur variable |
| DATE | Dates climatiques | Conservation des dates sans fuseau horaire |
| TIMESTAMPTZ | Horodatages techniques | Conservation des informations temporelles avec fuseau |
| NUMERIC(5,2) | Valeurs RONI | Précision décimale à deux chiffres après la virgule |

## 9. SQLAlchemy et Alembic

### 9.1 SQLAlchemy

SQLAlchemy assure la communication entre le code Python et PostgreSQL.

Les modèles relationnels sont définis dans :

```text
backend/app/db/models.py
```

La classe `Base` est définie dans :

```text
backend/app/db/base.py
```

Elle constitue la classe de base des modèles SQLAlchemy.

La connexion à PostgreSQL et la gestion des sessions sont configurées dans :

```text
backend/app/db/session.py
```

La connexion utilise la variable d'environnement `DATABASE_URL`.

Le pilote Psycopg assure la communication avec PostgreSQL.

### 9.2 Alembic

Alembic est utilisé pour gérer les migrations de la base de données.

La configuration se trouve dans :

```text
backend/alembic.ini
```

L'environnement de migration est configuré dans :

```text
backend/alembic/env.py
```

Les fichiers de migrations sont conservés dans :

```text
backend/alembic/versions/
```

### 9.3 Commandes de migration

Depuis le dossier `backend/` :

**Générer une nouvelle migration :**

```powershell
alembic revision --autogenerate -m "description de la modification"
```

**Appliquer les migrations :**

```powershell
alembic upgrade head
```

**Afficher la version actuellement appliquée :**

```powershell
alembic current
```

**Consulter l'historique des migrations :**

```powershell
alembic history
```

**Vérifier la cohérence entre les modèles et la base :**

```powershell
alembic check
```

Les migrations doivent être vérifiées avant leur application et conservées dans Git afin de garantir la reproductibilité de la structure de la base.

## 10. Tests

Les tests automatisés couvriront progressivement :

- Le traitement et la validation des données NOAA.
- La détection des valeurs invalides et des dates incorrectes.
- La prévention des doublons lors des imports.
- La gestion des données contradictoires.
- L'intégrité des relations PostgreSQL.
- Le fonctionnement des migrations.
- Les endpoints de l'API et leurs erreurs.
- Les données retournées au frontend.

Les tests de l'ETL devront notamment vérifier le comportement du traitement face aux doublons et aux observations invalides.

## 11. Statut du projet

Projet en cours de développement dans le cadre d'un projet de rattrapage HETIC.

**État d'avancement au 02/11/2026 :**

### Données et ETL

- [x] Récupération du fichier NOAA RONI.
- [x] Inspection de la structure des données.
- [x] Vérification des valeurs manquantes et des doublons.
- [x] Création du script de transformation ETL.
- [x] Génération du fichier CSV nettoyé.
- [x] Génération du fichier des rejets.
- [x] Association des saisons à leurs mois centraux.
- [x] Préparation des observations pour leur stockage PostgreSQL.
- [x] Validation du fichier CSV avant importation.

### Base de données

- [x] Installation et configuration de PostgreSQL.
- [x] Création de la base `enso_monitor`.
- [x] Définition du modèle relationnel.
- [x] Création des modèles SQLAlchemy.
- [x] Définition des clés primaires et étrangères.
- [x] Mise en place des contraintes UNIQUE et CHECK.
- [x] Création de l'index temporel.
- [x] Configuration de la connexion SQLAlchemy.
- [x] Initialisation d'Alembic.
- [x] Génération et application de la première migration.
- [x] Vérification de la structure de la base.
- [x] Ajout des premières données de référence : RONI et NOAA.
- [x] Documentation du modèle de données.
- [x] Ajout du champ `extracted_at` à la table `import_runs` via une migration Alembic.
- [x] Développement du script `scripts/import_to_postgres.py`.
- [x] Enregistrement des métadonnées de provenance et des tentatives d'importation.
- [x] Importation des 920 observations historiques dans PostgreSQL.
- [x] Mise en place des transactions pour sécuriser l'importation.
- [x] Prévention des doublons avec `ON CONFLICT DO NOTHING`.
- [x] Vérification de l'idempotence sur deux exécutions successives.
- [x] Vérification du nombre d'observations insérées et présentes.

### Développements restants
- [ ] Mise en place des tests automatisés de l'ETL et de la base.
- [ ] Connexion de l'API FastAPI à PostgreSQL.
- [ ] Développement des endpoints de consultation des données.
- [ ] Développement de la sélection annuelle.
- [ ] Développement de la comparaison entre deux années.
- [ ] Intégration des données dans le frontend React.
- [ ] Mise en place des tests de l'API et du frontend.

## 12. Licence et attribution

Les données climatiques utilisées par ENSO Monitor proviennent du NOAA Climate Prediction Center.

La source, la version du jeu de données, les conditions d'utilisation applicables et les éventuelles obligations d'attribution seront précisées avant la publication des données.

Les informations relatives à la source officielle sont disponibles dans la documentation du NOAA Climate Prediction Center.

---

*Projet ENSO Monitor — HETIC — Novembre 2026.*