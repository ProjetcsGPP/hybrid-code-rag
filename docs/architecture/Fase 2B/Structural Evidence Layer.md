# CODE-RAG — Structural Evidence Layer (FASE 2B)

# 📌 Objetivo

Após a formalização de:

* Symbol Model
* Relationship Model
* Relationship Extraction Layer
* Structural Persistence Layer

O próximo passo correto da FASE 2B é:

# introduzir evidência estrutural explícita

---

# 📌 Objetivo Real da Etapa

O objetivo NÃO é implementar traversal.

O objetivo NÃO é criar graph reasoning.

O objetivo NÃO é criar context assembly.

O objetivo desta etapa é:

# permitir que estrutura influencie retrieval e ranking

SEM heurística procedural.

---

# 📌 Problema Arquitetural Atual

Hoje o sistema possui:

```python
structural_score
```

Mas NÃO possui:

```text
Structural Evidence explícita
```

Isso gera:

* heurística lexical
* pseudoestrutura
* ranking procedural
* inferência distribuída
* structural guessing

---

# 📌 Principal Problema Atual

Hoje:

```python
if "validate" in name:
```

é usado como:

```text
sinal estrutural
```

Mas isso NÃO é estrutura.

Isso é:

# heurística lexical

---

# 📌 Nova Direção Arquitetural

A arquitetura correta começa a evoluir para:

```text
Vector Retrieval
    ↓
Structural Evidence
    ↓
Hybrid Ranking
```

---

# 📌 O que é Structural Evidence

Structural Evidence representa:

# evidências estruturais explícitas e determinísticas

Extraídas de:

* ownership
* namespace
* relationships
* module boundaries
* imports
* hierarchy

---

# 📌 IMPORTANTE

Structural Evidence NÃO é traversal.

Structural Evidence NÃO é graph reasoning.

Structural Evidence NÃO é context expansion.

---

# 📌 Papel da Structural Evidence Layer

A Structural Evidence Layer é responsável apenas por:

# transformar relações estruturais em sinais consumíveis

---

# 📌 Responsabilidades

## ✅ Gerar evidência estrutural explícita

## ✅ Produzir sinais determinísticos

## ✅ Preservar separação arquitetural

## ✅ Permitir ranking estrutural futuro

## ✅ Permitir retrieval híbrido evolutivo

---

# 📌 NÃO é responsabilidade da camada

## ❌ navegar grafo livremente

## ❌ expandir contexto arbitrariamente

## ❌ montar contexto final

## ❌ inferir semântica complexa

## ❌ executar traversal multi-hop

## ❌ realizar graph reasoning

---

# 📌 Problema Arquitetural Resolvido

Antes:

```text
ranker infere estrutura
```

---

Depois:

```text
ranker consome evidência estrutural explícita
```

---

# 📌 Mudança Arquitetural Fundamental

## ERRADO

```python
if "save" in name:
```

---

## CORRETO

```text
BELONGS_TO
IMPORTS
DEFINES
```

transformados em:

```text
Structural Evidence
```

---

# 📌 Estrutura Conceitual

## Módulo sugerido

```text
pipeline/structure/
    structural_evidence.py
```

---

# 📌 Papel do structural_evidence.py

Responsável por:

```text
Relationships → Structural Signals
```

---

# 📌 Conceito Central

## Relações NÃO geram score diretamente

Elas primeiro geram:

# evidência estrutural explícita

---

# 📌 Exemplo Conceitual

## Relationships

```text
save_user
    BELONGS_TO
UserService
```

```text
users.service
    IMPORTS
users.validators
```

---

## Structural Evidence

```text
same_module = True
same_parent = True
ownership_distance = 1
imports_related_module = True
```

---

# 📌 O que muda no ranking

Antes:

```text
heurística procedural
```

---

Depois:

```text
evidência estrutural explícita
```

---

# 📌 Structural Evidence Types — FASE 2B Inicial

Nesta fase apenas sinais simples e determinísticos.

---

# 📌 1. SAME_MODULE

## Objetivo

Identificar símbolos no mesmo módulo.

---

## Exemplo

```text
users.service.save_user
users.service.validate_user
```

---

# 📌 2. SAME_PARENT

## Objetivo

Identificar ownership compartilhado.

---

## Exemplo

```text
UserService.save_user
UserService.validate_user
```

---

# 📌 3. DIRECT_OWNERSHIP

## Objetivo

Representar relação direta BELONGS_TO.

---

## Exemplo

```text
save_user
    pertence a
UserService
```

---

# 📌 4. IMPORT_RELATED

## Objetivo

Detectar dependência estrutural explícita.

---

## Exemplo

```text
users.service
    IMPORTS
users.validators
```

---

# 📌 IMPORTANTE

Nesta fase NÃO implementar:

## ❌ traversal depth

## ❌ graph distance complexo

## ❌ multi-hop evidence

## ❌ dependency chains

## ❌ graph centrality

## ❌ graph algorithms

## ❌ semantic propagation

---

# 📌 Por que começar pequeno

O objetivo atual NÃO é:

# inteligência estrutural máxima

O objetivo é:

# substituir heurística por estrutura explícita

---

# 📌 Fluxo Conceitual Atualizado

```text
Query
    ↓
Intent Detection
    ↓
Vector Retrieval
    ↓
Structural Evidence
    ↓
Hybrid Ranking
```

---

# 📌 Estratégia Correta

## IMPORTANTE

Structural Evidence deve existir:

# separada do ranker

---

# 📌 Papel do Ranker Futuramente

O ranker deve apenas:

## consumir sinais

E NÃO:

## inferir estrutura

---

# 📌 Exemplo Conceitual Futuro

## Entrada do ranker

```python
{
    "vector_score": 0.88,
    "semantic_score": 0.74,

    "structural_evidence": {
        "same_module": True,
        "same_parent": True,
        "ownership_distance": 1,
    }
}
```

---

# 📌 Benefícios Arquiteturais

Após esta etapa:

## ✅ fim da pseudoestrutura lexical

## ✅ fim do structural_score heurístico

## ✅ estrutura explícita consumível

## ✅ ranking desacoplado de inferência estrutural

## ✅ base para traversal futuro

## ✅ base para context assembly futuro

---

# 📌 O que NÃO muda ainda

## ❌ NÃO existe traversal livre

## ❌ NÃO existe graph reasoning

## ❌ NÃO existe neighborhood expansion

## ❌ NÃO existe context assembly

## ❌ NÃO existe multi-hop exploration

---

# 📌 Estratégia de Integração

## IMPORTANTE

A Structural Evidence Layer NÃO deve quebrar:

* HybridRetriever
* HybridRanker
* ChromaIndexer
* semantic registry
* embedding pipeline

---

# 📌 Estratégia correta

A camada nasce:

# paralela ao ranking atual

---

# 📌 Evolução Correta do Ranker

## Hoje

```text
ranker infere estrutura
```

---

## Futuro correto

```text
ranker recebe estrutura explicitamente
```

---

# 📌 O que isso habilita futuramente

Sem quebrar a arquitetura:

* contextual ranking
* ownership-aware ranking
* module-aware retrieval
* graph traversal futuro
* contextual assembly futuro
* architecture reasoning futuro

---

# 📌 Próxima Etapa Após Structural Evidence

Depois da Structural Evidence Layer estabilizada:

# Context Assembly Foundations

AINDA sem traversal livre.

---

# 📌 Resultado Esperado

Ao final desta etapa o CODE-RAG deixa oficialmente de depender de:

# pseudoestrutura heurística

E começa a operar sobre:

# estrutura explicitamente modelada

Esse é o verdadeiro início da:

# Structural Intelligence Runtime
