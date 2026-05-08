# CODE-RAG — Context Assembly Foundations (FASE 2B)

# 📌 Objetivo

Após a formalização de:

* Symbol Model
* Relationship Model
* Relationship Extraction Layer
* Structural Persistence Layer
* Structural Evidence Layer

O próximo passo correto da FASE 2B é:

# preparar montagem contextual estrutural controlada

---

# 📌 IMPORTANTE

Esta etapa NÃO implementa:

## ❌ traversal livre

## ❌ graph reasoning completo

## ❌ multi-hop exploration

## ❌ autonomous exploration

## ❌ agentic retrieval

## ❌ context expansion arbitrário

---

# 📌 Objetivo Real da Etapa

O objetivo NÃO é montar contextos gigantes.

O objetivo NÃO é navegar dependências livremente.

O objetivo desta etapa é:

# criar a fundação arquitetural da composição contextual

---

# 📌 Problema Arquitetural Atual

Hoje o sistema retorna:

```text
chunks ranqueados individualmente
```

Mesmo quando estruturalmente relacionados.

Isso limita:

* entendimento contextual
* coerência estrutural
* compreensão multi-entidade
* reasoning arquitetural
* continuidade semântica

---

# 📌 Principal Problema Atual

Hoje:

```text
resultado = chunk isolado
```

Mas código real funciona como:

```text
estrutura conectada
```

---

# 📌 Nova Direção Arquitetural

A arquitetura correta começa a evoluir para:

```text
Query
    ↓
Candidate Retrieval
    ↓
Structural Evidence
    ↓
Context Assembly
    ↓
Hybrid Ranking
```

---

# 📌 O que é Context Assembly

Context Assembly representa:

# composição contextual controlada baseada em estrutura explícita

---

# 📌 IMPORTANTE

Context Assembly NÃO é traversal livre.

Context Assembly NÃO é graph crawling.

Context Assembly NÃO é neighborhood explosion.

---

# 📌 Papel da Context Assembly Layer

A Context Assembly Layer é responsável apenas por:

# compor contexto estruturalmente coerente

A partir de:

* candidates recuperados
* evidência estrutural
* ownership
* boundaries
* relações explícitas

---

# 📌 Responsabilidades

## ✅ Agrupar símbolos relacionados

## ✅ Preservar boundaries estruturais

## ✅ Produzir contexto coerente

## ✅ Evitar contexto órfão

## ✅ Preparar reasoning futuro

---

# 📌 NÃO é responsabilidade da camada

## ❌ traversal profundo

## ❌ graph search livre

## ❌ dependency recursion

## ❌ multi-hop expansion

## ❌ graph ranking

## ❌ semantic propagation

## ❌ autonomous exploration

---

# 📌 Mudança Arquitetural Fundamental

## Antes

```text
ranking de chunks isolados
```

---

## Depois

```text
contextos estruturais compostos
```

---

# 📌 Conceito Central

## Retrieval encontra candidatos

## Structure organiza contexto

---

# 📌 Estrutura Conceitual

## Módulo sugerido

```text
pipeline/context/
    context_assembler.py
```

---

# 📌 Papel do context_assembler.py

Responsável por:

```text
Candidates + Structural Evidence → Context Groups
```

---

# 📌 Conceito Inicial de Context Group

## Context Group

Representa:

# conjunto estruturalmente coerente de símbolos/chunks

---

# 📌 Exemplo Conceitual

## Candidates recuperados

```text
UserService.save_user
UserService.validate_user
UserRepository.insert_user
```

---

## Structural Evidence

```text
save_user
    BELONGS_TO
UserService

validate_user
    BELONGS_TO
UserService
```

---

## Context Group gerado

```text
Context Group:
    UserService
        - save_user
        - validate_user
```

---

# 📌 Objetivo do Context Group

Permitir futuramente:

* contextual reasoning
* architecture reasoning
* multi-entity understanding
* contextual prompting
* agentic exploration

---

# 📌 Context Assembly Types — FASE 2B Inicial

Nesta fase apenas agrupamentos simples e determinísticos.

---

# 📌 1. SAME_PARENT_GROUP

## Objetivo

Agrupar símbolos com mesmo owner.

---

## Exemplo

```text
UserService.save_user
UserService.validate_user
```

---

# 📌 2. SAME_MODULE_GROUP

## Objetivo

Agrupar símbolos do mesmo módulo.

---

## Exemplo

```text
users.service.*
```

---

# 📌 3. DIRECT_IMPORT_GROUP

## Objetivo

Agrupar módulos diretamente relacionados.

---

## Exemplo

```text
users.service
↔
users.validators
```

---

# 📌 IMPORTANTE

Nesta fase NÃO implementar:

## ❌ recursive expansion

## ❌ neighborhood explosion

## ❌ graph depth search

## ❌ dynamic context growth

## ❌ automatic dependency traversal

## ❌ relevance propagation

---

# 📌 Por que começar pequeno

O objetivo atual NÃO é:

# contexto infinito

O objetivo é:

# contexto estruturalmente coerente

---

# 📌 Estratégia Correta

## IMPORTANTE

Context Assembly deve existir:

# separada do retriever

E:

# separada do ranker

---

# 📌 Papel do Retriever

Retriever continua:

```text
candidate generation
```

---

# 📌 Papel do Ranker

Ranker continua:

```text
signal composition
```

---

# 📌 Papel do Context Assembler

Context Assembler passa a ser:

```text
context composition layer
```

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
Context Assembly
    ↓
Hybrid Ranking
```

---

# 📌 Exemplo Conceitual Futuro

## Entrada

```python
candidates = [
    save_user,
    validate_user,
    insert_user,
]
```

---

## Structural Evidence

```python
{
    "same_parent": True,
    "same_module": True,
}
```

---

## Saída

```python
ContextGroup(
    root_symbol="UserService",
    members=[
        save_user,
        validate_user,
    ]
)
```

---

# 📌 Benefícios Arquiteturais

Após esta etapa:

## ✅ contexto estrutural coerente

## ✅ agrupamento explícito

## ✅ fim do contexto isolado

## ✅ base para contextual reasoning

## ✅ base para architecture reasoning

## ✅ base para traversal futuro

## ✅ base para agentic retrieval futuro

---

# 📌 O que NÃO muda ainda

## ❌ NÃO existe traversal livre

## ❌ NÃO existe graph reasoning completo

## ❌ NÃO existe dependency recursion

## ❌ NÃO existe autonomous exploration

## ❌ NÃO existe multi-hop expansion

---

# 📌 Estratégia de Integração

## IMPORTANTE

A Context Assembly Layer NÃO deve quebrar:

* HybridRetriever
* HybridRanker
* ChromaIndexer
* semantic registry
* embedding pipeline

---

# 📌 Estratégia correta

A camada nasce:

# paralela ao retrieval atual

---

# 📌 O que isso habilita futuramente

Sem quebrar arquitetura:

* contextual prompting
* contextual retrieval
* architecture-aware ranking
* traversal futuro
* graph reasoning futuro
* autonomous exploration futura

---

# 📌 Próxima Etapa Após Context Assembly Foundations

Depois da Context Assembly estabilizada:

# Controlled Structural Traversal

AINDA com:

* limites explícitos
* profundidade controlada
* boundaries rígidos
* expansão segura

---

# 📌 Resultado Esperado

Ao final desta etapa o CODE-RAG deixa oficialmente de operar apenas sobre:

# chunks independentes

E começa a operar sobre:

# contextos estruturais compostos

Esse é o verdadeiro nascimento da:

# Contextual Structural Intelligence
