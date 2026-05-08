# CODE-RAG — Symbol Model (FASE 2B)

## 📌 Objetivo

O objetivo desta etapa NÃO é implementar traversal, graph reasoning ou context assembly.

O objetivo é:

# formalizar a identidade estrutural do sistema

A partir deste ponto:

* Chunk deixa de ser a entidade central
* Symbol passa a ser a entidade estrutural central
* Chunk vira representação indexável do símbolo
* Relações passam a ser explícitas

---

# 📌 Problema Arquitetural Atual

Hoje o sistema possui:

* chunk_id
* symbol_path
* parent_chunk_id
* module_name
* ast_hierarchy_path

Isso já representa:

* identidade
* ownership
* namespace
* lineage

Mas tudo ainda está:

# acoplado ao chunk

Isso cria problemas futuros:

* múltiplos chunks para o mesmo símbolo
* traversal procedural
* metadata explosion
* estrutura implícita
* graph improvisado
* retrieval acoplado à estrutura

---

# 📌 Nova Direção Arquitetural

A arquitetura começa a evoluir para:

```text
Symbol
    ↓
Relationship
    ↓
Chunk(s)
    ↓
Embeddings
```

E NÃO mais:

```text
Chunk
    contém tudo
```

---

# 📌 Papel do Symbol

O Symbol representa:

# uma entidade estrutural canônica do código

Exemplos:

* módulo
* classe
* função
* método
* futuramente:

  * atributo
  * interface
  * enum
  * decorator
  * endpoint
  * query
  * event

---

# 📌 Objetivos do Symbol

O Symbol deve permitir futuramente:

* namespace reasoning
* ownership reasoning
* graph traversal
* dependency expansion
* architecture reasoning
* contextual assembly
* semantic navigation
* multi-hop traversal
* agentic exploration

---

# 📌 Princípios Arquiteturais

## ✅ Symbol NÃO é chunk

Um símbolo pode possuir:

* múltiplos chunks
* múltiplos embeddings
* múltiplas representações
* múltiplos contextos

---

## ✅ Symbol NÃO pertence ao retrieval

O Symbol é estrutural.

O retrieval apenas recupera representações indexáveis.

---

## ✅ Symbol NÃO pertence ao ranker

O ranker apenas consome sinais.

Ele NÃO deve inferir estrutura.

---

## ✅ Symbol NÃO depende do Chroma

Chroma continua:

```text
semantic recall layer
```

O Symbol deve existir independentemente do banco vetorial.

---

# 📌 Modelo Conceitual Inicial

## Symbol

### Responsabilidade

Representar uma entidade estrutural única do sistema.

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

    start_line: int
    end_line: int

    decorators: list[str]

    semantic_type: str

    metadata: dict
```

---

# 📌 Campos do Symbol

## symbol_id

### Objetivo

Identidade estrutural estável.

---

### IMPORTANTE

O symbol_id NÃO deve depender do chunk.

Porque futuramente:

* um símbolo poderá possuir vários chunks
* vários embeddings
* várias representações derivadas

---

### Exemplo

```text
users.UserService.save_user
```

---

## symbol_path

### Objetivo

Namespace estrutural legível.

---

### Exemplo

```text
users.UserService.save_user
```

---

## symbol_name

### Objetivo

Nome simples do símbolo.

---

### Exemplo

```text
save_user
```

---

## symbol_type

### Objetivo

Tipo estrutural do símbolo.

---

### Valores iniciais

```text
module
class
function
method
```

---

### Futuramente

```text
attribute
interface
enum
endpoint
query
event
schema
```

---

## module_name

### Objetivo

Boundary estrutural do símbolo.

---

## file_path

### Objetivo

Localização física do símbolo.

---

## parent_symbol_id

### Objetivo

Ownership estrutural.

---

### Exemplo

```text
UserService.save_user
    pertence a
UserService
```

---

### IMPORTANTE

Isso NÃO é traversal.

É apenas:

# representação explícita de ownership

---

## start_line / end_line

### Objetivo

Mapeamento estrutural para código-fonte.

---

## decorators

### Objetivo

Preservar semântica estrutural relevante.

---

## semantic_type

### Objetivo

Bootstrap semântico inicial.

---

### IMPORTANTE

semantic_type ainda pode existir nesta fase.

Mas futuramente deverá migrar para:

```text
Semantic Layer explícita
```

---

## metadata

### Objetivo

Reservado para extensões futuras.

---

### IMPORTANTE

NÃO usar metadata para:

* graph traversal
* dependency persistence
* relationship expansion
* adjacency
* neighborhood

---

# 📌 O que deve sair do ChunkMetadata futuramente

## Deve migrar para Symbol

```text
symbol_path
module_name
parent_chunk_id
parent_class
ast_hierarchy_path
```

---

## Deve permanecer no Chunk

```text
embedding
vector similarity
retrieval metadata
```

---

# 📌 Nova Relação Conceitual

## Hoje

```text
Chunk
    contém:
        identidade
        estrutura
        retrieval
        ranking
```

---

## Futuro correto

```text
Symbol
    ↓
Chunk
    ↓
Embedding
```

---

# 📌 O que NÃO implementar ainda

## ❌ traversal

## ❌ graph database

## ❌ context expansion

## ❌ dependency engine

## ❌ relationship scoring

## ❌ graph ranking

## ❌ multi-hop reasoning

---

# 📌 Objetivo da FASE 2B Inicial

Somente:

# formalizar identidade estrutural explícita

---

# 📌 Próxima Etapa Após Symbol

Depois do Symbol Model estabilizado:

# Relationship Model

Inicialmente apenas:

* BELONGS_TO
* DEFINES
* IMPORTS

Sem traversal ainda.

---

# 📌 Estratégia de Migração

## IMPORTANTE

A introdução do Symbol NÃO deve quebrar:

* HybridRetriever
* HybridRanker
* Chroma Indexer
* semantic registry
* embeddings
* retrieval pipeline

---

# 📌 Estratégia Correta

O Symbol nasce:

# em paralelo ao pipeline atual

---

# 📌 Fluxo Arquitetural Temporário

```text
ASTChunker
    ↓
Symbol Extraction
    ↓
Chunk Generation
    ↓
Embedding Indexing
```

---

# 📌 Resultado Esperado

Ao final desta etapa o sistema terá:

## ✅ identidade estrutural explícita

## ✅ separação entre símbolo e chunk

## ✅ ownership model

## ✅ namespace model

## ✅ base para relationship extraction

## ✅ base para traversal futuro

## ✅ base para graph reasoning futuro

Sem quebrar o retrieval atual.
