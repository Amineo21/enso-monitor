
from pathlib import Path

import numpy as np
import pandas as pd


# --------------------------------------------------
# 1. Définition des chemins
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_FILE = BASE_DIR / "data" / "raw" / "RONI.ascii.txt"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

CLEAN_FILE = PROCESSED_DIR / "roni_clean.csv"
REJECTED_FILE = PROCESSED_DIR / "roni_rejected.csv"


# --------------------------------------------------
# 2. Définition des saisons et de leurs mois centraux
# --------------------------------------------------

SEASON_TO_MONTH = {
    "DJF": 1,
    "JFM": 2,
    "FMA": 3,
    "MAM": 4,
    "AMJ": 5,
    "MJJ": 6,
    "JJA": 7,
    "JAS": 8,
    "ASO": 9,
    "SON": 10,
    "OND": 11,
    "NDJ": 12,
}


# --------------------------------------------------
# 3. Vérification du fichier source
# --------------------------------------------------

if not RAW_FILE.exists():
    raise FileNotFoundError(
        f"Fichier NOAA introuvable : {RAW_FILE}"
    )

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# 4. Lecture des données brutes
# --------------------------------------------------

df = pd.read_csv(
    RAW_FILE,
    sep=r"\s+",
    dtype="string"
)

required_columns = ["SEAS", "YR", "ANOM"]

if list(df.columns) != required_columns:
    raise ValueError(
        f"Colonnes inattendues : {list(df.columns)}"
    )

print("Nombre de lignes initiales :", len(df))


# --------------------------------------------------
# 5. Nettoyage et validation
# --------------------------------------------------

df["SEAS"] = df["SEAS"].str.strip().str.upper()

df["YR"] = pd.to_numeric(
    df["YR"],
    errors="coerce"
)

df["ANOM"] = pd.to_numeric(
    df["ANOM"],
    errors="coerce"
)

reasons = pd.Series("", index=df.index, dtype="string")


def add_reason(mask, message):
    """Ajoute une raison de rejet aux lignes concernées."""
    reasons.loc[mask] = reasons.loc[mask].apply(
        lambda current: (
            f"{current} ; {message}"
            if current
            else message
        )
    )


# Saison inconnue
add_reason(
    ~df["SEAS"].isin(SEASON_TO_MONTH),
    "Saison invalide"
)

# Année manquante ou non entière
invalid_year = (
    df["YR"].isna()
    | (df["YR"] % 1 != 0)
)

add_reason(
    invalid_year,
    "Année manquante ou invalide"
)

# Valeur RONI manquante ou non numérique
invalid_value = (
    df["ANOM"].isna()
    | ~np.isfinite(df["ANOM"].fillna(0))
)

add_reason(
    invalid_value,
    "Valeur RONI manquante ou invalide"
)


# Séparation des lignes valides et rejetées
invalid_rows = reasons.ne("")

rejected = df.loc[invalid_rows].copy()
rejected["rejection_reason"] = reasons.loc[invalid_rows]

valid = df.loc[~invalid_rows].copy()


# --------------------------------------------------
# 6. Détection des données contradictoires
# --------------------------------------------------

conflicts = (
    valid.groupby(["YR", "SEAS"])["ANOM"]
    .nunique()
)

conflicts = conflicts[conflicts > 1]

if not conflicts.empty:
    raise ValueError(
        "Conflits détectés : plusieurs valeurs RONI "
        "pour une même année et saison.\n"
        f"{conflicts}"
    )


# --------------------------------------------------
# 7. Suppression des doublons exacts
# --------------------------------------------------

duplicate_mask = valid.duplicated(
    subset=["SEAS", "YR", "ANOM"],
    keep="first"
)

duplicates = valid.loc[duplicate_mask].copy()
duplicates["rejection_reason"] = "Doublon exact"

rejected = pd.concat(
    [rejected, duplicates],
    ignore_index=True
)

valid = valid.loc[~duplicate_mask].copy()


# --------------------------------------------------
# 8. Transformation des données
# --------------------------------------------------

valid["YR"] = valid["YR"].astype(int)

valid["month"] = valid["SEAS"].map(SEASON_TO_MONTH)

valid["date"] = pd.to_datetime(
    {
        "year": valid["YR"],
        "month": valid["month"],
        "day": 1
    }
)

clean = pd.DataFrame({
    "date": valid["date"].dt.strftime("%Y-%m-%d"),
    "year": valid["YR"],
    "month": valid["month"],
    "season": valid["SEAS"],
    "roni_value": valid["ANOM"]
})

clean = clean.sort_values("date").reset_index(drop=True)


# --------------------------------------------------
# 9. Export des fichiers
# --------------------------------------------------

clean.to_csv(
    CLEAN_FILE,
    index=False,
    encoding="utf-8"
)

rejected.to_csv(
    REJECTED_FILE,
    index=False,
    encoding="utf-8"
)


# --------------------------------------------------
# 10. Bilan de la transformation
# --------------------------------------------------

print("\n--- TRANSFORMATION TERMINÉE ---")

print("Lignes initiales :", len(df))
print("Lignes conservées :", len(clean))
print("Lignes rejetées :", len(rejected))

print("\nPériode couverte :")
print("Première date :", clean["date"].min())
print("Dernière date :", clean["date"].max())

print("\nFichier propre :", CLEAN_FILE)
print("Fichier des rejets :", REJECTED_FILE)

print("\nAperçu des données transformées :")
print(clean.head(12))
