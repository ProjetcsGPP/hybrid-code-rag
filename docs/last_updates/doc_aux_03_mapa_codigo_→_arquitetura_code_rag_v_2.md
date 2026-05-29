# 📗 DOC 03 — MAPA CÓDIGO → ARQUITETURA (CODE-RAG V2)

## 🎯 Objetivo
Este documento conecta diretamente o código-fonte real do CODE-RAG V2 com sua arquitetura conceitual e operacional.

Ele elimina ambiguidades entre:
- estrutura de pastas
- responsabilidades reais
- fluxos de execução
- camadas arquiteturais

---

# 🧠 1. VISÃO GERAL DO REPOSITÓRIO

O sistema está dividido em dois grandes blocos:

## 🟦 pipeline_v2/ (NÚCLEO ATUAL)
Sistema principal ativo

## 🟨 pipeline/ (LEGADO FUNCIONAL)
Sistema híbrido ainda usado em partes do fluxo

---

# 🧩 2. MAPEAMENTO ARQUITETURAL GLOBAL

```
ASTChunker
  ↓
SymbolExtractor / SymbolCoreV2
  ↓
RelationshipCoreV2
  ↓
IdentityConvergenceLayerV1
  ↓
GraphBuilderV2
  ↓
GraphWriterEngineV2 (parcial)
  ↓
PostgreSQL (migration_v2 / legacy)
```

---

# 🟦 3. PIPELINE_V2 — MAPEAMENTO DETALHADO

## 3.1 CORE BUILDER

### pipeline_v2/core/builder/

#### builder_pipeline.py
- Orquestrador simples de ingestão
- Entrada: file_path + symbols + relationships
- Saída: graph ingestido

➡ Papel: ENTRYPOINT de construção de grafo

---

#### graph_builder.py
- Responsável por:
  - ingestão de symbols
  - ingestão de relationships
  - integração com IdentityRegistry
  - criação de GraphNodeV2 / GraphEdgeV2

➡ Papel: NÚCLEO DE CONSTRUÇÃO DO GRAFO

---

#### build_context.py (implícito)
- container de dados do pipeline

➡ Papel: CONTEXTO DE EXECUÇÃO

---

## 3.2 WRITER LAYER

### pipeline_v2/core/writer/

#### graph_writer_engine_v2.py
- escreve symbols e relationships no graph store
- integra inheritance writer

➡ Papel: PERSISTÊNCIA INTERNA DO GRAFO

Subcomponentes:
- SymbolWriterV2
- RelationshipWriterV2
- InheritanceWriterV2

---

## 3.3 RUNTIME LAYER

### runtime_execution_graph_v2.py

- simula execução sobre grafo estático
- não executa código real
- produz:
  - execution_trace
  - runtime_edges
  - node_state

➡ Papel: SIMULAÇÃO DE EXECUÇÃO

---

## 3.4 RESOLUTION LAYER

### symbol_resolution_engine_v2.py

Responsável por:
- resolver calls
- normalizar chamadas
- resolver targets
- fallback unresolved

➡ Papel: RESOLUÇÃO SEMÂNTICA E ESTRUTURAL

---

## 3.5 RELATIONSHIP CORE

### relationship_core.py

Responsável por:
- inferência semântica de relações
- criação de relationships
- integração com SymbolResolutionEngine
- criação via RelationshipFactoryV2

➡ Papel: MOTOR SEMÂNTICO DE RELAÇÕES

---

## 3.6 IDENTITY LAYER

### identity/

#### identity_registry.py
- store central de entidades
- by_id / by_name / by_canonical

➡ Papel: REGISTRO GLOBAL EM MEMÓRIA

---

#### identity_convergence_layer_v1.py
- resolve identidade entre camadas
- canonicalização
- fallback external

➡ Papel: NORMALIZAÇÃO GLOBAL DE IDENTIDADE

---

#### identity_service_v2.py / gateway.py
- wrappers de acesso ao registry

➡ Papel: INTERFACES DE ACESSO

---

## 3.7 SYMBOL CORE

### symbol_core (não totalmente exibido aqui)
- criação de SymbolV2
- interface com identity_registry

➡ Papel: REPRESENTAÇÃO SEMÂNTICA BASE

---

# 🟨 4. PIPELINE LEGACY (pipeline/)

## 4.1 structure/

### symbol_extractor.py
- converte AST chunk → Symbol
- resolve parent_symbol_id

➡ LEGADO: extração estrutural

---

### relationship_extractor.py
- extrai relações simples (BELONGS_TO)
- resolve hierarquia via symbol_index

➡ LEGADO: relações estruturais básicas

---

### semantic/graph/semantic_graph_builder.py
- constrói edges semânticas
- usa CallNormalizer + resolver

➡ LEGADO: grafo semântico inicial

---

## 4.2 semantic_registry.py

- sistema de conceitos semânticos
- embeddings
- cosine similarity

➡ LEGADO: camada semântica auxiliar (NLP)

---

# 🧪 5. TESTS / HARNESSES

## pipeline_v2/tests/

### harness_full_pipeline.py
- pipeline completo end-to-end
- AST → symbols → relationships → graph → audit

➡ VALIDAÇÃO SISTÊMICA COMPLETA

---

### harness_transition_layer.py
- valida transição:
  - contract → core
  - AST → SymbolAdapter

➡ VALIDAÇÃO DE COMPATIBILIDADE

---

### harness_contract_drift.py
- detecta drift entre:
  - symbols vs graph nodes
  - relationships vs edges

➡ VALIDAÇÃO DE CONSISTÊNCIA

---

### harness_identity_graph_drift.py
- compara IdentityRegistry vs Graph

➡ VALIDAÇÃO DE INTEGRIDADE IDENTITÁRIA

---

# 🗄️ 6. PERSISTÊNCIA POSTGRESQL

## migration_legacy
- symbols
- relationships
- semantic_references

➡ compatibilidade histórica

---

## migration_v2
- nodes
- edges

➡ modelo atual do grafo

---

# 🔁 7. FLUXO REAL DE DADOS

## 7.1 Fluxo estrutural

AST
 → SymbolExtractor
 → SymbolCoreV2
 → RelationshipCoreV2
 → GraphBuilderV2
 → Graph Store
 → PostgreSQL

---

## 7.2 Fluxo de identidade

Any Entity
 → IdentityConvergenceLayerV1
 → IdentityRegistryV2
 → Canonical ID

---

## 7.3 Fluxo semântico

Chunk
 → SemanticAdapter
 → RelationshipResolverV2
 → RelationshipFactoryV2
 → Edge

---

# ⚠️ 8. GAPS ARQUITETURAIS IDENTIFICADOS

## 8.1 inconsistência estrutural
- Symbol ≠ Node
- Relationship ≠ Edge

---

## 8.2 identidade não persistida
- IdentityRegistry é memória apenas

---

## 8.3 dual graph system
- runtime graph ≠ postgres graph

---

## 8.4 legacy ainda ativo
- pipeline/ ainda influencia resultados

---

# 📌 9. MAPEAMENTO FINAL (RESUMO)

| Camada | Código |
|--------|-------|
| AST | pipeline.ast_chunker |
| Symbol | SymbolCoreV2 / SymbolExtractor |
| Relationship | RelationshipCoreV2 |
| Identity | IdentityRegistryV2 |
| Graph Build | GraphBuilderV2 |
| Graph Write | GraphWriterEngineV2 |
| Runtime | RuntimeExecutionGraphV2 |
| Persistence | PostgreSQL migration_v2 |

---

# 🧠 10. CONCLUSÃO

Este documento estabelece o mapa real entre código e arquitetura.

Ele revela que CODE-RAG V2 já possui:
- pipeline funcional completo
- identidade centralizada (mas não persistente)
- grafo híbrido (runtime + persistence)

Mas ainda carece de:
- unificação total de grafo
- persistência de identidade
- eliminação completa do legado

