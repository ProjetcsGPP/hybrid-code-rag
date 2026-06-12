A seguir está o **diagrama arquitetural operacional consolidado da Fase 3 (CODE-RAG V2)**, integrando:

* Pipeline base (AST → Graph)
* Camada Contract-Driven
* Semantic Reconciliation Layer
* Engines DOC-ARCH-01 a DOC-ARCH-04
* Estados semânticos (STRICT / EXTERNAL / UNRESOLVED / PARTIAL / PROMOTED)
* Fluxos de decisão e promoção

---

# 🧠 DIAGRAMA ARQUITETURAL OPERACIONAL — FASE 3 (CODE-RAG V2)

```mermaid
flowchart TD

%% =========================
%% 1. SOURCE LAYER
%% =========================
A[Source Code Repository] --> B[AST Extraction Layer]

%% =========================
%% 2. PIPELINE CORE
%% =========================
B --> C[Symbol Extraction Engine]
C --> D[Relationship Extraction Engine]
D --> E[Identity Resolution Layer]
E --> F[Graph Builder V2]
F --> G[Contract Validation Layer]

%% =========================
%% 3. SEMANTIC RECONCILIATION ENTRY
%% =========================
G --> H[Semantic Reconciliation Layer]

%% =========================
%% 4. DOC-ARCH ENGINE SUITE
%% =========================

H --> I1[DOC-ARCH-01\nSemantic Reconciliation Spec Engine]
I1 --> I2[DOC-ARCH-02\nReconciliation Pipeline Orchestrator]
I2 --> I3[DOC-ARCH-03\nSemantic Scoring Engine]
I3 --> I4[DOC-ARCH-04\nDecision & Promotion Policy Engine]

%% =========================
%% 5. SEMANTIC DECISION FLOW
%% =========================

I4 --> J{Semantic Decision Gate}

J -->|confidence >= 0.90| K[PROMOTED]
J -->|0.60 <= confidence < 0.90| L[PARTIAL]
J -->|confidence < 0.60| M[UNRESOLVED]
J -->|builtin/framework detected| N[EXTERNAL CLASSIFIED]

%% =========================
%% 6. PROMOTION LOOP
%% =========================

K --> O[Identity Registry Update]
O --> F

L --> H
M --> H
N --> P[External Registry Store]

%% =========================
%% 7. GRAPH ENRICHMENT
%% =========================

K --> Q[Graph Enrichment Engine]
Q --> F

%% =========================
%% 8. FINAL STATE OUTPUT
%% =========================

F --> R[Persistent Semantic Graph]

%% =========================
%% 9. STATE MODEL
%% =========================

subgraph STATE_MODEL[Semantic State Model]

S1[STRICT]
S2[EXTERNAL]
S3[UNRESOLVED]
S4[PARTIAL]
S5[PROMOTED]

end

K --- S1
N --- S2
M --- S3
L --- S4
K --- S5

%% =========================
%% 10. LEGACY CONTROL BOUNDARY
%% =========================

X[Legacy System Signals\n(external:: / UNRESOLVED::)] --> H

Y[Runtime Signals] --> H

Z[Framework/StdLib Detection] --> N
```

---

# 🧩 LEITURA ARQUITETURAL DO FLUXO

## 1. Pipeline base (imutável da Fase 2)

O núcleo continua sendo:

* AST Extraction
* Symbol Extraction
* Relationship Extraction
* Identity Resolution
* Graph Build
* Contract Validation

👉 Este fluxo permanece **CONGELADO (DOC-B / DOC-A)**

---

## 2. Entrada da Fase 3

Após validação de contratos:

➡ entra a camada nova:

### Semantic Reconciliation Layer

Responsável por:

* resolver EXTERNAL
* resolver UNRESOLVED
* reduzir ambiguidade semântica
* aplicar scoring
* decidir promoção

---

## 3. Engine Orchestration (DOC-ARCH-01 → 04)

### DOC-ARCH-01 — Specification Engine

Define regras formais de:

* o que pode ser resolvido
* o que é ignorado
* o que é builtin/framework

---

### DOC-ARCH-02 — Orchestrator

Coordena:

* batch de símbolos EXTERNAL
* cross-file resolution
* execução do scoring
* execução da decisão

---

### DOC-ARCH-03 — Scoring Engine

Gera:

* confidence score
* category classification
* binding probability
* resolution quality index

---

### DOC-ARCH-04 — Decision Engine (núcleo crítico)

Aplica política:

| Condição          | Resultado  |
| ----------------- | ---------- |
| ≥ 0.90            | PROMOTED   |
| 0.60–0.89         | PARTIAL    |
| < 0.60            | UNRESOLVED |
| builtin/framework | EXTERNAL   |

---

## 4. Loop de retroalimentação (essencial)

O sistema NÃO é linear.

Ele possui ciclo:

```
Graph → Reconciliation → Promotion → Identity Update → Graph
```

Isso garante:

* refinamento incremental
* redução progressiva de EXTERNAL
* estabilidade da Identity Layer

---

## 5. Estados semânticos oficiais

* STRICT → já resolvido e estável
* EXTERNAL → conhecido mas não ligado
* UNRESOLVED → não resolvido
* PARTIAL → resolução incompleta
* PROMOTED → resolvido via reconciliação

---

## 6. Boundary de segurança arquitetural

Camadas protegidas:

* Identity Registry ❌ não pode ser alterado pela reconciliação direta
* GraphBuilder ❌ não pode inferir identidade
* Contracts ❌ não podem ser violados
* Persistence ❌ não pode ser reescrita por scoring

---

## 7. Resultado arquitetural da Fase 3

Quando completo:

* EXTERNAL → drasticamente reduzido
* UNRESOLVED → classificado
* STRICT → dominante
* PROMOTED → mecanismo ativo
* Graph → semanticamente denso e reconciliado

---

Se quiser o próximo passo, posso gerar:

1. **DOC-ARCH-00 (Documento mestre de arquitetura consolidada)**
2. **versão executável em pseudo-code do orchestrator**
3. **ou um diagrama separado só do DOC-ARCH-01 a 04 (internals detalhados)**
