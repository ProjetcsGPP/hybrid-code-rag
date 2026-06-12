ARQUITETURA DA SEMANTIC RECONCILIATION LAYER

Bom dia.

Revisei todo o contexto que construímos desde os DOC-08, DOC-09, DOC-10A, DOC-11, DOC-12, DOC-13 e o estado atual após a execução completa do `project_ingestion_v2`.

Concordo com a direção que você definiu ontem:

* Não alterar a arquitetura central da Fase 2.
* Não reabrir decisões já encerradas.
* Não tentar resolver todos os `UNRESOLVED` durante a ingestão.
* Preservar a autoridade do Identity Registry.
* Implementar posteriormente uma camada especializada para reconciliação semântica global.

O que segue abaixo é exatamente o que eu colocaria no DOC-15.

---

# PARTE 1 — ARQUITETURA DA SEMANTIC RECONCILIATION LAYER

## Objetivo

Adicionar uma etapa pós-ingestão capaz de:

* analisar símbolos não resolvidos;
* correlacionar informações de múltiplos arquivos;
* reclassificar relacionamentos inicialmente marcados como:

  * EXTERNAL
  * UNRESOLVED
  * PARTIAL
* atualizar o grafo sem reconstruí-lo.

---

# Posição na Arquitetura

Hoje:

```text
AST
 ↓
Chunking
 ↓
Symbol Extraction
 ↓
Relationship Extraction
 ↓
Identity Resolution
 ↓
Graph Build
 ↓
Contract Validation
```

Proposto:

```text
AST
 ↓
Chunking
 ↓
Symbol Extraction
 ↓
Relationship Extraction
 ↓
Identity Resolution
 ↓
Graph Build
 ↓
Contract Validation
 ↓
Semantic Reconciliation Layer
 ↓
Graph Enrichment
 ↓
Final Knowledge Graph
```

---

# Componentes

## 1. Unresolved Registry

Novo componente.

Responsável por armazenar:

```python
external::UNRESOLVED::logging.getLogger

external::UNRESOLVED::timezone.now

external::UNRESOLVED::UserAuthzState.objects.get_or_create
```

Formato:

```python
@dataclass
class UnresolvedReference:
    source_id: str
    raw_call: str
    file_path: str
    semantic_context: dict
    confidence: float
```

---

## 2. Semantic Candidate Engine

Recebe:

```python
logging.getLogger
```

e procura candidatos:

```python
import logging
```

em qualquer arquivo.

Produz:

```python
Candidate(
    identity="stdlib.logging.getLogger",
    confidence=0.95
)
```

---

## 3. Cross File Resolver

Responsável por:

```python
UserAuthzState.objects.get_or_create
```

encontrar:

```python
class UserAuthzState(...)
```

em outro arquivo.

---

## 4. Reconciliation Engine

Executa:

```python
UNRESOLVED
     ↓
Candidate Search
     ↓
Ranking
     ↓
Promotion
```

Transformando:

```text
external::UNRESOLVED::UserAuthzState.objects.get_or_create
```

em

```text
STRICT::accounts.models.UserAuthzState
```

---

## 5. Graph Enricher

Atualiza:

```python
relationship.target
```

sem recriar o grafo inteiro.

---

# PARTE 2 — CHECKLIST IMPLEMENTÁVEL

# FASE 3A

## Infraestrutura

### Criar

```text
pipeline_v2/core/reconciliation/
```

---

### Criar

```text
unresolved_registry.py
```

---

### Criar

```text
semantic_candidate_engine.py
```

---

### Criar

```text
cross_file_resolver.py
```

---

### Criar

```text
reconciliation_engine.py
```

---

### Criar

```text
graph_enricher.py
```

---

# FASE 3B

## RelationshipCore

Adicionar:

```python
self.unresolved_registry.register(...)
```

quando ocorrer:

```python
external::UNRESOLVED
```

---

Não alterar:

```python
IdentityRegistry
```

---

Não alterar:

```python
GraphCore
```

---

# FASE 3C

## Candidate Ranking

Implementar ranking:

### Peso 1

Mesmo arquivo

---

### Peso 2

Mesmo módulo

---

### Peso 3

Mesmo pacote

---

### Peso 4

Mesmo namespace

---

### Peso 5

Match semântico

---

# FASE 3D

## Promotion

Converter:

```text
EXTERNAL
```

para:

```text
STRICT
```

somente quando:

```python
confidence >= 0.90
```

---

# FASE 3E

## Auditoria

Criar:

```python
SemanticReconciliationReport
```

com:

```python
resolved_count
unresolved_count
promoted_count
confidence_distribution
```

---

# PARTE 3 — DOC-15 (FORMAL)

# DOC-15

## ESPECIFICAÇÃO DA FASE 3

## SEMANTIC RECONCILIATION LAYER

---

### Status

PROPOSTA APROVADA

---

### Dependência

DOC-08

DOC-09

DOC-10A

DOC-11

DOC-12

DOC-13

DOC-14

---

### Objetivo

Adicionar resolução semântica global pós-processamento sem comprometer:

* Identity Registry
* Relationship Layer
* Graph Layer

---

### Princípios Arquiteturais

#### Princípio 1

Identity continua sendo autoridade única.

---

#### Princípio 2

Relationship continua produzindo resolução local.

---

#### Princípio 3

Semantic Reconciliation nunca participa da ingestão.

---

#### Princípio 4

Semantic Reconciliation opera apenas após:

```text
Contract Validation
```

---

#### Princípio 5

Nenhuma decisão tomada pela Identity Layer pode ser sobrescrita.

Somente:

```text
UNRESOLVED
```

ou

```text
EXTERNAL
```

podem ser promovidos.

---

### Escopo

Resolver:

* imports tardios
* símbolos distribuídos
* referências cross-file
* referências cross-module
* chamadas framework
* chamadas stdlib

---

### Fora do Escopo

Não resolver:

* código dinâmico arbitrário
* eval()
* exec()
* monkey patching
* reflection extrema

---

### Critério de Aceitação

Projeto Django de teste:

Resultado atual:

```text
3732 nodes
4942 relationships
```

Meta da Fase 3:

Reduzir significativamente:

```text
external::UNRESOLVED::*
```

sem gerar:

```text
identity drift
```

---

# ESTADO OFICIAL PARA O PRÓXIMO CHAT

O CODE-RAG V2 encontra-se em:

```text
FASE 2 CONCLUÍDA
```

com:

```text
Pipeline operacional
Identity estável
Graph estável
Contracts aprovados
```

Próxima etapa autorizada:

```text
FASE 3
Semantic Reconciliation Layer
```

sem alteração das decisões arquiteturais já consolidadas nos documentos anteriores.
