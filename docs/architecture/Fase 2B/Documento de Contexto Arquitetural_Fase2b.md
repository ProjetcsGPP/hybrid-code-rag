# CODE-RAG — Documento de Contexto Arquitetural

## Estado Atual, Análise Estrutural e Diretrizes para Evolução da FASE 2B+

Data de referência: Maio/2026

---

# 1. OBJETIVO DESTE DOCUMENTO

Este documento consolida:

* estado arquitetural atual do projeto CODE-RAG
* análise estrutural da pipeline existente
* responsabilidades reais dos módulos
* riscos arquiteturais identificados
* limitações atuais
* diretrizes para evolução futura
* fundamentos da FASE 2B
* recomendações para evitar dívida técnica

O objetivo principal é:

preservar consistência arquitetural conforme o projeto evolui para um sistema avançado de inteligência estrutural e semântica de código-fonte.

---

# 2. VISÃO REAL DO PROJETO

O CODE-RAG não é mais apenas um RAG baseado em embeddings.

O projeto já começou a evoluir para:

* semantic structural retrieval
* symbolic navigation
* contextual code intelligence
* graph-assisted retrieval
* multi-stage retrieval orchestration
* semantic code exploration
* architecture-aware retrieval

Objetivo futuro:

Construir um mecanismo avançado de inteligência semântica e estrutural para código-fonte.

---

# 3. ESTADO ARQUITETURAL ATUAL

## 3.1 Camadas já existentes

### Chunk Extraction Layer

Responsável por:

* parsing AST
* extração estrutural
* geração de chunks
* identidade simbólica básica
* metadata contextual

Arquivo:

```text
pipeline/ast_chunker.py
```

---

### Semantic Layer

Responsável por:

* conceitos semânticos
* similaridade conceitual
* semantic matching
* semantic enrichment
* intent inference

Arquivos:

```text
pipeline/semantic_registry.py
pipeline/intent/intent_classifier.py
pipeline/intent/intent_registry.py
```

---

### Vector Infrastructure Layer

Responsável por:

* geração de embeddings
* normalização vetorial
* persistência vetorial
* semantic recall

Arquivos:

```text
pipeline/embeddings.py
pipeline/indexer/chroma_indexer.py
```

---

### Retrieval Orchestration Layer

Responsável por:

* candidate generation
* semantic expansion inicial
* orchestration do retrieval
* preparação de sinais

Arquivo:

```text
pipeline/retrieval/hybrid_retriever.py
```

---

### Ranking Layer

Responsável por:

* composição determinística de scores
* reranking híbrido
* combinação de sinais

Arquivo:

```text
pipeline/ranking/hybrid_ranker.py
```

---

# 4. PRINCIPAIS DESCOBERTAS DA ANÁLISE

# 4.1 O sistema ainda é retrieval-centric

Hoje o sistema pensa:

```text
resultado = chunk rankeado
```

Mas a evolução futura exigirá:

```text
resultado = contexto estrutural contextualizado
```

Essa é a principal transformação arquitetural futura.

---

# 4.2 O sistema ainda é metadata-oriented

Atualmente:

* estrutura é representada como metadata
* relações são implícitas
* traversal não existe
* dependências não são modeladas explicitamente

Exemplos atuais:

```text
imports_context
siblings
parent_chunk_id
ast_hierarchy_path
```

Esses elementos ainda são apenas:

```text
structural hints
```

E NÃO:

```text
structural relationships reais
```

---

# 4.3 O sistema já possui identidade simbólica implícita

O projeto já começou a modelar símbolos mesmo sem formalizar isso.

Exemplos:

```text
symbol_path
chunk_id
parent_chunk_id
module_name
```

Isso indica fortemente que a arquitetura correta futura será:

# Symbol-Centric Architecture

---

# 4.4 O projeto ainda NÃO possui Structural Intelligence Layer

Atualmente:

* chunker conhece hierarquia
* retriever conhece metadata
* ranker conhece structural_score

Mas:

nenhum componente é responsável pela estrutura real.

Isso será o núcleo da FASE 2B.

---

# 5. RESPONSABILIDADES ATUAIS DOS COMPONENTES

# 5.1 ASTChunker

Responsabilidades corretas atuais:

* parsing AST
* extração de funções/classes
* construção de identidade simbólica
* metadata contextual
* bootstrap estrutural

Responsabilidades que NÃO deve assumir futuramente:

* traversal
* graph reasoning
* dependency resolution
* ranking
* semantic inference complexa

---

# 5.2 SemanticRegistry

Responsabilidades corretas atuais:

* centralização semântica
* embeddings conceituais
* concept matching
* semantic similarity

Problema importante identificado:

Atualmente existem duas camadas semânticas coexistindo:

1. heurística lexical
2. similarity-based semantic matching

Exemplo:

```text
_infer_semantic()
semantic_registry.find_similar_concepts()
```

Isso ainda está controlado.

Mas pode gerar:

```text
semantic divergence
```

---

# 5.3 HybridRetriever

Responsabilidades corretas atuais:

* retrieval orchestration
* candidate generation
* semantic preparation
* handoff para ranking

Risco identificado:

O retriever começou a virar:

```text
metadata assembler
```

Isso NÃO deve evoluir para:

* traversal engine
* graph engine
* structural reasoning

---

# 5.4 HybridRanker

Responsabilidades corretas atuais:

* deterministic scoring
* signal composition
* reranking

Importante:

Hoje o structural_score NÃO é estrutural real.

Ele é apenas:

```text
heuristic symbolic scoring
```

Isso é positivo.

Porque permite introduzir structural intelligence futuramente sem quebrar contratos.

---

# 5.5 ChromaIndexer

Responsabilidades corretas atuais:

* persistência vetorial
* semantic recall
* armazenamento de embeddings

Problema arquitetural identificado:

O ChromaDB está sendo usado como:

```text
storage universal do sistema
```

Isso NÃO deve continuar.

O Chroma NÃO deve virar:

* graph database improvisado
* relationship store
* traversal backend

---

# 6. PRINCIPAIS RISCOS ARQUITETURAIS IDENTIFICADOS

# 6.1 Semântica distribuída

Hoje existem múltiplas fontes semânticas:

* _infer_semantic
* SemanticRegistry
* SemanticMatcher
* HybridRanker
* IntentClassifier

Isso pode evoluir para:

```text
semantic leakage
semantic inconsistency
```

---

# 6.2 Metadata explosion

Continuar adicionando relações no metadata seria um erro.

Exemplo perigoso:

```text
calls
references
dependencies
neighbors
```

persistidos diretamente no Chroma metadata.

Isso geraria:

* traversal procedural
* query complexity crescente
* baixo desempenho
* dívida técnica estrutural

---

# 6.3 Retrieval procedural

O antigo Retriever revelou o caminho errado:

* retrieval
* ranking
* semantic scoring
* symbolic scoring
* debugging

misturados no mesmo fluxo.

O pipeline oficial correto deve permanecer:

```text
HybridRetriever
    ↓
HybridRanker
```

---

# 6.4 Acoplamento implícito via dicts

Hoje o sistema ainda utiliza protocolos baseados em dicionários.

Exemplo:

```text
results = [dict]
```

Isso ainda funciona.

Mas futuramente poderá gerar:

```text
implicit coupling
invisible dependencies
schema drift
```

---

# 7. PRINCIPAL TRANSFORMAÇÃO DA FASE 2B

A FASE 2B NÃO é:

```text
melhorar retrieval
```

Ela é:

# introduzir modelagem relacional explícita

---

# 8. O QUE ESTÁ FALTANDO HOJE

O sistema já entende:

```text
o que um chunk representa
```

Mas ainda NÃO entende:

```text
como símbolos se relacionam
```

Essa é a evolução central da FASE 2B.

---

# 9. ARQUITETURA QUE COMEÇA A EMERGIR

A evolução correta começa a apontar para:

```text
Query
  ↓
Intent Detection
  ↓
Semantic Expansion
  ↓
Vector Candidate Retrieval
  ↓
Structural Expansion Engine
  ↓
Context Assembly
  ↓
Hybrid Ranking
  ↓
Contextual Response
```

Hoje ainda NÃO existem:

```text
Structural Expansion Engine
Context Assembly
```

---

# 10. DIREÇÃO ARQUITETURAL RECOMENDADA

# 10.1 Não continuar expandindo metadata

O próximo passo correto NÃO é:

```text
mais scores
mais metadata
mais heurísticas
```

O próximo passo correto é:

# modelagem estrutural explícita

---

# 10.2 Separar semantic recall de structural reasoning

O Chroma deve continuar responsável por:

* semantic recall
* vector search
* candidate generation

Mas NÃO por:

* traversal
* relationship queries
* graph navigation
* contextual assembly

---

# 10.3 Introduzir Structural Intelligence Layer

Provável direção futura:

```text
pipeline/structure/
    symbol_extractor.py
    relationship_extractor.py
    symbol_graph.py
    traversal_engine.py
    context_assembler.py
```

IMPORTANTE:

Essa estrutura ainda NÃO deve ser implementada sem modelagem prévia.

---

# 11. MODELO ESTRUTURAL MAIS PROMISSOR

# Symbol-Centric Architecture

A arquitetura atual já aponta para:

```text
símbolos como entidades centrais
```

E NÃO:

```text
chunks como documentos isolados
```

---

# 12. TIPOS DE ENTIDADES FUTURAS

Prováveis entidades futuras:

```text
Symbol
Relationship
TraversalContext
RetrievalContext
ContextWindow
```

---

# 13. RELATIONSHIPS FUTUROS

Exemplos prováveis:

```text
CALLS
IMPORTS
INHERITS
USES
VALIDATES
AUTHORIZES
RETURNS
DEPENDS_ON
```

Importante:

Esses relacionamentos devem ser:

* explícitos
* persistidos separadamente
* navegáveis
* independentes do Chroma metadata

---

# 14. CONTEXT ASSEMBLY

Futuramente retrieval NÃO retornará apenas chunks.

Provavelmente retornará algo próximo de:

```text
RetrievalContext
    primary_match
    supporting_symbols
    traversal_path
    related_dependencies
    semantic_neighbors
```

---

# 15. MULTI-STAGE RETRIEVAL

A arquitetura atual já suporta implicitamente:

```text
Stage 1:
vector recall

Stage 2:
structural expansion

Stage 3:
contextual reranking
```

Isso foi uma excelente decisão arquitetural.

---

# 16. DECISÃO MAIS IMPORTANTE DO PROJETO

Antes da implementação da FASE 2B:

é obrigatório definir:

## 1. tipos de símbolos

## 2. tipos de relacionamentos

## 3. traversal policies

## 4. context assembly model

## 5. ownership de responsabilidades

Sem isso:

há alto risco de:

* acoplamento estrutural
* traversal procedural
* graph spaghetti
* metadata explosion
* dívida técnica exponencial

---

# 17. RECOMENDAÇÃO TÉCNICA ATUAL

Com base na análise atual:

A direção mais saudável parece:

```text
FASE 2B
    in-memory structural graph
    + traversal engine
    + relationship extraction

FASE 3
    persistência estrutural incremental
```

---

# 18. O QUE NÃO DEVE SER FEITO

## NÃO:

* colocar traversal no ranker
* transformar Chroma em graph DB
* persistir edges em metadata textual
* misturar retrieval com traversal
* duplicar inferência semântica
* adicionar mais heurísticas desestruturadas
* criar novos pipelines paralelos

---

# 19. CONCLUSÃO GERAL

O projeto está arquiteturalmente muito mais saudável do que normalmente estaria nesta fase.

Os principais boundaries ainda existem.

Isso significa que:

# a FASE 2B ainda pode ser construída corretamente

SEM:

* refatoração destrutiva
* reescrita completa
* ruptura de contratos principais

O próximo grande passo NÃO é:

```text
melhor retrieval
```

É:

# formalizar inteligência estrutural.

Esse é o ponto de transição do projeto:

De:

```text
semantic retrieval pipeline
```

Para:

```text
code intelligence engine
```
