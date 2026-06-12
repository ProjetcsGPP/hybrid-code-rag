# 📘 DOC 01 — ESTADO OPERACIONAL DETALHADO (CODE-RAG V2)

## 🎯 Objetivo
Descrever com precisão o estado REAL do sistema CODE-RAG V2, incluindo execução, pipelines, camadas, fluxos e fontes de verdade.

---

# 🧠 1. VISÃO GERAL DO SISTEMA

CODE-RAG V2 é um sistema híbrido composto por:

- Extração estrutural de código (AST)
- Inferência semântica (relationships)
- Construção de grafo (nodes/edges)
- Resolução de identidade canônica
- Persistência em PostgreSQL

---

# 🔄 2. PIPELINE REAL DE EXECUÇÃO

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
GraphRepositoryPostgresV2
  ↓
PostgreSQL (migration_v2 / migration_legacy)

---

# 🧩 3. CAMADAS DO SISTEMA

## 🟦 CAMADA SEMÂNTICA
Responsável por interpretar código.

Componentes:
- SymbolCoreV2
- RelationshipCoreV2
- SemanticAdapter
- ContractEnforcer

Função:
- Extrair significado do código
- Gerar relações entre símbolos

---

## 🟪 CAMADA DE IDENTIDADE
Responsável por resolução global de entidades.

Componentes:
- IdentityRegistryV2
- IdentityConvergenceLayerV1

Função:
- Resolver referências
- Canonicalizar entidades

Estado:
- Em memória
- Não persistido

---

## 🟩 CAMADA DE GRAFO
Responsável por estruturação de dados.

Componentes:
- GraphBuilderV2
- GraphWriterEngineV2
- RuntimeExecutionGraphV2

Função:
- Converter entidades em nodes/edges
- Simular execução

---

## 🟨 CAMADA DE PERSISTÊNCIA
PostgreSQL:

### migration_legacy
- symbols
- relationships
- semantic_references

### migration_v2
- nodes
- edges

---

# 📊 4. FONTES DE VERDADE

| Camada | Fonte |
|--------|------|
| Identidade | IdentityRegistryV2 (memória) |
| Semântica | RelationshipCoreV2 |
| Estrutura | GraphBuilderV2 |
| Persistência | PostgreSQL |
| Runtime | RuntimeExecutionGraphV2 |

---

# ⚠️ 5. DIVERGÊNCIAS E DRIFT

- Identity não persistido
- Graph não reconstruível completamente do banco
- Symbol ≠ Node
- Relationship ≠ Edge

---

# 🔁 6. DUPLICAÇÃO DE MODELOS

## Symbol vs Node
- Symbol: semântico
- Node: estrutural

## Relationship vs Edge
- Relationship: inferido
- Edge: estruturado

---

# 🚨 7. RISCOS ATUAIS

- múltiplas fontes de verdade
- inconsistência entre runtime e persistência
- identidade em memória
- grafo não determinístico

---

# 🧠 8. ESTADO DE MATURIDADE

| Subsystem | Status |
|----------|-------|
| AST Pipeline | Estável |
| Symbol Extraction | Estável |
| Relationship Core | Estável |
| Identity Layer | Parcial |
| Graph Builder | Estável |
| Persistence | Estável |
| Unificação global | Incompleto |

---

# 📌 9. CONCLUSÃO OPERACIONAL

O sistema está funcional, porém ainda não possui uma única fonte de verdade global, operando como um sistema híbrido em transição entre semântica e grafo estrutural.

