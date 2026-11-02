
import sys
from pathlib import Path
from datetime import date, datetime, time, timezone
from decimal import Decimal

import pandas as pd

from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import insert

# Ajouter le dossier backend au chemin Python
ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "backend"

sys.path.insert(0, str(BACKEND_DIR))

# Importer notre configuration et nos modèles existants
from app.db.session import SessionLocal
from app.db.models import (
    ClimateIndex,
    Source,
    ImportRun,
    Observation,
)


# Chemin du fichier CSV nettoyé
CSV_PATH = ROOT_DIR / "data" / "processed" / "roni_clean.csv"

# Informations sur la série NOAA
SOURCE_NAME = "NOAA CPC"

SOURCE_URL = (
    "https://www.cpc.ncep.noaa.gov/"
    "data/indices/RONI.ascii.txt"
)

INDEX_CODE = "RONI"
INDEX_NAME = "Relative Oceanic Niño Index"

# Date connue de récupération du fichier
EXTRACTION_DATE = datetime(
    2026, 10, 30, 0, 0,
    tzinfo=timezone.utc
)

# Nombre de lignes attendu
EXPECTED_ROWS = 920

# Correspondance entre les mois et les saisons RONI
SEASONS_BY_MONTH = {
    1: "DJF",
    2: "JFM",
    3: "FMA",
    4: "MAM",
    5: "AMJ",
    6: "MJJ",
    7: "JJA",
    8: "JAS",
    9: "ASO",
    10: "SON",
    11: "OND",
    12: "NDJ",
}


def load_csv():
    """
    Charge et vérifie les données nettoyées du RONI.
    """

    print("\n--- LECTURE DU CSV ---")

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Fichier introuvable : {CSV_PATH}"
        )

    df = pd.read_csv(CSV_PATH)

    required_columns = [
        "date",
        "year",
        "month",
        "season",
        "roni_value",
    ]

    # Vérifier la présence des colonnes
    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Colonnes manquantes : {missing_columns}"
        )

    # Convertir les dates
    df["date"] = pd.to_datetime(
        df["date"],
        errors="raise"
    )

    # Vérifier les valeurs manquantes
    if df[required_columns].isnull().any().any():
        raise ValueError(
            "Le CSV contient des valeurs manquantes."
        )

    # Vérifier la cohérence année/mois/date
    if not (
        (df["year"] == df["date"].dt.year)
        & (df["month"] == df["date"].dt.month)
    ).all():
        raise ValueError(
            "Incohérence entre les dates, années et mois."
        )

    # Vérifier les saisons
    expected_seasons = df["month"].map(
        SEASONS_BY_MONTH
    )

    if not (df["season"] == expected_seasons).all():
        raise ValueError(
            "Certaines saisons ne correspondent pas aux mois."
        )

    # Vérifier les doublons dans le fichier
    if df["date"].duplicated().any():
        raise ValueError(
            "Le CSV contient des dates en double."
        )

    if len(df) != EXPECTED_ROWS:
        raise ValueError(
            f"Nombre de lignes inattendu : {len(df)} "
            f"au lieu de {EXPECTED_ROWS}."
        )

    print(f"Lignes chargées : {len(df)}")
    print("Contrôles du CSV : OK")

    return df


def get_or_create_metadata(session):
    """
    Recherche ou crée l'indice RONI et la source NOAA.
    """

    # Recherche de l'indice climatique
    climate_index = session.scalar(
        select(ClimateIndex).where(
            ClimateIndex.code == INDEX_CODE
        )
    )

    if climate_index is None:
        climate_index = ClimateIndex(
            code=INDEX_CODE,
            name=INDEX_NAME,
            description=(
                "Relative Oceanic Niño Index, "
                "indice climatique utilisé pour "
                "suivre le phénomène ENSO."
            ),
            unit="°C",
        )

        session.add(climate_index)
        session.flush()

        print("Indice RONI créé.")

    # Recherche de la source NOAA
    source = session.scalar(
        select(Source).where(
            Source.name == SOURCE_NAME
        )
    )

    if source is None:
        source = Source(
            name=SOURCE_NAME,
            url=SOURCE_URL,
            description=(
                "NOAA Climate Prediction Center "
                "(CPC), source officielle des données RONI."
            ),
        )

        session.add(source)
        session.flush()

        print("Source NOAA créée.")

    return climate_index, source



def prepare_observations(
    df,
    index_id,
    source_id,
    import_run_id
):
    """
    Transforme les lignes CSV en observations SQLAlchemy.
    """

    observations = []

    for _, row in df.iterrows():

        # Date du mois central
        observation_date = row["date"]

        # Calcul du début et de la fin de la période
        period_start = (
            observation_date - pd.DateOffset(months=1)
        )

        period_end = (
            observation_date + pd.DateOffset(months=1)
        )

        observation = {
            "index_id": index_id,
            "source_id": source_id,
            "import_run_id": import_run_id,

            "period_start": period_start.date(),
            "period_end": period_end.date(),

            "observation_date": observation_date.date(),

            "year": int(row["year"]),
            "month": int(row["month"]),

            "season_label": str(row["season"]),

            "value": Decimal(str(row["roni_value"])),
        }

        observations.append(observation)

    print(
        f"Observations préparées : {len(observations)}"
    )

    return observations


def create_import_run():
    """
    Crée une nouvelle entrée dans l'historique des imports.
    """

    with SessionLocal() as session:
        with session.begin():

            climate_index, source = get_or_create_metadata(
                session
            )

            import_run = ImportRun(
                source_id=source.id,
                extracted_at=EXTRACTION_DATE,
                status="running",
                rows_imported=0,
            )

            session.add(import_run)
            session.flush()

            # Récupération des identifiants
            index_id = climate_index.id
            source_id = source.id
            import_run_id = import_run.id

    print(f"ImportRun créé : {import_run_id}")

    return index_id, source_id, import_run_id



def import_observations(df, index_id, source_id, import_run_id):
    """
    Insère les observations dans PostgreSQL.
    Ignore les observations déjà présentes.
    """

    observations = prepare_observations(
        df,
        index_id,
        source_id,
        import_run_id,
    )

    period_starts = [
        observation["period_start"]
        for observation in observations
    ]

    with SessionLocal() as session:
        with session.begin():

            # Création de la requête d'insertion PostgreSQL
            statement = (
                insert(Observation)
                .values(observations)
                .on_conflict_do_nothing(
                    index_elements=[
                        "index_id",
                        "period_start",
                    ]
                )
                .returning(Observation.id)
            )

            # Exécution de l'insertion
            inserted_ids = (
                session.execute(statement)
                .scalars()
                .all()
            )

            rows_inserted = len(inserted_ids)

            # Vérifier combien d'observations existent
            total_present = session.scalar(
                select(func.count())
                .select_from(Observation)
                .where(
                    Observation.index_id == index_id,
                    Observation.period_start.in_(
                        period_starts
                    ),
                )
            )

            if total_present != len(observations):
                raise RuntimeError(
                    "Le nombre d'observations présentes "
                    "ne correspond pas au nombre attendu."
                )

            # Mise à jour de l'historique
            import_run = session.get(
                ImportRun,
                import_run_id,
            )

            import_run.rows_imported = rows_inserted
            import_run.status = "success"
            import_run.finished_at = datetime.now(
                timezone.utc
            )

    print("\n--- IMPORTATION TERMINÉE ---")
    print(f"Lignes attendues : {len(observations)}")
    print(f"Lignes insérées : {rows_inserted}")
    print(
        f"Doublons ignorés : "
        f"{len(observations) - rows_inserted}"
    )
    print(f"Observations présentes : {total_present}")

    return rows_inserted


def mark_import_failed(import_run_id):
    """
    Enregistre l'échec d'une importation.
    """

    with SessionLocal() as session:
        with session.begin():

            import_run = session.get(
                ImportRun,
                import_run_id,
            )

            if import_run is not None:
                import_run.status = "failed"
                import_run.finished_at = datetime.now(
                    timezone.utc
                )
                import_run.rows_imported = 0



def main():
    """
    Lance l'ensemble du processus d'importation.
    """

    import_run_id = None

    try:
        print("================================")
        print(" ENSO MONITOR - IMPORTATION RONI")
        print("================================")

        # 1. Charger et contrôler les données
        df = load_csv()

        # 2. Créer l'historique d'importation
        index_id, source_id, import_run_id = (
            create_import_run()
        )

        # 3. Insérer les observations
        import_observations(
            df,
            index_id,
            source_id,
            import_run_id,
        )

        print("\nImportation réussie !")

    except Exception as error:

        print("\nERREUR DURANT L'IMPORTATION")
        print(error)

        if import_run_id is not None:
            try:
                mark_import_failed(import_run_id)
                print("Statut de l'import : failed")
            except Exception as status_error:
                print(
                    "Impossible d'enregistrer l'échec :",
                    status_error,
                )

        raise


if __name__ == "__main__":
    main()
