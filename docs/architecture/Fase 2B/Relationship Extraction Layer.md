# CODE-RAG — Relationship Extraction Layer (FASE 2B)

# 📌 Objetivo

Após a formalização de:

* Symbol Model
* Relationship Model

O próximo passo correto da FASE 2B é:

# extração estrutural explícita de relações

---

# 📌 IMPORTANTE

Esta etapa NÃO implementa:

## ❌ traversal

## ❌ graph reasoning

## ❌ context expansion

## ❌ dependency engine avançado

## ❌ multi-hop exploration

## ❌ structural ranking

---

# 📌 Objetivo Real da Etapa

O objetivo é:

# transformar AST em estrutura relacional explícita

---

# 📌 Problema Arquitetural Atual

Hoje o sistema já possui:

```text
parent_chunk_id
imports_context
siblings
symbol_path
ast_hierarchy_path
```

Esses elementos representam relações implícitas.

Mas ainda NÃO existem como:

# entidades relacionais explícitas

---

# 📌 Riscos de NÃO formalizar a extração

Sem uma Relationship Extraction Layer dedicada, o sistema inevitavelmente evolui para:

* traversal procedural
* ranking estrutural heurístico
* metadata graph improvisado
* retriever acoplado à estrutura
* context expansion procedural
* relationship inference espalhada
* graph spaghetti

---

# 📌 Nova Direção Arquitetural

A arquitetura começa a evoluir para:

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

# 📌 Papel da Relationship Extraction Layer

A Relationship Extraction Layer é responsável apenas por:

# detectar relações estruturais explícitas no código

---

# 📌 Responsabilidades

## ✅ Extrair ownership

## ✅ Extrair namespace boundaries

## ✅ Extrair import relationships

## ✅ Gerar entidades Relationship

## ✅ Preservar separação estrutural

---

# 📌 NÃO é responsabilidade da camada

## ❌ navegar estrutura

## ❌ expandir contexto

## ❌ calcular score

## ❌ fazer retrieval

## ❌ inferir semântica complexa

## ❌ montar grafos navegáveis

## ❌ executar traversal

---

# 📌 Estrutura Conceitual Inicial

## Módulo sugerido

```text
pipeline/structure/
    relationship_extractor.py
```

---

# 📌 Papel do relationship_extractor.py

Responsável por:

```text
AST → Relationships
```

---

# 📌 Fluxo Conceitual

```text
ASTChunker
    ↓
Symbol Extraction
    ↓
Relationship Extraction
    ↓
Relationship Store
```

---

# 📌 Relationship Types — FASE 2B Inicial

## SAFE RELATIONSHIPS ONLY

Nesta fase apenas relações estáveis e determinísticas.

---

# 📌 1. BELONGS_TO

## Objetivo

Representar ownership estrutural.

---

## Exemplo

```text
save_user
    BELONGS_TO
UserService
```

---

## Origem AST

Método pertencente a classe.

---

## Benefícios

Permite futuramente:

* ownership traversal
* namespace reasoning
* contextual expansion
* hierarchy exploration

---

# 📌 2. DEFINES

## Objetivo

Representar definição estrutural.

---

## Exemplo

```text
users.service
    DEFINES
UserService
```

---

## Origem AST

Módulo define símbolo.

---

## Benefícios

Permite futuramente:

* module exploration
* namespace navigation
* architecture reasoning

---

# 📌 3. IMPORTS

## Objetivo

Representar dependências explícitas de módulo.

---

## Exemplo

```text
users.service
    IMPORTS
users.validators
```

---

## Origem AST

```python
import x
from x import y
```

---

## IMPORTANTE

Nesta fase:

# IMPORTS é apenas estrutural

Ainda NÃO significa:

* runtime dependency
* execution dependency
* semantic dependency
* call relationship

---

# 📌 O que NÃO implementar ainda

## ❌ CALLS

Porque CALLS exige:

* symbol resolution
* import resolution
* alias resolution
* namespace disambiguation
* inheritance resolution
* dynamic dispatch understanding

---

## ❌ REFERENCES

## ❌ DATA_FLOW

## ❌ CONTROL_FLOW

## ❌ DEPENDS_ON

## ❌ EXECUTES

---

# 📌 Por que começar pequeno

O objetivo da FASE 2B inicial NÃO é inteligência máxima.

O objetivo é:

# fundação estrutural correta

---

# 📌 Modelo Conceitual do Extractor

## Entrada

```python
symbols: list[Symbol]
```

---

## Saída

```python
relationships: list[Relationship]
```

---

# 📌 Exemplo Conceitual

## Symbols

```text
users.UserService
users.UserService.save_user
users.validators.validate_user
```

---

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

# 📌 Estratégia Correta de Integração

## IMPORTANTE

A Relationship Extraction Layer NÃO deve quebrar:

* ASTChunker
* HybridRetriever
* HybridRanker
* ChromaIndexer
* Embedding pipeline

---

# 📌 Estratégia correta

A camada nasce:

# paralela ao pipeline atual

---

# 📌 Evolução incremental segura

## FASE 1

Symbol extraction.

---

## FASE 2

Relationship extraction.

---

## FASE 3

Relationship persistence.

---

## FASE 4

Structural evidence.

---

## FASE 5

Traversal futuramente.

---

# 📌 Persistência Estrutural

## IMPORTANTE

Relationship persistence NÃO deve usar:

```python
metadata["relationships"]
```

Nem:

```python
metadata["neighbors"]
```

Nem:

```python
metadata["imports"]
```

---

# 📌 Separação Arquitetural Obrigatória

## Chroma

Continua:

```text
semantic recall layer
```

---

## Relationship Store

Passa a ser:

```text
structural persistence layer
```

---

# 📌 Persistência Inicial Aceitável

Nesta fase:

* SQLite
* JSONL
* TinyDB
* NetworkX

são suficientes.

---

# 📌 O que muda arquiteturalmente após esta etapa

O sistema deixa de depender de:

# estrutura implícita em metadata

E passa a possuir:

# estrutura explicitamente modelada

---

# 📌 Benefícios Arquiteturais

Após esta etapa o sistema terá:

## ✅ ownership explícito

## ✅ namespace explícito

## ✅ boundaries explícitos

## ✅ dependências explícitas

## ✅ base para traversal futuro

## ✅ base para graph reasoning futuro

## ✅ structural evidence futura

Sem quebrar o retrieval atual.

---

# 📌 Próxima Etapa Após Relationship Extraction

Depois da extração estabilizada:

# Structural Persistence Layer

Responsável por:

* armazenar símbolos
* armazenar relações
* permitir consultas estruturais futuras

AINDA sem traversal complexo.

---

# 📌 Resultado Esperado

Ao final desta etapa o CODE-RAG deixa oficialmente de ser:

```text
RAG baseado em metadata enriquecida
```

E começa a evoluir para:

```text
Structural & Semantic Code Intelligence Engine
```
