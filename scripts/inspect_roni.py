
from pathlib import Path
import pandas as pd

# 1. Définir les chemins du projet
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "raw" / "RONI.ascii.txt"

# 2. Vérifier que le fichier existe
if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Fichier RONI introuvable : {DATA_FILE}"
    )

# 3. Lire le fichier NOAA
# sep=r"\s+" permet de séparer les colonnes
# même si elles sont espacées différemment.
df = pd.read_csv(
    DATA_FILE,
    #pandas utilise les espaces et les tabulations comme séparateurs
    sep=r"\s+",
    header=0
)

# 4. Afficher les premières lignes
print("\n--- APERÇU DES DONNÉES ---")
print(df.head(10))

# 5. Examiner la structure
print("\n--- STRUCTURE DU FICHIER ---")
df.info()


# 6. Vérifier les valeurs manquantes
print("\n--- VALEURS MANQUANTES ---")
print(df.isnull().sum())

# 7. Vérifier les doublons
print("\n--- DOUBLONS ---")
print(df.duplicated().sum())

# Vérifier les saisons disponibles
expected_seasons = [
    "DJF", "JFM", "FMA", "MAM",
    "AMJ", "MJJ", "JJA", "JAS",
    "ASO", "SON", "OND", "NDJ"
]

print("\n--- VALIDATION DES SAISONS ---")

invalid_seasons = df[~df["SEAS"].isin(expected_seasons)]

print("Saisons invalides :", len(invalid_seasons))

# Vérifier les doublons année + saison
print("\n--- DOUBLONS ANNÉE / SAISON ---")

print(
    df.duplicated(subset=["YR", "SEAS"]).sum()
)

# Vérifier les années incomplètes
print("\n--- ANNÉES INCOMPLÈTES ---")

season_counts = df.groupby("YR")["SEAS"].nunique()

print(season_counts[season_counts != 12])



# 8. Examiner les statistiques
print("\n--- STATISTIQUES ---")
print(df["ANOM"].describe())

# 9. Examiner les années disponibles
print("\n--- PÉRIODE COUVERTE ---")
print("Première année :", df["YR"].min())
print("Dernière année :", df["YR"].max())

# 10. Vérifier le nombre de lignes par année
print("\n--- NOMBRE DE SAISONS PAR ANNÉE ---")
print(df.groupby("YR").size().tail(10))

# 11. Afficher les valeurs les plus récentes
print("\n--- DERNIÈRES MESURES ---")
print(df.tail(12))

print("\nInspection terminée.")
