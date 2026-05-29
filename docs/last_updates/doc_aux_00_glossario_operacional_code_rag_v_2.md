# 📘 DOC 00 — GLOSSÁRIO OPERACIONAL (CODE-RAG V2)

## 🎯 Objetivo
Definir com precisão todos os conceitos estruturais, semânticos e arquiteturais do sistema CODE-RAG V2, eliminando ambiguidades entre camadas.

---

# 🧠 1. ENTIDADES FUNDAMENTAIS

## SYMBOL
Entidade semântica extraída diretamente do código-fonte.

### Origem
- SymbolExtractor
- SymbolCoreV2

### Características
- Representa unidades lógicas do código (classes, funções, métodos)
- Contém metadados estruturais e semânticos

### Campos
- symbol_id
- symbol_path
- name
- symbol_type
- module_name
- file_path
- parent_symbol_id
- calls
- imports
- metadata

### Propriedades
✔ Semântico
✔ Derivado do AST
❌ Não é estrutura de grafo
❌ Não é persistência final

---

## NODE
Representação estrutural de um elemento no grafo.

### Origem
- GraphBuilderV2
- GraphRepositoryPostgresV2

### Campos
- id
- type
- name
- canonical
- metadata

### Propriedades
✔ Estrutural
✔ Persistido no Postgres (migration_v2.nodes)
❌ Não contém semântica completa

---

## RELATIONSHIP
Relação semântica inferida entre Symbols.

### Origem
- RelationshipCoreV2

### Campos
- relationship_id
- source_symbol_id
- target_symbol_id
- relationship_type
- confidence
- metadata

### Propriedades
✔ Semântico
✔ Enriquecido por resolução
❌ Não é Edge final

---

## EDGE
Relação estrutural no grafo.

### Origem
- GraphBuilderV2

### Campos
- id
- source
- target
- type
- layer
- status
- confidence

### Propriedades
✔ Estrutural
✔ Persistido no Postgres (migration_v2.edges)
❌ Sem enriquecimento semântico completo

---

## IDENTITY
Identificador canônico global de entidades no sistema.

### Origem
- IdentityRegistryV2

### Características
- Resolve referências entre camadas
- Mantém indexação em memória

### Propriedades
✔ Canonical resolution
❌ Não persistido
❌ Não é grafo

---

## CANONICAL
Chave lógica única de identidade de um símbolo ou nó.

### Exemplo
pipeline_v2.core.symbol.symbol_core.SymbolCoreV2

---

## GRAPH CORE
Estrutura em memória do grafo em execução.

### Origem
- GraphBuilderV2

### Contém
- nodes
- edges
- edges_by_source

---

## GRAPH STORE (POSTGRES)
Persistência final do grafo.

### Schemas
- migration_v2.nodes
- migration_v2.edges

---

# 🔗 2. RELAÇÕES ENTRE ENTIDADES

SYMBOL → RELATIONSHIP → EDGE → POSTGRES

SYMBOL → NODE → POSTGRES

IDENTITY ↔ SYMBOL
IDENTITY ↔ NODE

---

# ⚠️ 3. AMBIGUIDADES

- Symbol ≠ Node
- Relationship ≠ Edge
- Identity não persistido
- Graph runtime ≠ Graph storage

---

# 📌 4. REGRAS ATUAIS

- IdentityRegistry é autoridade de resolução
- RelationshipCore é autoridade semântica
- GraphBuilder é autoridade estrutural
- Postgres é persistência final

