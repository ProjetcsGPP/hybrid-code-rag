# 📘 DOC 04 — PLANO DE EVOLUÇÃO ARQUITETURAL (CODE-RAG V2)

## 🎯 Objetivo

Definir o plano de evolução do CODE-RAG V2 a partir do estado atual real do sistema, eliminando ambiguidades restantes entre:

* semântica
* identidade
* grafo estrutural
* persistência

e conduzindo a arquitetura para um modelo determinístico e incremental consistente.

---

# 🧠 1. ESTADO ATUAL CONSOLIDADO

O sistema já atingiu:

## ✔ Camada semântica funcional

* RelationshipCoreV2 operacional
* inferência de relações ativa
* SemanticContextV2 integrado

## ✔ Camada de resolução funcional

* SymbolResolutionEngineV2 consolidado
* múltiplas fontes de lookup unificadas

## ✔ Camada de identidade parcialmente centralizada

* IdentityServiceV2 é o único resolvedor canônico
* IdentityRegistryV2 ainda em memória

## ✔ Camada estrutural funcional

* GraphBuilderV2 operacional
* GraphNodeV2 ainda presente como projeção híbrida

## ✔ Persistência funcional

* PostgreSQL ativo
* nodes / edges já estruturados

---

# ⚠️ 2. PROBLEMAS RESIDUAIS (REALMENTE IMPORTANTES AGORA)

Esses são os problemas que realmente importam a partir deste ponto:

## 2.1 Identity ainda não é persistente

* IdentityRegistry é memória
* não há replay de identidade
* não há reconstrução determinística

📌 impacto:
→ drift após restart
→ inconsistência de canonicalização

---

## 2.2 Graph ainda não é derivado exclusivamente

Hoje:

* GraphBuilder cria estrutura
* RelationshipCore influencia estrutura indiretamente
* Identity participa parcialmente da construção

📌 problema:
→ grafo não é 100% derivado de um único fluxo

---

## 2.3 GraphNodeV2 ainda tem papel híbrido

* ainda é criado em fluxo semântico
* ainda participa da identidade transitória

📌 problema:
→ mistura de camadas conceituais

---

## 2.4 Symbol / Relationship ainda carregam intenção estrutural

* RelationshipCore ainda “decide forma”
* SymbolResolution ainda influencia estrutura final

📌 problema:
→ semântica ainda invade estrutura

---

# 🧭 3. PRINCÍPIO ARQUITETURAL DA PRÓXIMA FASE

A próxima fase deve consolidar este princípio:

## SINGLE DIRECTION PIPELINE PRINCIPLE

```text
SEMÂNTICA → RESOLUÇÃO → IDENTIDADE → ESTRUTURA → PERSISTÊNCIA
```

E PROIBIR:

* retorno de estrutura para semântica
* identidade influenciar semântica
* grafo influenciar resolução

---

# 🚀 4. PLANO DE EVOLUÇÃO EM FASES

---

# 🟦 FASE 2.1 — CONSOLIDAÇÃO DA IDENTIDADE PERSISTENTE

## 🎯 Objetivo

Transformar identidade em estado reconstruível.

### Mudanças:

### 4.1 Criar Identity Store persistente

Adicionar tabela:

```sql
graph_meta.identities
```

Contendo:

* identity_id
* canonical
* name_index
* symbol_reference
* created_at
* version

---

### 4.2 IdentityRegistry deixa de ser autoridade

Passa a ser:

> cache de leitura

---

### 4.3 IdentityService passa a consultar banco

Fluxo:

```text
Postgres Identity Store → IdentityService → cache local
```

---

### Resultado esperado:

✔ identidade replayável
✔ canonical estável entre execuções
✔ eliminação de drift de identidade

---

# 🟩 FASE 2.2 — SEPARAÇÃO TOTAL DE GRAFO

## 🎯 Objetivo

Eliminar qualquer influência semântica na estrutura do grafo.

### Mudanças:

### 4.4 GraphBuilder passa a ser único criador de estrutura

* RelationshipCore NÃO cria GraphNodeV2
* SymbolResolution NÃO cria estrutura
* Identity NÃO cria nós

---

### 4.5 GraphNodeV2 vira EXCLUSIVAMENTE DTO

Regras:

* proibido registrar no IdentityRegistry
* proibido lifecycle próprio
* proibido criação fora do GraphBuilder

---

### Resultado esperado:

✔ grafo 100% estrutural
✔ semântica não interfere na forma
✔ identidade não cria estrutura

---

# 🟨 FASE 2.3 — DETERMINISMO DO GRAFO

## 🎯 Objetivo

Garantir reconstrução completa do grafo a partir de identidade + relações.

---

### 4.6 Graph becomes derivable artifact

Entrada:

* identities (persistidas)
* relationships (semânticas)

Saída:

* nodes
* edges

---

### 4.7 Introdução do Graph Rebuilder

Novo componente:

```text
GraphRebuilderV2
```

Responsável por:

* reconstruir grafo do zero
* validar consistência
* detectar drift estrutural

---

### Resultado esperado:

✔ grafo totalmente reconstruível
✔ sem dependência de runtime state

---

# 🟥 FASE 2.4 — ELIMINAÇÃO DE DUAL SOURCE OF TRUTH

## 🎯 Objetivo

Eliminar qualquer duplicidade entre:

* runtime graph
* persisted graph
* semantic graph

---

### 4.8 Unificação final

Todos os estados passam a derivar de:

```text
PostgreSQL (Identity + Relationships)
```

---

### 4.9 Runtime graph deixa de ser fonte

Passa a ser:

> projeção derivada

---

### Resultado esperado:

✔ zero divergência entre runtime e persistência
✔ replay completo do sistema

---

# 🟪 FASE 2.5 — ESTABILIZAÇÃO DO DRIFT ENGINE

## 🎯 Objetivo

Transformar drift detection em mecanismo central de confiabilidade.

---

### 4.10 Drift Engine passa a validar:

* identity mismatch
* missing relationships
* graph divergence
* unresolved symbols

---

### Resultado esperado:

✔ sistema autoauditorável
✔ detecção contínua de inconsistência

---

# 🧠 5. ARQUITETURA FINAL ESPERADA

Após essas fases:

```text
SOURCE CODE
   ↓
SEMANTIC LAYER (RelationshipCore)
   ↓
RESOLUTION LAYER (SymbolResolutionEngine)
   ↓
IDENTITY LAYER (IdentityService + Postgres)
   ↓
GRAPH BUILDER (GraphBuilderV2)
   ↓
PERSISTENCE (Postgres canonical)
   ↓
GRAPH RECONSTRUCTION (GraphRebuilderV2)
```

---

# 📌 6. REGRA MAIS IMPORTANTE DA PRÓXIMA FASE

## NENHUMA CAMADA PODE MAIS CRIAR IDENTIDADE OU ESTRUTURA FORA DO SEU DOMÍNIO

* semântica NÃO cria grafo
* resolução NÃO cria estrutura
* identidade NÃO cria nodes
* grafo NÃO resolve significado

---

# 🧭 7. DIREÇÃO ESTRATÉGICA FINAL

O sistema está evoluindo para:

> um sistema determinístico de reconstrução de conhecimento estruturado a partir de identidade canônica persistida.

---

# 📌 8. RESUMO EXECUTIVO

A próxima evolução do CODE-RAG não é mais:

* adicionar features
* melhorar pipeline
* expandir semântica

Mas sim:

## CONSOLIDAR UM MODELO DE VERDADE ÚNICA RECONSTRUÍVEL


# 🧭 OPÇÃO 1 — DIAGRAMA ARQUITETURAL FINAL (PÓS FASE 2)

## 🧠 VISÃO CONSOLIDADA (NOVA REALIDADE)

```
                ┌──────────────────────────────┐
                │        SOURCE CODE           │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │     AST / CHUNK LAYER        │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │     SYMBOL CORE LAYER        │
                │  (SymbolCoreV2 / Extractor)  │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │ SYMBOL RESOLUTION LAYER      │
                │ SymbolResolutionEngineV2     │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │   RELATIONSHIP CORE LAYER    │
                │ RelationshipCoreV2           │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │  IDENTITY GATEWAY LAYER      │
                │ IdentityServiceV2            │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │ IDENTITY REGISTRY (STATE)    │
                │ IdentityRegistryV2           │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │ GRAPH PROJECTION LAYER       │
                │ GraphBuilderV2               │
                └──────────────┬───────────────┘
                               ↓
                ┌──────────────────────────────┐
                │ PERSISTENCE LAYER (POSTGRES) │
                │ nodes / edges / legacy       │
                └──────────────────────────────┘
```

---

## 🔥 PRINCÍPIO NOVO (IMPORTANTE)

👉 IdentityServiceV2 NÃO é ontologia
👉 ele é:

> “gateway determinístico de resolução canônica”

Ou seja:

* ele NÃO decide significado
* ele NÃO cria estrutura
* ele NÃO modela grafo

Ele só responde:

> “quem é isso no sistema?”

---

# 🧨 OPÇÃO 2 — ONDE HOJE EXISTEM VAZAMENTOS (CRÍTICO)

Aqui está o que está “quebrando a pureza arquitetural” hoje:

---

## 🚨 2.1 RelationshipCoreV2 ainda toca IdentityRegistry direto

### Problema:

```python
self.identity_registry.register(rel)
```

❌ Isso mistura:

* semântica (Relationship)
* identidade (Registry mutation)
* projeção (GraphNodeV2 indireto)

---

## 🚨 2.2 IdentityServiceV2 e IdentityRegistry fazem resolução dupla

Você tem:

* IdentityServiceV2.resolve()
* IdentityRegistryV2.resolve()

⚠️ Isso cria:

> dual resolution path

---

## 🚨 2.3 GraphBuilder ainda pode inferir identidade implicitamente

Ele aceita:

* string ids
* objetos
* GraphNodeV2

❌ sem contrato rígido de Identity Gateway

---

## 🚨 2.4 SymbolResolutionEngine ainda “cai para registry”

```python
self.identity_registry.resolve_by_name(...)
```

⚠️ Ele ignora IdentityServiceV2

---

## 🚨 2.5 GraphNodeV2 ainda aparece como “quase identidade”

Mesmo com regra:

> ele deveria ser só projection

mas ainda:

* pode ser criado fora do IdentityService
* pode existir sem canonical enforcement

---

# 🧭 OPÇÃO 3 — PLANO DE REFATORAÇÃO INCREMENTAL (SEGURO)

Aqui está o plano REALISTA sem quebrar sistema.

---

# 🟢 FASE 2.1 — CONSOLIDAÇÃO DO IDENTITY GATEWAY

## 🎯 objetivo

IdentityServiceV2 vira ÚNICA porta de entrada de resolução

---

### mudanças:

### 1. remover acesso direto ao registry fora do service

❌ proibido:

```python
identity_registry.resolve(...)
identity_registry.resolve_by_name(...)
```

✔ substituição:

```python
identity_service.resolve(...)
```

---

### 2. IdentityService vira facade completa

Adicionar nele:

* resolve_by_name
* resolve_by_canonical
* exists
* register proxy (opcional controlado)

---

# 🟡 FASE 2.2 — NORMALIZAÇÃO DO RELATIONSHIP CORE

## objetivo:

RelationshipCore NÃO toca registry diretamente

---

### mudança crítica:

❌ hoje:

```python
self.identity_registry.register(rel)
```

✔ futuro:

```python
self.identity_service.register_relationship(rel)
```

ou

```python
self.identity_service.ensure_identity(rel.source)
self.identity_service.ensure_identity(rel.target)
```

---

# 🟠 FASE 2.3 — ELIMINAR DUPLA RESOLUÇÃO

## objetivo:

um único caminho de resolução

---

### regra nova:

| componente        | pode resolver identidade?      |
| ----------------- | ------------------------------ |
| IdentityServiceV2 | SIM                            |
| Registry          | NÃO                            |
| Resolver Engine   | NÃO (apenas consulta indireta) |

---

# 🔵 FASE 2.4 — GRAPH BOUNDARY STRICT

## objetivo:

GraphBuilder não pode decidir identidade

---

### regra:

✔ recebe apenas:

* resolved_id (string canônica)

❌ nunca:

* raw string
* name lookup
* fallback

---

# 🟣 FASE 2.5 — REGISTRY PURIFICATION

IdentityRegistry vira:

> storage layer only

sem lógica:

* sem resolve inteligente
* sem fallback
* sem heurística

---

# 🔴 FASE FINAL — ESTADO ALVO

## depois disso:

### único fluxo válido:

```
RAW CODE
  ↓
SymbolCore
  ↓
SymbolResolutionEngine
  ↓
IdentityServiceV2   ← CENTRO REAL
  ↓
GraphBuilderV2
  ↓
PostgreSQL
```

---

# 🧠 RESPOSTA DIRETA À SUA DÚVIDA CENTRAL

> “IdentityService deve ser o ponto central?”

✔ SIM — MAS com uma nuance crítica:

Ele NÃO é ontologia.

Ele é:

> CONTROL PLANE de identidade

---

## 🧩 separação correta:

| conceito         | responsabilidade     |
| ---------------- | -------------------- |
| IdentityService  | controle e resolução |
| RelationshipCore | semântica            |
| SymbolResolution | descoberta           |
| GraphBuilder     | projeção             |
| Registry         | storage              |

---

# 🚀 SE PRÓXIMO PASSO

Se quiser, no próximo chat posso te entregar:

### 1. 📐 DIAGRAMA “FORMA FINAL LIMPA”

(com setas de proibição entre camadas)

### 2. 🔍 MAPA DE VAZAMENTO POR ARQUIVO

(ex: linha exata onde quebra arquitetura hoje)

### 3. 🛠 PLANO DE REFACTOR EM COMMIT ORDER

(pronto para execução incremental sem risco)

---

Se quiser ser ainda mais agressivo na evolução do sistema, posso também desenhar a versão “IDEAL FINAL” onde IdentityService desaparece e vira apenas protocolo distribuído — mas isso já é fase pós-2.

Só me diz qual direção você quer seguir primeiro.


