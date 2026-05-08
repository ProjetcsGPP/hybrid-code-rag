# CODE-RAG — Structural Persistence Layer (FASE 2B)

# 📌 Objetivo

Após a formalização de:

* Symbol Model
* Relationship Model
* Relationship Extraction Layer

O próximo passo correto da FASE 2B é:

# persistência estrutural explícita

---

# 📌 Objetivo Real da Etapa

O objetivo NÃO é criar um graph database completo.

O objetivo NÃO é implementar traversal avançado.

O objetivo NÃO é criar graph reasoning.

O objetivo desta etapa é:

# separar persistência estrutural da persistência vetorial

---

# 📌 Problema Arquitetural Atual

Hoje o sistema depende fortemente de:

```text
metadata enriquecida
```

persistida junto do retrieval vetorial.

Isso é aceitável nas fases iniciais.

Mas torna-se perigoso quando surgem:

* relações explícitas
* ownership
* structural evidence
* neighborhood reasoning
* traversal futuro
* dependency exploration

---

# 📌 Principal Risco Atual

Sem uma Structural Persistence Layer separada, o sistema inevitavelmente evolui para:

* Chroma Frankenstein
* metadata graph improvisado
* traversal procedural
* ranking estrutural acoplado
* expansion procedural
* graph spaghetti

---

# 📌 Separação Arquitetural Obrigatória

A arquitetura correta começa a evoluir para:

```text
Semantic Layer
    ↓
Vector Store (Chroma)

Structural Layer
    ↓
Relationship Store
```

---

# 📌 Responsabilidade do Chroma

Chroma continua responsável apenas por:

## ✅ embeddings

## ✅ vector similarity

## ✅ semantic recall

## ✅ candidate generation

---

# 📌 O que NÃO pertence ao Chroma

## ❌ traversal

## ❌ graph persistence

## ❌ relationship navigation

## ❌ adjacency queries

## ❌ ownership graph

## ❌ dependency graph

## ❌ neighborhood expansion

---

# 📌 Papel da Structural Persistence Layer

A Structural Persistence Layer é responsável por:

# persistir entidades estruturais explicitamente

---

# 📌 Responsabilidades

## ✅ Persistir Symbols

## ✅ Persistir Relationships

## ✅ Permitir consultas estruturais simples

## ✅ Preservar ownership

## ✅ Preservar namespace boundaries

## ✅ Preservar import relationships

---

# 📌 NÃO é responsabilidade da camada

## ❌ traversal complexo

## ❌ graph ranking

## ❌ context assembly

## ❌ semantic inference

## ❌ retrieval vetorial

## ❌ ranking híbrido

---

# 📌 Nova Estrutura Conceitual

## Módulo sugerido

```text
pipeline/structure/
    symbol_store.py
    relationship_store.py
```

---

# 📌 Papel do symbol_store.py

Responsável por:

```text
persistência de símbolos
```

---

# 📌 Papel do relationship_store.py

Responsável por:

```text
persistência de relações
```

---

# 📌 Estratégia Correta da FASE 2B

## IMPORTANTE

Nesta fase:

# simplicidade > complexidade

O objetivo NÃO é performance extrema.

O objetivo é:

# separação arquitetural correta

---

# 📌 Persistência Inicial Aceitável

Nesta etapa soluções simples são suficientes.

---

## SQLite

### Excelente opção inicial

Porque oferece:

* persistência real
* consultas relacionais
* simplicidade operacional
* baixo acoplamento
* fácil debug
* fácil migração futura

---

## JSONL

Aceitável apenas para protótipo.

Mas tende a limitar:

* queries
* relacionamento
* consistência
* escalabilidade

---

## TinyDB

Aceitável para experimentação.

Mas pode limitar evolução futura.

---

## NetworkX

Útil para:

* prototipar traversal
* explorar grafos
* validar modelos estruturais

Mas NÃO deve virar persistência principal.

---

# 📌 Recomendação Atual

## Melhor equilíbrio arquitetural:

# SQLite

---

# 📌 Estrutura Conceitual Inicial

## Symbols Table

```text
symbols
```

---

## Campos conceituais

```text
symbol_id
symbol_path
symbol_name
symbol_type
module_name
file_path
parent_symbol_id
semantic_type
start_line
end_line
```

---

# 📌 Relationships Table

```text
relationships
```

---

## Campos conceituais

```text
relationship_id
source_symbol_id
target_symbol_id
relationship_type
relationship_direction
confidence
```

---

# 📌 IMPORTANTE

Nesta fase NÃO implementar:

## ❌ graph indexes complexos

## ❌ graph engine

## ❌ graph algorithms

## ❌ traversal cache

## ❌ adjacency cache

## ❌ neighborhood expansion

## ❌ dependency expansion

---

# 📌 Objetivo Atual

Somente:

# persistência estrutural explícita

---

# 📌 Estratégia de Integração

## IMPORTANTE

A Structural Persistence Layer NÃO deve quebrar:

* ASTChunker
* HybridRetriever
* HybridRanker
* ChromaIndexer
* semantic registry
* embedding pipeline

---

# 📌 Estratégia correta

A camada nasce:

# paralela ao pipeline atual

---

# 📌 Fluxo Conceitual Atualizado

```text
AST
    ↓
Symbol Extraction
    ↓
Relationship Extraction
    ↓
Structural Persistence
    ↓
Chunk Generation
    ↓
Embedding Indexing
```

---

# 📌 O que muda arquiteturalmente

Antes:

```text
metadata enriquecida
```

---

Depois:

```text
estrutura explicitamente persistida
```

---

# 📌 Benefícios Arquiteturais

Após esta etapa o sistema terá:

## ✅ separação entre retrieval e estrutura

## ✅ ownership persistido

## ✅ namespace persistido

## ✅ relações persistidas

## ✅ base para traversal futuro

## ✅ base para structural evidence

## ✅ base para context assembly futuro

---

# 📌 Structural Evidence — Próxima Evolução

Após a persistência estrutural estabilizada:

# Structural Evidence Layer

Essa será a primeira etapa onde:

```text
estrutura começa a influenciar retrieval e ranking
```

Mas:

## IMPORTANTÍSSIMO

O ranker NÃO deve inferir estrutura.

Ele apenas consumirá:

```text
structural evidence explícita
```

---

# 📌 O que isso habilita futuramente

Sem quebrar a arquitetura atual:

* ownership traversal
* neighborhood exploration
* contextual expansion
* architecture reasoning
* dependency reasoning
* graph traversal
* agentic retrieval

---

# 📌 Resultado Esperado

Ao final desta etapa o CODE-RAG deixa oficialmente de depender de:

# metadata estrutural improvisada

E passa a possuir:

# backbone estrut
