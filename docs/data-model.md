
# Modèle de données — ENSO Monitor

## 1. Présentation

ENSO Monitor utilise PostgreSQL pour stocker les
observations historiques de l'indice RONI
(Relative Oceanic Niño Index).

Le modèle relationnel repose sur quatre tables :

- `indices`
- `sources`
- `import_runs`
- `observations`

## 2. Description des tables

### indices

Répertorie les indices climatiques disponibles.

- `id` : identifiant primaire.
- `code` : code unique de l'indice.
- `name` : nom complet.
- `description` : description.
- `unit` : unité de mesure.

### sources

Conserve la provenance des données.

- `id` : identifiant primaire.
- `name` : nom de la source.
- `url` : adresse de la source.
- `description` : informations complémentaires.

### import_runs

Conserve l'historique des imports.

- `id` : identifiant primaire.
- `source_id` : référence à la source.
- `started_at` : date de début.
- `finished_at` : date de fin.
- `status` : statut de l'import.
- `rows_imported` : nombre de lignes importées.

### observations

Stocke les observations climatiques.

- `id` : identifiant primaire.
- `index_id` : référence à l'indice.
- `source_id` : référence à la source.
- `import_run_id` : référence à l'import.
- `period_start` : début de la période climatique.
- `period_end` : fin de la période climatique.
- `observation_date` : date du mois central.
- `year` : année du mois central.
- `month` : mois central.
- `season_label` : saison NOAA sur trois mois.
- `value` : anomalie climatique en °C.

## 3. Relations

- Un indice possède plusieurs observations.
- Une source peut être associée à plusieurs imports.
- Une source peut être associée à plusieurs observations.
- Un import peut contenir plusieurs observations.

## 4. Contraintes d'intégrité

- Clés primaires sur les quatre tables.
- Clés étrangères pour assurer les relations.
- Unicité du code des indices.
- Unicité du nom des sources.
- Unicité de l'observation par indice et période.
- Vérification des périodes et des mois.
- Vérification des saisons NOAA.
- Vérification du statut des imports.
- Vérification de la cohérence entre date, année et mois.

## 5. Indexation

Un index B-tree est créé sur `observations.period_start`
pour accélérer les recherches temporelles.

Une contrainte UNIQUE sur `(index_id, period_start)`
garantit également l'absence de doublons.

## 6. Choix techniques

- PostgreSQL : système de gestion relationnelle.
- SQLAlchemy : ORM Python.
- Alembic : gestion des migrations.
- DATE : dates climatiques.
- TIMESTAMPTZ : dates techniques.
- NUMERIC(5,2) : précision des valeurs RONI.

Les migrations Alembic constituent la référence
pour faire évoluer le schéma de la base.
