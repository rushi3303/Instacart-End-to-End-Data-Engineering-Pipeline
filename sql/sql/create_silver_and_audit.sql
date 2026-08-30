BEGIN;

CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS audit;

CREATE TABLE IF NOT EXISTS audit.audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    layer_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    status TEXT NOT NULL,
    rows_processed BIGINT NOT NULL DEFAULT 0,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    execution_time_seconds NUMERIC(12,2),
    error_message TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMIT;