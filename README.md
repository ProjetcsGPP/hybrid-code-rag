# CODE-RAG — Hybrid Semantic Retrieval Pipeline

## README.md

````markdown
# CODE-RAG

Pipeline híbrido de recuperação semântica para análise de código-fonte utilizando:

- AST Chunking
- Embeddings Semânticos
- Hybrid Ranking
- Semantic Registry
- Intent Detection
- ChromaDB
- Retrieval contextual para LLMs

---

# Objetivo

O projeto CODE-RAG foi criado para evoluir além do RAG tradicional baseado apenas em similaridade vetorial.

O foco é construir um pipeline especializado em entendimento estrutural e semântico de código-fonte, permitindo:

- Busca contextual inteligente
- Recuperação semântica híbrida
- Entendimento de intenção da consulta
- Ranking contextual de código
- Futuro suporte a agentes de engenharia reversa e arquitetura

---

# Arquitetura Atual

```text
User Query
    ↓
Intent Detection
    ↓
Embedding Generation
    ↓
Semantic Registry Matching
    ↓
Vector Search (ChromaDB)
    ↓
Hybrid Ranker
    ├── Vector Similarity
    ├── Semantic Alignment
    ├── Structural Boost
    ├── Intent Score
    └── Importance Score
    ↓
Final Ranked Chunks
````

---

# Estrutura do Projeto

```text
code-rag/
│
├── pipeline/
│   ├── ast_chunker.py
│   ├── embeddings.py
│   ├── semantic_registry.py
│   ├── contracts.py
│   │
│   ├── retrieval/
│   │   ├── retriever.py
│   │   └── hybrid_retriever.py
│   │
│   ├── ranking/
│   │   └── hybrid_ranker.py
│   │
│   ├── intent/
│   │   ├── intent_classifier.py
│   │   └── intent_registry.py
│   │
│   ├── indexer/
│   │   └── chroma_indexer.py
│   │
│   ├── test_pipeline.py
│   └── test_intent.py
│
├── vectordb.py
├── retriever.py
├── indexer.py
├── rag_chat.py
├── cli.py
├── config.py
├── requirements.txt
├── README.md
└── docs/
```

---

# Componentes

## AST Chunker

Responsável por:

* Ler arquivos Python
* Extrair classes
* Extrair funções
* Criar chunks estruturados
* Preservar contexto estrutural

---

## Semantic Registry

Sistema responsável por:

* Classificação semântica
* Matching de conceitos
* Similaridade semântica
* Identificação contextual

Conceitos atuais:

* query
* mutation
* validation
* authorization
* business_logic
* general

---

## Hybrid Ranker

Sistema central de ranking.

Combina:

* Similaridade vetorial
* Similaridade semântica
* Structural boost
* Importância estrutural
* Intenção da consulta

---

## Intent Detection

Detecta intenção da query do usuário.

Exemplos:

| Query              | Intent        |
| ------------------ | ------------- |
| onde salva usuário | mutation      |
| onde valida senha  | validation    |
| permissões RBAC    | authorization |
| busca usuário      | query         |

---

## ChromaDB

Banco vetorial utilizado para:

* armazenamento de embeddings
* busca vetorial
* recuperação semântica

---

# Pipeline Atual

## Indexação

```bash
python -m pipeline.test_pipeline --file caminho/arquivo.py --reset
```

Fluxo:

1. AST parsing
2. Chunk extraction
3. Semantic enrichment
4. Embedding generation
5. Chroma indexing

---

## Retrieval

Fluxo:

1. Query embedding
2. Intent detection
3. Semantic concept matching
4. Candidate retrieval
5. Hybrid ranking
6. Final scoring

---

# Estado Atual do Projeto

## Fase Atual

FASE 2A — Hybrid Retrieval Estabilizado

---

## Implementado

* AST chunking
* Semantic Registry
* Intent detection
* ChromaDB integration
* Hybrid ranking
* Structural scoring
* Importance scoring
* Semantic alignment
* Metadata enrichment
* Chunk normalization
* Retrieval pipeline
* Contratos estabilizados

---

## Próximas Etapas

### Fase 2B

* Structural graph retrieval
* Parent-child navigation
* Cross-file linking
* Symbol graph
* Import graph
* Call graph

### Fase 3

* Multi-file contextual retrieval
* Repository understanding
* Architectural reasoning
* Dependency tracing
* Agentic retrieval
* Autonomous code exploration

### Fase 4

* Fine-tuning especializado
* Memory system
* Persistent semantic graph
* Multi-agent orchestration
* Self-improving retrieval

---

# Instalação

## Clonar repositório

```bash
git clone <repo-url>
cd code-rag
```

## Criar ambiente virtual

```bash
python -m venv venv
source venv/bin/activate
```

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Dependências Principais

* sentence-transformers
* chromadb
* numpy
* torch
* transformers

---

# Exemplo de Uso

## Indexar arquivo

```bash
python -m pipeline.test_pipeline \
  --file /path/models.py \
  --reset
```

---

## Consultar retrieval

```python
from pipeline.retrieval.hybrid_retriever import HybridRetriever

retriever = HybridRetriever(
    embedding_service,
    semantic_registry,
)

results = retriever.retrieve(
    query="onde salva usuário",
    k=5,
)
```

---

# Filosofia do Projeto

O projeto NÃO busca apenas similaridade vetorial.

O objetivo é construir:

* entendimento estrutural
* entendimento arquitetural
* reasoning contextual
* navegação semântica de código
* recuperação inteligente orientada por intenção

---

# Licença

MIT

````

---

# Estrutura Recomendada da Pasta docs/

```text
docs/
│
├── architecture/
│   ├── pipeline-overview.md
│   ├── retrieval-flow.md
│   ├── semantic-registry.md
│   └── hybrid-ranking.md
│
├── development/
│   ├── roadmap.md
│   ├── conventions.md
│   ├── debugging.md
│   └── testing.md
│
├── research/
│   ├── rag-evolution.md
│   ├── hybrid-retrieval-notes.md
│   └── semantic-search.md
│
├── phases/
│   ├── phase-1.md
│   ├── phase-2A.md
│   ├── phase-2B.md
│   ├── phase-3.md
│   └── phase-4.md
│
└── decisions/
    ├── adr-001-semantic-registry.md
    ├── adr-002-hybrid-ranker.md
    └── adr-003-contract-stabilization.md
````

---

# docs/architecture/pipeline-overview.md

```markdown
# Pipeline Overview

O pipeline CODE-RAG é dividido em:

1. Parsing estrutural
2. Chunking semântico
3. Embedding generation
4. Semantic enrichment
5. Vector indexing
6. Hybrid retrieval
7. Final ranking

Objetivo:

Criar um mecanismo avançado de entendimento contextual de código.
```

---

# docs/development/roadmap.md

```markdown
# Roadmap

## Fase 1

- AST parsing
- Chunk extraction
- Embeddings
- ChromaDB

## Fase 2A

- Hybrid retrieval
- Semantic registry
- Intent detection
- Metadata enrichment

## Fase 2B

- Graph retrieval
- Structural navigation
- Symbol relationships

## Fase 3

- Multi-file reasoning
- Repository understanding
- Autonomous navigation

## Fase 4

- Agents
- Persistent memory
- Self-improving ranking
```

---

# docs/development/conventions.md

```markdown
# Convenções do Projeto

## Estrutura

- snake_case para arquivos
- PascalCase para classes
- funções pequenas e focadas

## Contracts

Toda comunicação entre pipeline stages deve utilizar contratos explícitos.

## Retrieval

Nenhuma etapa deve depender implicitamente de metadata opcional.

## Ranking

Todos os scores devem ser normalizados.
```

---

# docs/architecture/hybrid-ranking.md

```markdown
# Hybrid Ranking

O ranking híbrido combina múltiplos sinais:

- vector similarity
- semantic alignment
- intent score
- structural score
- importance score

Objetivo:

Reduzir falsos positivos do retrieval vetorial puro.
```

---

# docs/decisions/adr-001-semantic-registry.md

```markdown
# ADR-001 — Semantic Registry

## Contexto

Embeddings vetoriais puros não representam corretamente intenção estrutural.

## Decisão

Criar Semantic Registry próprio.

## Consequências

- Melhor alinhamento semântico
- Possibilidade de reasoning estrutural
- Base para graph retrieval futuro
```

---

# docs/phases/phase-2A.md

```markdown
# Phase 2A — Stabilized Hybrid Retrieval

## Objetivos

- estabilizar pipeline
- padronizar contratos
- integrar semantic registry
- integrar hybrid ranker

## Status

Concluído.

## Resultados

- retrieval contextual funcional
- ranking híbrido operacional
- enrichment estável
- pipeline desacoplado
```
