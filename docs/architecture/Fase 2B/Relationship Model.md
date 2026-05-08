# CODE-RAG — Relationship Model (FASE 2B)

# 📌 Objetivo

Após a formalização do Symbol Model, o próximo passo correto da FASE 2B é:

# formalizar relações estruturais explícitas

O objetivo NÃO é implementar traversal.

O objetivo NÃO é criar graph reasoning.

O objetivo NÃO é criar context expansion.

O objetivo desta etapa é:

# transformar estrutura implícita em estrutura modelada

---

# 📌 Problema Arquitetural Atual

Hoje o sistema possui relações implícitas espalhadas em metadata:

```text
parent_chunk_id
siblings
imports_context
ast_hierarchy_path
parent_class
```

Esses campos já representam:

* ownership
* namespace
* dependência
* vizinhança estrutural
* hierarquia

Mas tudo ainda existe como:

# metadata procedural

---

# 📌 Risco Atual

Sem Relationship Model explícito, o sistema inevitavelmente evolui para:

* traversal procedural
* ranking heurístico estrutural
* metadata explosion
* graph improvisado
* retrieval acoplado à estrutura
* semântica distribuída
* context expansion procedural

---

# 📌 Nova Direção Arquitetural

A arquitetura começa a evoluir para:

```text
Symbol
    ↓
Relationship
    ↓
Chunk
    ↓
Embedding
```

---

# 📌 Papel do Relationship

Relationship representa:

# conexão estrutural explícita entre símbolos

Exemplos:

```text
UserService
    DEFINES
save_user
```

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

# 📌 Objetivos do Relationship Model

O Relationship Model deve permitir futuramente:

* structural traversal
* neighborhood expansion
* ownership reasoning
* architecture reasoning
* dependency reasoning
* contextual expansion
* graph reasoning
* multi-hop exploration
* structural evidence generation

---

# 📌 Princípios Arquiteturais

## ✅ Relações NÃO devem viver em metadata

Evitar:

```python
metadata["neighbors"]
metadata["calls"]
metadata["references"]
metadata["imports"]
```

Porque isso transforma metadata em:

# graph store improvisado

---

## ✅ Relationship NÃO pertence ao retriever

Retriever continua:

```text
candidate orchestration
```

Retriever NÃO deve:

* navegar estrutura
* expandir contexto
* resolver dependências
* montar grafos

---

## ✅ Relationship NÃO pertence ao ranker

Ranker apenas consome sinais.

Ele NÃO deve inferir relações.

---

## ✅ Relationship NÃO pertence ao Chroma

Chroma continua:

```text
semantic recall layer
```

Relações estruturais devem possuir persistência própria.

---

# 📌 Modelo Conceitual Inicial

## Relationship

### Responsabilidade

Representar uma conexão estrutural explícita entre dois símbolos.

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

    metadata: dict
```

---

# 📌 Campos do Relationship

## relationship_id

### Objetivo

Identidade única da relação.

---

### Exemplo

```text
users.UserService -> BELONGS_TO -> users
```

---

## source_symbol_id

### Objetivo

Símbolo de origem.

---

## target_symbol_id

### Objetivo

Símbolo de destino.

---

## relationship_type

### Objetivo

Tipo estrutural da relação.

---

# 📌 Relationship Types — FASE 2B Inicial

## SAFE RELATIONSHIPS

Somente relações estáveis e previsíveis.

---

## BELONGS_TO

### Exemplo

```text
save_user
    BELONGS_TO
UserService
```

---

## DEFINES

### Exemplo

```text
users.service
    DEFINES
UserService
```

---

## IMPORTS

### Exemplo

```text
users.service
    IMPORTS
users.validators
```

---

# 📌 IMPORTANTE

Nesta fase NÃO implementar:

## ❌ CALLS

## ❌ REFERENCES

## ❌ DATA_FLOW

## ❌ CONTROL_FLOW

## ❌ DEPENDS_ON

## ❌ USES_VARIABLE

## ❌ EXECUTES

---

# 📌 Por que começar simples

Relações de chamada (CALLS) parecem simples.

Mas rapidamente exigem:

* symbol resolution
* import resolution
* alias resolution
* namespace disambiguation
* dynamic dispatch
* inheritance reasoning
* runtime inference

Isso aumenta MUITO a complexidade.

---

# 📌 Estratégia Correta da FASE 2B

Primeiro:

# ownership e boundaries

Depois:

# traversal

Depois:

# dependency reasoning

---

# 📌 relationship_direction

### Objetivo

Definir orientação semântica da relação.

---

### Exemplos

```text
OUTBOUND
INBOUND
BIDIRECTIONAL
```

---

# 📌 confidence

### Objetivo

Permitir inferências futuras graduais.

---

### IMPORTANTE

Mesmo relações AST podem futuramente possuir:

* resolução parcial
* ambiguidade
* inferência híbrida

---

# 📌 metadata

### Objetivo

Extensões futuras controladas.

---

### IMPORTANTE

metadata NÃO deve carregar:

* adjacency lists
* traversal state
* graph neighborhood
* expansion context

---

# 📌 O que deve sair do ChunkMetadata futuramente

## Deve migrar para Relationship Layer

```text
parent_chunk_id
siblings
imports_context
```

---

## Deve permanecer no Symbol

```text
symbol_path
module_name
ownership
```

---

# 📌 Relationship Extraction

A extração de relações deverá acontecer:

# separada do retrieval

---

# 📌 Fluxo Conceitual Futuro

```text
AST
    ↓
Symbol Extraction
    ↓
Relationship Extraction
    ↓
Chunk Generation
    ↓
Embedding Indexing
```

---

# 📌 O que NÃO fazer

## ❌ NÃO usar metadata como graph

## ❌ NÃO expandir contexto no retriever

## ❌ NÃO calcular traversal no ranker

## ❌ NÃO transformar Chroma em relationship store

## ❌ NÃO criar graph db cedo demais

---

# 📌 Estratégia de Persistência Inicial

Nesta fase a persistência estrutural pode ser simples.

Exemplos aceitáveis:

* SQLite
* JSONL
* TinyDB
* NetworkX

---

# 📌 IMPORTANTE

O objetivo atual NÃO é performance extrema.

O objetivo é:

# separação arquitetural correta

---

# 📌 Benefícios Arquiteturais

Após o Relationship Model:

## ✅ estrutura explícita

## ✅ ownership explícito

## ✅ dependências explícitas

## ✅ boundaries estruturais

## ✅ base para traversal futuro

## ✅ structural evidence real

## ✅ graph evolution path

Sem quebrar o pipeline atual.

---

# 📌 Próxima Etapa Após Relationship Model

Depois do Relationship Model estabilizado:

# Relationship Extraction Layer

Inicialmente extraindo apenas:

* BELONGS_TO
* DEFINES
* IMPORTS

A partir do AST.

---

# 📌 Resultado Esperado

Ao final desta etapa o sistema deixará de possuir:

# estrutura implícita distribuída

E passará a possuir:

# estrutura explicitamente modelada

Esse é o verdadeiro início da Structural Intelligence Layer.
