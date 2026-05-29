-- =========================================================
-- CODE-RAG V2
-- Semantic Graph Database V2
-- PostgreSQL DDL
-- =========================================================

-- =========================================================
-- EXTENSIONS
-- =========================================================

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================================================
-- SCHEMAS
-- =========================================================

CREATE SCHEMA IF NOT EXISTS graph_meta;
CREATE SCHEMA IF NOT EXISTS graph_v1;
CREATE SCHEMA IF NOT EXISTS graph_runtime;

-- =========================================================
-- =========================================================
-- GRAPH META
-- =========================================================
-- =========================================================

-- =========================================================
-- WORKSPACES
-- =========================================================

CREATE TABLE graph_meta.workspaces (
    workspace_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,

    description TEXT,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- =========================================================
-- PROJECTS
-- =========================================================

CREATE TABLE graph_meta.projects (
    project_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    workspace_id UUID NOT NULL,

    name TEXT NOT NULL,
    slug TEXT NOT NULL,

    description TEXT,

    status TEXT DEFAULT 'ACTIVE',

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_projects_workspace
        FOREIGN KEY (workspace_id)
        REFERENCES graph_meta.workspaces(workspace_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_project_workspace_slug
        UNIQUE (workspace_id, slug)
);

-- =========================================================
-- REPOSITORIES
-- =========================================================

CREATE TABLE graph_meta.repositories (
    repository_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    project_id UUID NOT NULL,

    name TEXT NOT NULL,

    repository_type TEXT,
    -- git | local | monorepo | mirror

    remote_url TEXT,
    local_path TEXT,

    default_branch TEXT,

    status TEXT DEFAULT 'ACTIVE',

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_repository_project
        FOREIGN KEY (project_id)
        REFERENCES graph_meta.projects(project_id)
        ON DELETE CASCADE
);

-- =========================================================
-- SNAPSHOTS
-- =========================================================

CREATE TABLE graph_meta.snapshots (
    snapshot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    workspace_id UUID NOT NULL,
    project_id UUID NOT NULL,
    repository_id UUID NOT NULL,

    snapshot_name TEXT,

    branch_name TEXT,
    commit_hash TEXT,

    snapshot_type TEXT DEFAULT 'MANUAL',
    -- MANUAL | BRANCH | COMMIT | RELEASE | TAG | RUNTIME

    semantic_version TEXT,

    language_profile JSONB DEFAULT '{}'::jsonb,
    framework_profile JSONB DEFAULT '{}'::jsonb,

    stats JSONB DEFAULT '{}'::jsonb,

    status TEXT DEFAULT 'ACTIVE',

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_snapshot_workspace
        FOREIGN KEY (workspace_id)
        REFERENCES graph_meta.workspaces(workspace_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_snapshot_project
        FOREIGN KEY (project_id)
        REFERENCES graph_meta.projects(project_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_snapshot_repository
        FOREIGN KEY (repository_id)
        REFERENCES graph_meta.repositories(repository_id)
        ON DELETE CASCADE
);

-- =========================================================
-- SEMANTIC CONTEXTS
-- =========================================================

CREATE TABLE graph_meta.semantic_contexts (
    context_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    language TEXT,
    language_family TEXT,
    language_variant TEXT,

    framework TEXT,
    framework_version TEXT,

    detector_engine TEXT,

    detector_confidence FLOAT DEFAULT 0.0,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_semantic_context_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE
);

-- =========================================================
-- LANGUAGE PROFILES
-- =========================================================

CREATE TABLE graph_meta.language_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    language TEXT NOT NULL,
    variant TEXT,

    confidence FLOAT DEFAULT 0.0,

    files_count INTEGER DEFAULT 0,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_language_profile_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE
);

-- =========================================================
-- FRAMEWORK PROFILES
-- =========================================================

CREATE TABLE graph_meta.framework_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    framework TEXT NOT NULL,

    confidence FLOAT DEFAULT 0.0,

    files_count INTEGER DEFAULT 0,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_framework_profile_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE
);

-- =========================================================
-- PIPELINE RUNS
-- =========================================================

CREATE TABLE graph_meta.pipeline_runs (
    pipeline_run_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID,

    mode TEXT NOT NULL,
    -- legacy | v2 | bridge

    status TEXT NOT NULL,
    -- running | success | failed

    symbols_count INTEGER DEFAULT 0,
    relationships_count INTEGER DEFAULT 0,

    drift_count INTEGER DEFAULT 0,

    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    finished_at TIMESTAMP,

    metadata JSONB DEFAULT '{}'::jsonb,

    CONSTRAINT fk_pipeline_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE SET NULL
);

-- =========================================================
-- =========================================================
-- GRAPH V1
-- =========================================================
-- =========================================================

-- =========================================================
-- SYMBOLS
-- =========================================================

CREATE TABLE graph_v1.symbols (
    symbol_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    name TEXT NOT NULL,

    canonical_name TEXT NOT NULL,
    fully_qualified_name TEXT,

    symbol_path TEXT NOT NULL,

    symbol_type TEXT NOT NULL,
    -- class | function | method | interface | enum | module

    semantic_type TEXT,
    -- service | repository | model | controller | dto | entity

    visibility TEXT,
    -- public | private | protected | internal

    module_name TEXT,
    file_path TEXT NOT NULL,

    parent_symbol_id UUID,

    start_line INTEGER,
    end_line INTEGER,

    language TEXT,
    framework TEXT,

    status TEXT DEFAULT 'ACTIVE',
    -- ACTIVE | DEPRECATED | ORPHAN | UNRESOLVED

    confidence FLOAT DEFAULT 1.0,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_symbol_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_symbol_parent
        FOREIGN KEY (parent_symbol_id)
        REFERENCES graph_v1.symbols(symbol_id)
        ON DELETE SET NULL
);

-- =========================================================
-- RELATIONSHIPS
-- =========================================================

CREATE TABLE graph_v1.relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    source_symbol_id UUID NOT NULL,

    target_symbol_id UUID,

    raw_call TEXT,

    unresolved_target TEXT,

    relationship_type TEXT NOT NULL,
    -- CALLS | IMPORTS | INHERITS | IMPLEMENTS | REFERENCES

    semantic_layer TEXT NOT NULL,
    -- STRUCTURAL | SEMANTIC | RUNTIME

    dispatch_type TEXT,
    -- DIRECT | SELF | SUPER | DYNAMIC

    provenance TEXT,
    -- AST | IMPORT_RESOLUTION | RUNTIME | AI_INFERENCE

    resolver_stage TEXT,
    -- AST_PASS | SEMANTIC_PASS | RUNTIME_PASS

    framework_hint TEXT,

    status TEXT DEFAULT 'ACTIVE',

    confidence FLOAT DEFAULT 0.0,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_relationship_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_relationship_source
        FOREIGN KEY (source_symbol_id)
        REFERENCES graph_v1.symbols(symbol_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_relationship_target
        FOREIGN KEY (target_symbol_id)
        REFERENCES graph_v1.symbols(symbol_id)
        ON DELETE SET NULL
);

-- =========================================================
-- INHERITANCE EDGES
-- =========================================================

CREATE TABLE graph_v1.inheritance_edges (
    inheritance_edge_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    child_symbol_id UUID NOT NULL,

    base_symbol_name TEXT NOT NULL,

    resolved_base_symbol_id UUID,

    inheritance_type TEXT DEFAULT 'CLASSIC',
    -- CLASSIC | MIXIN | TRAIT | INTERFACE

    resolution_strategy TEXT,
    -- DIRECT | IMPORT | FRAMEWORK | AI

    confidence FLOAT DEFAULT 1.0,

    status TEXT DEFAULT 'ACTIVE',

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_inheritance_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_inheritance_child
        FOREIGN KEY (child_symbol_id)
        REFERENCES graph_v1.symbols(symbol_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_inheritance_resolved
        FOREIGN KEY (resolved_base_symbol_id)
        REFERENCES graph_v1.symbols(symbol_id)
        ON DELETE SET NULL
);

-- =========================================================
-- EXTERNAL SYMBOLS
-- =========================================================

CREATE TABLE graph_v1.external_symbols (
    external_symbol_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    provider TEXT,
    -- django | react | stdlib | sqlalchemy | java_sdk

    name TEXT NOT NULL,

    canonical_name TEXT,

    module_name TEXT,

    symbol_type TEXT,

    framework TEXT,

    semantic_type TEXT,

    confidence FLOAT DEFAULT 0.0,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_external_symbol_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE
);

-- =========================================================
-- =========================================================
-- GRAPH RUNTIME
-- =========================================================
-- =========================================================

-- =========================================================
-- CALL TRACES
-- =========================================================

CREATE TABLE graph_runtime.call_traces (
    call_trace_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    symbol_id UUID,

    raw_call TEXT NOT NULL,

    resolved_target TEXT,

    call_type TEXT,

    confidence FLOAT DEFAULT 0.0,

    runtime_source TEXT,
    -- tracing | instrumentation | logs | ai

    context JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_call_trace_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE
);

-- =========================================================
-- DRIFT EVENTS
-- =========================================================

CREATE TABLE graph_runtime.drift_events (
    drift_event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    snapshot_id UUID NOT NULL,

    symbol_id UUID,

    relationship_id UUID,

    drift_type TEXT NOT NULL,
    -- ORPHAN_CALL | UNRESOLVED_SYMBOL | MISMATCH

    severity TEXT NOT NULL,
    -- LOW | MEDIUM | HIGH | CRITICAL

    expected TEXT,
    actual TEXT,

    resolution_status TEXT DEFAULT 'OPEN',
    -- OPEN | IGNORED | RESOLVED

    confidence FLOAT DEFAULT 0.0,

    context JSONB DEFAULT '{}'::jsonb,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    resolved_at TIMESTAMP,

    CONSTRAINT fk_drift_snapshot
        FOREIGN KEY (snapshot_id)
        REFERENCES graph_meta.snapshots(snapshot_id)
        ON DELETE CASCADE
);

-- =========================================================
-- =========================================================
-- INDEXES
-- =========================================================
-- =========================================================

-- =========================================================
-- META INDEXES
-- =========================================================

CREATE INDEX idx_projects_workspace
    ON graph_meta.projects(workspace_id);

CREATE INDEX idx_repositories_project
    ON graph_meta.repositories(project_id);

CREATE INDEX idx_snapshots_repository
    ON graph_meta.snapshots(repository_id);

CREATE INDEX idx_snapshots_branch
    ON graph_meta.snapshots(branch_name);

CREATE INDEX idx_snapshots_commit
    ON graph_meta.snapshots(commit_hash);

-- =========================================================
-- SYMBOL INDEXES
-- =========================================================

CREATE INDEX idx_symbols_snapshot
    ON graph_v1.symbols(snapshot_id);

CREATE INDEX idx_symbols_name
    ON graph_v1.symbols(name);

CREATE INDEX idx_symbols_canonical
    ON graph_v1.symbols(canonical_name);

CREATE INDEX idx_symbols_fqn
    ON graph_v1.symbols(fully_qualified_name);

CREATE INDEX idx_symbols_parent
    ON graph_v1.symbols(parent_symbol_id);

CREATE INDEX idx_symbols_module
    ON graph_v1.symbols(module_name);

CREATE INDEX idx_symbols_file
    ON graph_v1.symbols(file_path);

CREATE INDEX idx_symbols_type
    ON graph_v1.symbols(symbol_type);

CREATE INDEX idx_symbols_status
    ON graph_v1.symbols(status);

CREATE INDEX idx_symbols_snapshot_fqn
    ON graph_v1.symbols(snapshot_id, fully_qualified_name);

-- =========================================================
-- RELATIONSHIP INDEXES
-- =========================================================

CREATE INDEX idx_relationship_snapshot
    ON graph_v1.relationships(snapshot_id);

CREATE INDEX idx_relationship_source
    ON graph_v1.relationships(source_symbol_id);

CREATE INDEX idx_relationship_target
    ON graph_v1.relationships(target_symbol_id);

CREATE INDEX idx_relationship_type
    ON graph_v1.relationships(relationship_type);

CREATE INDEX idx_relationship_layer
    ON graph_v1.relationships(semantic_layer);

CREATE INDEX idx_relationship_status
    ON graph_v1.relationships(status);

-- =========================================================
-- INHERITANCE INDEXES
-- =========================================================

CREATE INDEX idx_inheritance_snapshot
    ON graph_v1.inheritance_edges(snapshot_id);

CREATE INDEX idx_inheritance_child
    ON graph_v1.inheritance_edges(child_symbol_id);

CREATE INDEX idx_inheritance_resolved
    ON graph_v1.inheritance_edges(resolved_base_symbol_id);

-- =========================================================
-- RUNTIME INDEXES
-- =========================================================

CREATE INDEX idx_call_traces_snapshot
    ON graph_runtime.call_traces(snapshot_id);

CREATE INDEX idx_drift_snapshot
    ON graph_runtime.drift_events(snapshot_id);

CREATE INDEX idx_drift_symbol
    ON graph_runtime.drift_events(symbol_id);

CREATE INDEX idx_drift_relationship
    ON graph_runtime.drift_events(relationship_id);