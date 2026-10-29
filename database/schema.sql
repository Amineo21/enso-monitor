
CREATE TABLE indices (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE sources (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    url TEXT NOT NULL,
    dataset_version VARCHAR(100),
    license_notes TEXT
);

CREATE TABLE import_runs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source_id BIGINT NOT NULL REFERENCES sources(id),
    imported_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL
        CHECK (status IN ('running', 'success', 'partial', 'failed')),
    file_checksum VARCHAR(128),
    rows_read INTEGER NOT NULL DEFAULT 0,
    rows_inserted INTEGER NOT NULL DEFAULT 0,
    rows_updated INTEGER NOT NULL DEFAULT 0,
    error_message TEXT
);

CREATE TABLE observations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    index_id BIGINT NOT NULL REFERENCES indices(id),
    import_run_id BIGINT NOT NULL REFERENCES import_runs(id),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    season_label VARCHAR(10) NOT NULL,
    value DOUBLE PRECISION,
    CONSTRAINT valid_period CHECK (period_end >= period_start),
    CONSTRAINT unique_index_period UNIQUE (index_id, period_start)
);

CREATE INDEX idx_observations_period
    ON observations(period_start);
