# CODE-RAG — Structural Contracts & Canonical Entities (FASE 2B)

# 📌 Objetivo

Após a formalização de:

* Symbol Model
* Relationship Model
* Relationship Extraction Layer
* Structural Persistence Layer
* Structural Evidence Layer
* Context Assembly Foundations

O próximo passo correto da FASE 2B é:

# formalizar contratos estruturais canônicos

---

# 📌 Objetivo Real da Etapa

O objetivo NÃO é implementar traversal ainda.

O objetivo NÃO é criar graph reasoning.

O objetivo desta etapa é:

# transformar a Structural Layer em um runtime orientado a entidades explícitas

---

# 📌 Problema Arquitetural Atual

Hoje o sistema ainda depende fortemente de:

```python
Dict[str, Any]
```

Espalhados entre:

* retrieval
* ranking
* chunking
* metadata
* structural evidence
* context assembly

---

# 📌 Principal Risco Atual

Sem contratos estruturais explícitos, traversal inevitavelmente evolui para:

* metadata procedural
* dicionários arbitrários
* acoplamento implícito
* graph spaghetti
* inconsistência estrutural
* payloads divergentes
* expansão descontrolada

---

# 📌 Nova Direção Arquitetural

A arquitetura correta começa a evoluir para:

```text
Structural Runtime
    ↓
Canonical Entities
    ↓
Structural Operations
```

---

# 📌 O que são Canonical Entities

Canonical Entities representam:

# entidades estruturais oficiais do runtime

---

# 📌 IMPORTANTE

Canonical Entities NÃO são:

* payloads improvisados
* metadata livre
* estruturas locais do módulo
* dicionários contextuais

---

# 📌 Objetivo dos Contratos

Os contratos estruturais devem permitir:

## ✅ consistência estrutural

## ✅ evolução segura

## ✅ traversal controlado futuro

## ✅ reasoning arquitetural futuro

## ✅ interoperabilidade entre camadas

## ✅ separação de responsabilidades

## ✅ versionamento estrutural futuro

---

# 📌 Papel da Structural Contracts Layer

A Structural Contracts Layer é responsável por:

# definir entidades oficiais do runtime estrutural

---

# 📌 Responsabilidades

## ✅ Definir contratos explícitos

## ✅ Definir entidades canônicas

## ✅ Definir boundaries estruturais

## ✅ Garantir interoperabilidade

## ✅ Reduzir acoplamento procedural

---

# 📌 NÃO é responsabilidade da camada

## ❌ executar traversal

## ❌ realizar retrieval

## ❌ calcular ranking

## ❌ montar contexto

## ❌ inferir semântica

## ❌ expandir neighborhood

---

# 📌 Estrutura Conceitual

## Módulo sugerido

```text
pipeline/contracts/
    symbol.py
    relationship.py
    structural_evidence.py
    context_group.py
    structural_candidate.py
    structural_query.py
    traversal_boundary.py
```

---

# 📌 Canonical Entity — Symbol

## Responsabilidade

Representar entidade estrutural canônica.

---

## Estrutura Conceitual

```python
class Symbol:

    symbol_id: str

    symbol_path: str

    symbol_name: str

    symbol_type: str

    module_name: str

    file_path: str

    parent_symbol_id: str | None

    semantic_type: str

    start_line: int
    end_line: int
```

---

# 📌 Canonical Entity — Relationship

## Responsabilidade

Representar relação estrutural explícita.

---

## Estrutura Conceitual

```python
class Relationship:

    relationship_id: str

    source_symbol_id: str

    target_symbol_id: str

    relationship_type: str

    relationship_direction: str

    confidence: float
```

---

# 📌 Canonical Entity — StructuralEvidence

## Responsabilidade

Representar sinais estruturais explícitos.

---

## Estrutura Conceitual

```python
class StructuralEvidence:

    same_module: bool

    same_parent: bool

    direct_ownership: bool

    import_related: bool

    ownership_distance: int
```

---

# 📌 Canonical Entity — ContextGroup

## Responsabilidade

Representar agrupamento contextual coerente.

---

## Estrutura Conceitual

```python
class ContextGroup:

    context_group_id: str

    root_symbol_id: str

    members: list[str]

    evidence: StructuralEvidence
```

---

# 📌 Canonical Entity — StructuralCandidate

## Responsabilidade

Representar unidade estrutural consumível pelo ranking.

---

## Estrutura Conceitual

```python
class StructuralCandidate:

    symbol_id: str

    chunk_id: str

    vector_score: float

    semantic_score: float

    structural_evidence: StructuralEvidence
```

---

# 📌 Canonical Entity — StructuralQuery

## Responsabilidade

Representar intenção estrutural explícita.

---

## Estrutura Conceitual

```python
class StructuralQuery:

    query_text: str

    intent_type: str

    semantic_concepts: list[str]

    structural_constraints: dict
```

---

# 📌 Canonical Entity — TraversalBoundary

## Responsabilidade

Definir limites explícitos de navegação estrutural.

---

## IMPORTANTE

Mesmo antes do traversal existir oficialmente,

os limites devem existir.

---

## Estrutura Conceitual

```python
class TraversalBoundary:

    max_depth: int

    allowed_relationships: list[str]

    allowed_modules: list[str]

    stop_conditions: list[str]
```

---

# 📌 Mudança Arquitetural Fundamental

## Antes

```text
payloads soltos
```

---

## Depois

```text
runtime estrutural orientado a entidades
```

---

# 📌 IMPORTANTE

Os contratos devem ser:

# independentes do Chroma

---

# 📌 IMPORTANTE

Os contratos devem ser:

# independentes do retriever

---

# 📌 IMPORTANTE

Os contratos devem ser:

# independentes do ranker

---

# 📌 Estratégia Correta

## Retriever

Continua:

```text
candidate orchestration
```

---

## Ranker

Continua:

```text
signal composition
```

---

## Structural Runtime

Passa a operar sobre:

```text
Canonical Structural Entities
```

---

# 📌 Benefícios Arquiteturais

Após esta etapa:

## ✅ contratos explícitos

## ✅ entidades canônicas

## ✅ boundaries formais

## ✅ interoperabilidade estrutural

## ✅ redução de acoplamento procedural

## ✅ base segura para traversal

## ✅ base segura para reasoning futuro

---

# 📌 O que NÃO muda ainda

## ❌ NÃO existe traversal livre

## ❌ NÃO existe graph reasoning

## ❌ NÃO existe multi-hop exploration

## ❌ NÃO existe autonomous expansion

## ❌ NÃO existe recursive traversal

---

# 📌 Estratégia de Integração

## IMPORTANTE

A Structural Contracts Layer NÃO deve quebrar:

* HybridRetriever
* HybridRanker
* ChromaIndexer
* semantic registry
* embedding pipeline

---

# 📌 Estratégia correta

Os contratos nascem:

# paralelos ao runtime atual

---

# 📌 O que isso habilita futuramente

Sem quebrar arquitetura:

* controlled traversal
* architecture reasoning
* contextual expansion
* graph reasoning
* autonomous exploration
* agentic systems

---

# 📌 Próxima Etapa Após Structural Contracts

Depois dos contratos estabilizados:

# Structural Query Layer

Que será responsável por:

* interpretar intenção estrutural
* definir constraints estruturais
* controlar expansão futura
* preparar traversal seguro

---

# 📌 Resultado Esperado

Ao final desta etapa o CODE-RAG deixa oficialmente de operar sobre:

# payloads procedurais dispersos

E passa a operar sobre:

# entidades estruturais canônicas

Esse é o verdadeiro nascimento do:

# Structural Runtime Engine
