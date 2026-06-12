# DOC-A — CONSTITUIÇÃO ARQUITETURAL OFICIAL DO CODE-RAG

Status: ATIVO

Prioridade: MÁXIMA

Leitura Obrigatória: SIM

Objetivo:

Consolidar todas as decisões arquiteturais permanentes do projeto CODE-RAG.

Este documento possui precedência sobre qualquer documento operacional.

Nenhuma proposta futura poderá contrariar este documento sem evidência técnica obtida a partir do código real.

---

# 1. MISSÃO DO PROJETO

O CODE-RAG NÃO é:

* indexador de código;
* parser AST;
* mecanismo de embeddings;
* RAG tradicional;
* grafo estático.

O CODE-RAG é:

um motor universal de indexação semântica persistida orientado a grafos, incremental, runtime-aware, multi-framework, multi-linguagem e multi-projeto.

---

# 2. VISÃO FINAL

Objetivo final:

* Semantic Graph Engine Universal
* Runtime-Aware Graph Engine
* Incremental Semantic Indexing Engine
* Multi-Language Semantic Engine
* Framework-Aware Runtime Engine
* Drift-Aware Intelligence Engine
* Persistence-Native Semantic Infrastructure
* Multi-Project Semantic Operating System

---

# 3. PRINCÍPIO FUNDAMENTAL

Persistência é Source Of Truth.

O estado oficial não vive:

* em memória;
* em caches;
* em DTOs;
* em GraphNodeV2;
* em estruturas transitórias.

O estado oficial vive na persistência canônica.

---

# 4. ONTOLOGIA OFICIAL

Symbol

Entidade semântica derivada do código.

Relationship

Relação semântica entre Symbols.

Node

Representação estrutural do grafo.

Edge

Representação estrutural de relacionamento.

Identity

Identificador canônico global.

Canonical

Chave única de identidade.

---

# 5. SEPARAÇÃO OBRIGATÓRIA DE CAMADAS

Symbol ≠ Node

Relationship ≠ Edge

Identity ≠ Node

Identity ≠ Persistência

Graph Runtime ≠ Graph Storage

---

# 6. ARQUITETURA GLOBAL OFICIAL

SOURCE CODE
↓
SEMANTIC LAYER
↓
RESOLUTION LAYER
↓
IDENTITY LAYER
↓
GRAPH LAYER
↓
PERSISTENCE LAYER

---

# 7. PRINCÍPIO DO FLUXO UNIDIRECIONAL

SEMÂNTICA
→ RESOLUÇÃO
→ IDENTIDADE
→ ESTRUTURA
→ PERSISTÊNCIA

É proibido:

* estrutura influenciar semântica;
* identidade influenciar semântica;
* grafo resolver significado.

---

# 8. PAPÉIS OFICIAIS

RelationshipCore

Autoridade semântica.

Identity Service

Gateway de identidade.

Identity Registry

Armazenamento e indexação.

GraphBuilder

Autoridade estrutural.

PostgreSQL

Persistência oficial.

Legacy

Referência comportamental obrigatória.

---

# 9. REGRAS SOBRE O LEGACY

Antes de implementar qualquer funcionalidade nova:

obrigatório verificar:

* como o legacy resolve;
* como o legacy persiste;
* como o legacy propaga contexto;
* como o legacy calcula confiança.

---

# 10. MULTI-PROJECT AWARENESS

Requisito oficial obrigatório.

Todo elemento semântico deve pertencer a um projeto.

Incluindo:

* symbols;
* relationships;
* runtime traces;
* drift events;
* embeddings;
* snapshots;
* semantic states.

---

# 11. PROJECT INTELLIGENCE LAYER

Responsável por:

* linguagem;
* framework;
* runtime;
* ecossistema;
* manifests;
* identidade do projeto.

---

# 12. DRIFT ENGINE

Objetivo final:

detectar:

* orphan calls;
* unresolved symbols;
* runtime mismatch;
* graph inconsistency;
* semantic degradation;
* projection divergence.

---

# 13. PROIBIÇÕES PERMANENTES

Nunca:

* criar identidade paralela;
* criar graph state paralelo;
* criar persistência concorrente;
* inventar ontologias;
* inventar contratos;
* criar abstrações especulativas;
* propor arquitetura sem ler código real.

---

# 14. REGRA DE OURO

O CODE-RAG encontra-se em fase de consolidação.

O objetivo não é perfeição arquitetural.

O objetivo é evolução incremental controlada preservando estabilidade operacional.
