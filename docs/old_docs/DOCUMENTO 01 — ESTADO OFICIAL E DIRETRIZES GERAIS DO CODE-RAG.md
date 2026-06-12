A estrutura ideal daqui para frente seria:

DOCUMENTAÇÃO NOVA
DOCUMENTO 01

Arquitetura Consolidada do CODE-RAG
(que já criamos)

DOCUMENTO 02

Estado Operacional Real do Repositório
(ainda será produzido)

DOCUMENTO 03 (opcional/futuro)

DDL Oficial Consolidado PostgreSQL

Somente quando o schema estabilizar mais.

DOCUMENTO 04 (futuro)

Roadmap de Migração Semântica V2

Quando:

self/super resolver;
inheritance traversal;
runtime approximation;
framework adapters;

estiverem mais maduros.


# DOCUMENTO 01 — ESTADO OFICIAL E DIRETRIZES GERAIS DO CODE-RAG

Versão Consolidada Pós-Fase PostgreSQL + Consolidação Arquitetural

---

# 1. OBJETIVO REAL DO PROJETO

O CODE-RAG NÃO é:

* apenas um indexador de código;
* apenas um parser AST;
* apenas um grafo estático;
* apenas um mecanismo de embeddings;
* apenas um sistema RAG tradicional.

O CODE-RAG é:

um motor universal de indexação semântica persistida orientado a grafos, runtime-aware, incremental e multi-projeto.

---

# 2. VISÃO FINAL DO SISTEMA

O objetivo final é construir:

* semantic graph engine universal;
* runtime-aware graph engine;
* incremental semantic indexing engine;
* multi-language semantic engine;
* framework-aware semantic runtime;
* drift-aware graph intelligence;
* persistence-native semantic infrastructure;
* project-aware semantic operating system.

---

# 3. PRINCÍPIOS FUNDAMENTAIS

## 3.1 Persistência é Source-of-Truth

O PostgreSQL é a verdade oficial do sistema.

O estado semântico oficial NÃO vive:

* na memória;
* em GraphNodeV2;
* em caches locais;
* em SQLite.

O estado oficial vive no PostgreSQL.

---

## 3.2 O Grafo é Persistido

O grafo NÃO é reconstruído do zero como conceito central.

Ele é:

* incremental;
* versionável;
* auditável;
* observável;
* replayable;
* reconciliável.

---

## 3.3 O Sistema é Incremental

O projeto foi concebido para:

* atualização incremental;
* reconciliação parcial;
* replay semântico;
* resolução progressiva;
* enriquecimento contínuo.

O sistema NÃO deve depender de resets completos como estratégia arquitetural principal.

Reset total é apenas:

* ferramenta operacional;
* mecanismo de recuperação;
* fallback de integridade.

---

## 3.4 O Semantic Engine NÃO conhece linguagem

O núcleo semântico conhece apenas:

* symbols;
* relationships;
* ownership;
* imports;
* inheritance;
* semantic states;
* runtime hints;
* dispatch;
* confidence;
* provenance.

A linguagem existe apenas via adapters.

---

# 4. ARQUITETURA GLOBAL OFICIAL

```text
CODE-RAG
│
├── pipeline/                 -> Legacy Semantic Engine
│
├── pipeline_v2/              -> Future Universal Semantic Engine
│
├── PostgreSQL                -> Persistência Oficial
│
├── Runtime Graph Layer       -> Runtime Approximation
│
├── Drift Engine              -> Consistency Intelligence
│
├── Semantic Contracts        -> Ontologia Universal
│
└── Project Intelligence      -> Multi-Project Awareness
```

---

# 5. ESTADO ATUAL OFICIAL

## IMPLEMENTADO

### Legacy

* AST extraction;
* symbol extraction;
* semantic resolution;
* inheritance resolution;
* ORM awareness parcial;
* queryset propagation parcial;
* semantic graph persistence;
* PostgreSQL persistence.

---

### V2

* semantic contracts;
* graph contracts;
* runtime contracts;
* assignment semantic inference;
* drift harness;
* runtime graph bootstrap;
* PostgreSQL storage migration;
* graph repository abstraction;
* graph serialization contracts.

---

### PostgreSQL

Persistência consolidada em:

* `graph_v1`
* `graph_runtime`
* `graph_meta`

SQLite deixou de ser persistência operacional oficial.

---

# 6. O QUE AINDA NÃO ESTÁ CONSOLIDADO

## V2

Ainda incompleto:

* self resolver completo;
* super resolver completo;
* inheritance traversal universal;
* framework resolution universal;
* runtime approximation engine completo;
* semantic confidence propagation;
* semantic replay engine;
* graph reconciliation engine.

---

# 7. REGRA CRÍTICA

NENHUMA NOVA IMPLEMENTAÇÃO DEVE:

* criar sistemas paralelos;
* duplicar identidades;
* duplicar graph state;
* criar persistência concorrente;
* inventar ontologias;
* inventar contracts;
* introduzir abstrações especulativas.

---

# 8. MULTI-PROJECT AWARENESS (NOVO REQUISITO OFICIAL)

## Problema Detectado

A arquitetura original ainda assumia implicitamente:

* um único repositório;
* um único projeto semanticamente ativo.

Isso impede:

* CODE-RAG como produto universal;
* múltiplos projetos simultâneos;
* análise multi-repositório;
* graph federation;
* runtime isolation.

---

# 9. OBJETIVO DA CAMADA DE PROJETOS

O sistema deve operar semanticamente sobre:

* múltiplos projetos;
* múltiplos repositórios;
* múltiplas linguagens;
* múltiplos frameworks;
* múltiplos runtimes.

---

# 10. PROJECT INTELLIGENCE LAYER

Nova camada oficial obrigatória.

Responsável por:

* detectar linguagem;
* detectar frameworks;
* detectar variantes;
* detectar manifests;
* detectar runtime ecosystem;
* consolidar identidade do projeto;
* associar símbolos ao projeto correto.

---

# 11. DETECÇÃO TECNOLÓGICA

## Estratégia Oficial

Combinação híbrida:

### Bibliotecas Públicas

* [Guesslang](https://guesslang.readthedocs.io?utm_source=chatgpt.com)
* [Pygments](https://pygments.org?utm_source=chatgpt.com)

---

### Heurísticas Semânticas

Complementam:

* framework detection;
* runtime ecosystem;
* TSX/JSX;
* NodeJS;
* Django;
* FastAPI;
* React;
* Vue;
* Angular;
* Spring;
* Laravel;
* etc.

---

# 12. REGRA CRÍTICA SOBRE DETECÇÃO

Detecção NÃO é cosmética.

Ela influencia:

* semantic adapters;
* runtime inference;
* framework resolution;
* ontology interpretation;
* dispatch resolution;
* confidence propagation.

---

# 13. NOVA EXIGÊNCIA DE PERSISTÊNCIA

Todos os elementos do grafo devem pertencer a um projeto.

Incluindo:

* symbols;
* relationships;
* runtime traces;
* semantic states;
* drift events;
* snapshots;
* embeddings;
* runtime approximations.

---

# 14. ALTERAÇÃO OBRIGATÓRIA DE SCHEMA

Toda tabela semântica principal deve possuir:

```sql
project_id
```

---

# 15. NOVAS TABELAS OFICIAIS

## graph_meta.projects

```sql
CREATE TABLE graph_meta.projects (
    project_id TEXT PRIMARY KEY,

    project_name TEXT NOT NULL,

    root_path TEXT,

    primary_language TEXT,
    primary_framework TEXT,

    repository_type TEXT,

    confidence FLOAT DEFAULT 0.0,

    metadata JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## graph_meta.project_detection_profiles

```sql
CREATE TABLE graph_meta.project_detection_profiles (
    id SERIAL PRIMARY KEY,

    project_id TEXT NOT NULL,

    detector_version TEXT,

    language_profile JSONB,
    framework_profile JSONB,
    variant_profile JSONB,

    evidence JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);
```

---

# 16. ALTERAÇÕES OBRIGATÓRIAS NAS TABELAS EXISTENTES

## graph_v1.symbols

Adicionar:

```sql
project_id TEXT NOT NULL
```

---

## graph_v1.relationships

Adicionar:

```sql
project_id TEXT NOT NULL
```

---

## graph_runtime.call_traces

Adicionar:

```sql
project_id TEXT NOT NULL
```

---

## graph_runtime.drift_events

Adicionar:

```sql
project_id TEXT NOT NULL
```

---

# 17. GRAPH IDENTITY CONSOLIDATION

## Problema Detectado

O sistema começou a desenvolver:

dual identity semantics.

Exemplo:

* Symbol Registry;
* GraphNodeV2;
* runtime nodes;
* semantic nodes.

Isso gera:

* graph drift;
* duplicate identity;
* replay corruption;
* incremental inconsistency.

---

# 18. DECISÃO ARQUITETURAL OFICIAL

GraphNodeV2 NÃO é identidade oficial.

GraphNodeV2 passa a ser:

projeção estrutural transitória do registry persistido.

---

# 19. CONSEQUÊNCIA DIRETA

A identidade oficial do sistema passa a ser:

```text
symbol_id persistido no PostgreSQL
```

---

# 20. GraphNodeV2 PASSA A SER

Apenas:

* DTO estrutural;
* projeção de leitura;
* projection model;
* runtime representation;
* serialization helper.

---

# 21. O QUE NÃO PODE MAIS EXISTIR

GraphNodeV2 NÃO pode:

* possuir lifecycle próprio;
* possuir identidade própria;
* gerar IDs independentes;
* competir semanticamente com registry;
* manter estado autoritativo.

---

# 22. BENEFÍCIOS DA CONSOLIDAÇÃO

Resolve:

* dual identity drift;
* graph duplication semantics;
* replay inconsistency;
* incremental corruption;
* graph divergence.

Sem quebrar:

* harnesses;
* graph readers;
* context builders;
* ranking;
* retrieval;
* runtime projection.

---

# 23. ARQUITETURA OFICIAL DE IDENTIDADE

```text
PostgreSQL Registry
        ↓
Semantic Identity
        ↓
Graph Projection Layer
        ↓
GraphNodeV2
```

---

# 24. PIPELINE LEGACY — STATUS OFICIAL

O legacy NÃO é descartável.

Ele continua sendo:

* principal referência semântica;
* motor operacional maduro;
* verdade comportamental da resolução.

---

# 25. REGRA CRÍTICA SOBRE O LEGACY

Antes de implementar qualquer feature semântica na V2:

obrigatório validar:

* como o legacy resolve;
* como o legacy persiste;
* como o legacy propaga contexto;
* como o legacy calcula confiança.

---

# 26. V2 — PAPEL OFICIAL

A V2 NÃO deve copiar código do legacy.

Ela deve absorver:

* conceitos;
* contratos;
* ontologia;
* semântica;
* regras de resolução.

---

# 27. ORDEM OFICIAL DE MIGRAÇÃO SEMÂNTICA

## Fase 1

* self resolver;
* super resolver.

---

## Fase 2

* inheritance traversal;
* framework resolution.

---

## Fase 3

* ORM awareness;
* queryset propagation.

---

## Fase 4

* runtime approximation;
* confidence propagation;
* semantic replay.

---

# 28. DRIFT ENGINE — OBJETIVO FINAL

O Drift Engine deve detectar:

* orphan calls;
* unresolved symbols;
* runtime mismatch;
* semantic degradation;
* graph inconsistency;
* projection divergence;
* stale runtime states.

---

# 29. REGRAS OPERACIONAIS PARA NOVOS CHATS

## OBRIGATÓRIO

Antes de implementar:

* validar estado atual;
* validar arquivos reais;
* validar contracts;
* validar schema;
* validar pipeline afetado.

---

## PROIBIDO

Nunca:

* inventar classes;
* inventar arquitetura;
* inventar persistência;
* inventar fluxos;
* criar abstrações especulativas.

---

# 30. REGRA FINAL

O CODE-RAG NÃO está mais em fase experimental conceitual.

Ele já possui:

* ontologia;
* direção arquitetural;
* persistência oficial;
* semantic contracts;
* runtime contracts;
* graph model.

O foco agora é:

* consolidação;
* estabilização;
* migração controlada;
* remoção de dualidades;
* convergência arquitetural;
* evolução incremental consistente.
