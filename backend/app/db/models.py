
from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from datetime import date, datetime
from decimal import Decimal


class ClimateIndex(Base):
    """Indices climatiques disponibles."""

    __tablename__ = "indices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str] = mapped_column(
        String(20), nullable=False, default="°C"
    )

    observations: Mapped[list["Observation"]] = relationship(
        back_populates="climate_index"
    )


class Source(Base):
    """Sources des données climatiques."""

    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    url: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)

    import_runs: Mapped[list["ImportRun"]] = relationship(
        back_populates="source"
    )
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="source"
    )


class ImportRun(Base):
    """Historique des imports de données."""

    __tablename__ = "import_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="RESTRICT"),
        nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True)
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        server_default=text("'running'")
    )

    rows_imported: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("0")
    )

    source: Mapped["Source"] = relationship(
        back_populates="import_runs"
    )

    observations: Mapped[list["Observation"]] = relationship(
        back_populates="import_run"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('running', 'success', 'failed')",
            name="ck_import_runs_status"
        ),
        CheckConstraint(
            "rows_imported >= 0",
            name="ck_import_runs_rows_imported"
        ),
        CheckConstraint(
            "finished_at IS NULL OR finished_at >= started_at",
            name="ck_import_runs_finished_at"
        ),
    )


class Observation(Base):
    """Observations historiques du RONI."""

    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    index_id: Mapped[int] = mapped_column(
        ForeignKey("indices.id", ondelete="RESTRICT"),
        nullable=False
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id", ondelete="RESTRICT"),
        nullable=False
    )

    import_run_id: Mapped[int] = mapped_column(
        ForeignKey("import_runs.id", ondelete="RESTRICT"),
        nullable=False
    )

    period_start: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    period_end: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    observation_date: Mapped[date] = mapped_column(
        Date, nullable=False
    )

    year: Mapped[int] = mapped_column(
        SmallInteger, nullable=False
    )

    month: Mapped[int] = mapped_column(
        SmallInteger, nullable=False
    )

    season_label: Mapped[str] = mapped_column(
        String(3), nullable=False
    )

    value: Mapped[Decimal] = mapped_column(
        Numeric(5, 2), nullable=False
    )

    climate_index: Mapped["ClimateIndex"] = relationship(
        back_populates="observations"
    )

    source: Mapped["Source"] = relationship(
        back_populates="observations"
    )

    import_run: Mapped["ImportRun"] = relationship(
        back_populates="observations"
    )

    __table_args__ = (
        UniqueConstraint(
            "index_id",
            "period_start",
            name="uq_observations_index_period_start"
        ),
        CheckConstraint(
            "period_end >= period_start",
            name="ck_observations_period_valid"
        ),
        CheckConstraint(
            "month BETWEEN 1 AND 12",
            name="ck_observations_month_valid"
        ),
        CheckConstraint(
            "season_label IN ('DJF', 'JFM', 'FMA', 'MAM', "
            "'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', "
            "'OND', 'NDJ')",
            name="ck_observations_season_valid"
        ),
        CheckConstraint(
            "year BETWEEN 1800 AND 2200",
            name="ck_observations_year_valid"
        ),
        CheckConstraint(
            "EXTRACT(YEAR FROM observation_date) = year "
            "AND EXTRACT(MONTH FROM observation_date) = month",
            name="ck_observations_date_consistent"
        ),
        Index(
            "idx_observations_period_start",
            "period_start"
        ),
    )
