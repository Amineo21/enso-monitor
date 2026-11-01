
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Chemin vers la racine du projet
ROOT_DIR = Path(__file__).resolve().parents[3]

# Chargement des variables d'environnement
load_dotenv(ROOT_DIR / ".env")

# Récupération de l'URL PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL est absente du fichier .env")


# Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# Fabrique de sessions SQLAlchemy
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():
    """
    Fournit une session de base de données.
    Sera utilisée ultérieurement par FastAPI.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
