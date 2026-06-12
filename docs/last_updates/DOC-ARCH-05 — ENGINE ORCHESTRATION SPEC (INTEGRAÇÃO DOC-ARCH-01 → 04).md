# 📄 DOC-ARCH-05 — ENGINE ORCHESTRATION SPEC (INTEGRAÇÃO DOC-ARCH-01 → 04)

Observação importante! Essa documentação foi escrita baseada nos documentos orginiais e consequequentemente, não estavam com a terminologia adequada: "Todas as referências a EXTERNAL e UNRESOLVED nestes documentos devem ser interpretadas como estados semânticos tipados derivados de ResolutionEventV2, e não como artefatos string-based legados."

## Status

CANÔNICO — ORQUESTRAÇÃO EXECUTÁVEL

## Objetivo

Este documento define a **orquestração completa da Fase 3 (Semantic Reconciliation Layer)** integrando:

* DOC-ARCH-01 — Semantic Reconciliation Specification
* DOC-ARCH-02 — Pipeline de Reconciliation
* DOC-ARCH-03 — Semantic Scoring Engine
* DOC-ARCH-04 — Semantic Decision Engine & Promotion Policy Engine

em um **fluxo único executável, determinístico e auditável**.

---

# 1. VISÃO GERAL DA PIPELINE ORQUESTRADA

A arquitetura final da Fase 3 é um sistema de **multi-stage semantic execution pipeline** com separação rígida de responsabilidades.

```
SOURCE CODE
   ↓
AST CHUNKING
   ↓
SYMBOL EXTRACTION
   ↓
RELATIONSHIP EXTRACTION
   ↓
IDENTITY RESOLUTION (DOC-B CONGELADO)
   ↓
GRAPH BUILD (DOC-B CONGELADO)
   ↓
CONTRACT VALIDATION
   ↓
────────────────────────────
SEMANTIC RECONCILIATION (DOC-ARCH-01 / 02)
────────────────────────────
   ↓
SCORING ENGINE (DOC-ARCH-03)
   ↓
DECISION ENGINE (DOC-ARCH-04)
   ↓
PROMOTION POLICY ENGINE (DOC-ARCH-04)
   ↓
GRAPH ENRICHMENT
   ↓
PERSISTENCE LAYER
```

---

# 2. ORQUESTRADOR CENTRAL

## 2.1 Nome lógico

```
SemanticReconciliationOrchestratorV3
```

---

## 2.2 Responsabilidade

O Orchestrator NÃO decide semântica.

Ele apenas:

* coordena etapas
* garante ordem de execução
* controla fluxo de dados
* registra eventos
* preserva determinismo

---

# 3. PIPELINE EXECUTION MODEL

## 3.1 Entrada

```python
PipelineInputV3:
  - chunks
  - symbols
  - relationships
  - identity_graph
  - contract_state
```

---

## 3.2 Saída

```python
PipelineOutputV3:
  - resolved_graph
  - decision_events
  - promotion_events
  - unresolved_registry
  - reconciliation_report
```

---

# 4. EXECUÇÃO PASSO A PASSO

---

## STEP 0 — CONTRACT VALIDATION (pré-condição)

Responsável:

* Contract Enforcer (DOC-B)

Verifica:

* integrity do graph
* identity consistency
* schema compliance

❗ Se falhar → pipeline aborta

---

## STEP 1 — SEMANTIC RECONCILIATION ENGINE (DOC-ARCH-01/02)

### Entrada:

* EXTERNAL nodes
* UNRESOLVED references
* PARTIAL bindings

### Saída:

* SemanticCandidateSetV3

Estrutura:

```python
{
  "symbol": "...",
  "candidates": [...],
  "context": [...],
  "origin": ["import", "attribute", "runtime", "cross-file"]
}
```

---

## STEP 2 — SEMANTIC SCORING ENGINE (DOC-ARCH-03)

### Função:

Converter candidatos em ranking probabilístico.

### Saída:

```python
SemanticScoreV3:
  symbol: str
  scored_candidates: List[{
      target: str
      score: float
      evidence: list
  }]
```

---

## STEP 3 — DECISION ENGINE (DOC-ARCH-04)

### Entrada:

* scored_candidates

### Saída:

```python
SemanticDecisionEventV2
```

Tipos:

* PROMOTE
* REJECT
* DEFER

---

## STEP 4 — PROMOTION POLICY ENGINE (DOC-ARCH-04)

### Função:

Aplicar regra final de estado.

```
if confidence >= 0.90:
    EXTERNAL → STRICT
```

---

## STEP 5 — GRAPH ENRICHMENT

Responsável:

* Graph Enricher

Funções:

* atualizar nodes
* adicionar edges resolvidos
* remover ambiguity state
* persistir decisões

---

## STEP 6 — PERSISTENCE LAYER

Responsável:

* persistência canônica

Garantias:

* atomic commit
* versionamento de graph snapshot
* audit trail completo

---

# 5. FLUXO DE DADOS (STATE TRANSITION MODEL)

## 5.1 Estados possíveis

```
RAW CODE
→ CHUNKED
→ SYMBOLIZED
→ RELATIONIZED
→ IDENTIFIED
→ CONTRACT-VALIDATED
→ RECONCILED
→ SCORED
→ DECIDED
→ PROMOTED
→ PERSISTED
```

---

## 5.2 Transições críticas

### EXTERNAL FLOW

```
EXTERNAL
 → RECONCILIATION
 → SCORING
 → DECISION
 → PROMOTION (ou REJECT)
```

---

### UNRESOLVED FLOW

```
UNRESOLVED
 → RECONCILIATION
 → POSSIBLE PROMOTION OR DEFER
```

---

# 6. INVARIANTES DO SISTEMA

## 6.1 Invariante de identidade

```
Identity Registry MUST NOT be modified after STEP 0
```

---

## 6.2 Invariante de graph

```
GraphBuilder MUST NOT infer semantics
```

---

## 6.3 Invariante de decisão

```
Decision Engine is final authority on semantic promotion
```

---

## 6.4 Invariante de contratos

```
No stage may bypass contract validation
```

---

# 7. MODELO DE EXECUÇÃO (SEQUENCIAL OBRIGATÓRIO)

O pipeline é estritamente sequencial:

```
Contract Validation
→ Reconciliation
→ Scoring
→ Decision
→ Promotion
→ Graph Enrichment
→ Persistence
```

❗ Paralelismo permitido apenas dentro de scoring interno

---

# 8. AUDITABILIDADE COMPLETA

Cada execução deve gerar:

```python
PipelineExecutionTraceV3:
  run_id
  timestamp
  input_hash
  decisions
  promotions
  rejections
  deferrals
  final_graph_delta
```

---

# 9. CONTROLE DE QUALIDADE GLOBAL

## Métricas obrigatórias:

* external_reduction_rate
* unresolved_resolution_rate
* promotion_precision
* decision_confidence_distribution
* graph_consistency_score
* drift_score (DEVE permanecer 0.0)

---

# 10. CRITÉRIO DE SUCESSO DA ORQUESTRAÇÃO

O sistema está correto se:

* pipeline executa sem bypass de etapas
* decisões são auditáveis
* graph permanece consistente
* Identity Registry não é violado
* PROMOTION ocorre apenas via DOC-ARCH-04
* EXTERNAL diminui progressivamente
* UNRESOLVED converge para STRICT ou REJECT

---

# 11. RESULTADO ARQUITETURAL FINAL

Após integração DOC-ARCH-01 → 04:

O CODE-RAG V2 passa a operar como:

```
Deterministic Semantic Execution System
with:
- Multi-pass resolution
- Scored semantic binding
- Policy-driven promotion
- Contract-enforced graph evolution
```

---

# 12. CONCLUSÃO

Este documento transforma a Fase 3 de:

> conjunto de módulos independentes

para:

> sistema único orquestrado com execução determinística e auditável

---
