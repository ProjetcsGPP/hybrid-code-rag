-- =========================================================
-- CODE-RAG
-- TEMPORARY MIGRATION SCHEMAS
--
-- PURPOSE:
-- Compatibility-first SQLite → PostgreSQL migration
--
-- IMPORTANT:
-- These schemas are TEMPORARY.
-- They intentionally preserve current SQLite contracts.
--
-- DO NOT normalize yet.
-- DO NOT consolidate semantics yet.
-- DO NOT rename fields yet.
--
-- Future phases:
-- - storage abstraction
-- - semantic consolidation
-- - canonical graph unification
-- =========================================================


-- #########################################################
-- SCHEMA: migration_legacy
-- #########################################################

CREATE SCHEMA IF NOT EXISTS migration_legacy;


-- =========================================================
-- TABLE: symbols
-- Mirrors legacy SQLiteStructuralStore
-- =========================================================

CREATE TABLE IF NOT EXISTS migration_legacy.symbols (

    symbol_id              TEXT PRIMARY KEY,

    symbol_path            TEXT,
    canonical_name         TEXT,

    name                   TEXT,
    symbol_type            TEXT,
    semantic_type          TEXT,

    module_name            TEXT,
    file_path              TEXT,

    parent_symbol_id       TEXT,

    start_line             INTEGER,
    end_line               INTEGER,

    calls                  JSONB,
    imports                JSONB,

    metadata               JSONB DEFAULT '{}'::jsonb,

    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_migration_legacy_symbols_name
ON migration_legacy.symbols(name);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_symbols_type
ON migration_legacy.symbols(symbol_type);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_symbols_semantic
ON migration_legacy.symbols(semantic_type);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_symbols_module
ON migration_legacy.symbols(module_name);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_symbols_parent
ON migration_legacy.symbols(parent_symbol_id);



-- =========================================================
-- TABLE: relationships
-- Mirrors legacy relationship persistence
-- =========================================================

CREATE TABLE IF NOT EXISTS migration_legacy.relationships (

    relationship_id        TEXT PRIMARY KEY,

    source_symbol_id       TEXT,
    target_symbol_id       TEXT,

    relationship_type      TEXT,

    dispatch_type          TEXT,
    edge_layer             TEXT,
    provenance_type        TEXT,

    confidence             DOUBLE PRECISION,

    file_path              TEXT,
    line_number            INTEGER,

    metadata               JSONB DEFAULT '{}'::jsonb,

    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_migration_legacy_rel_source
ON migration_legacy.relationships(source_symbol_id);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_rel_target
ON migration_legacy.relationships(target_symbol_id);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_rel_type
ON migration_legacy.relationships(relationship_type);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_rel_dispatch
ON migration_legacy.relationships(dispatch_type);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_rel_layer
ON migration_legacy.relationships(edge_layer);



-- =========================================================
-- TABLE: semantic_references
-- Optional compatibility table
-- Create now to future-proof migration
-- =========================================================

CREATE TABLE IF NOT EXISTS migration_legacy.semantic_references (

    reference_id           TEXT PRIMARY KEY,

    owner_symbol_id        TEXT,

    referenced_name        TEXT,
    resolved_target_id     TEXT,

    semantic_type          TEXT,
    framework_hint         TEXT,

    confidence             DOUBLE PRECISION,

    provenance_type        TEXT,

    metadata               JSONB DEFAULT '{}'::jsonb,

    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_migration_legacy_semref_owner
ON migration_legacy.semantic_references(owner_symbol_id);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_semref_target
ON migration_legacy.semantic_references(resolved_target_id);

CREATE INDEX IF NOT EXISTS idx_migration_legacy_semref_type
ON migration_legacy.semantic_references(semantic_type);



-- #########################################################
-- SCHEMA: migration_v2
-- #########################################################

CREATE SCHEMA IF NOT EXISTS migration_v2;


-- =========================================================
-- TABLE: nodes
-- Mirrors GraphRepositoryV2.nodes
-- =========================================================

CREATE TABLE IF NOT EXISTS migration_v2.nodes (

    id                     TEXT PRIMARY KEY,

    type                   TEXT,
    name                   TEXT,

    canonical              TEXT,

    metadata               JSONB DEFAULT '{}'::jsonb,

    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_migration_v2_nodes_type
ON migration_v2.nodes(type);

CREATE INDEX IF NOT EXISTS idx_migration_v2_nodes_name
ON migration_v2.nodes(name);

CREATE INDEX IF NOT EXISTS idx_migration_v2_nodes_canonical
ON migration_v2.nodes(canonical);



-- =========================================================
-- TABLE: edges
-- Mirrors GraphRepositoryV2.edges
-- =========================================================

CREATE TABLE IF NOT EXISTS migration_v2.edges (

    id                     TEXT PRIMARY KEY,

    source                 TEXT,
    target                 TEXT,

    type                   TEXT,

    layer                  TEXT,
    status                 TEXT,

    confidence             DOUBLE PRECISION,

    metadata               JSONB DEFAULT '{}'::jsonb,

    created_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at             TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_migration_v2_edges_source
ON migration_v2.edges(source);

CREATE INDEX IF NOT EXISTS idx_migration_v2_edges_target
ON migration_v2.edges(target);

CREATE INDEX IF NOT EXISTS idx_migration_v2_edges_type
ON migration_v2.edges(type);

CREATE INDEX IF NOT EXISTS idx_migration_v2_edges_layer
ON migration_v2.edges(layer);

CREATE INDEX IF NOT EXISTS idx_migration_v2_edges_status
ON migration_v2.edges(status);



-- #########################################################
-- OPTIONAL FUTURE TRACKING TABLES
-- (SAFE TO CREATE NOW)
-- #########################################################

CREATE TABLE IF NOT EXISTS migration_legacy.migration_metadata (

    migration_id           BIGSERIAL PRIMARY KEY,

    source_engine          TEXT,
    source_path            TEXT,

    started_at             TIMESTAMP,
    finished_at            TIMESTAMP,

    status                 TEXT,

    migrated_symbols       INTEGER DEFAULT 0,
    migrated_relationships INTEGER DEFAULT 0,

    notes                  TEXT
);


CREATE TABLE IF NOT EXISTS migration_v2.migration_metadata (

    migration_id           BIGSERIAL PRIMARY KEY,

    source_engine          TEXT,
    source_path            TEXT,

    started_at             TIMESTAMP,
    finished_at            TIMESTAMP,

    status                 TEXT,

    migrated_nodes         INTEGER DEFAULT 0,
    migrated_edges         INTEGER DEFAULT 0,

    notes                  TEXT
);