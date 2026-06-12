# 📙 DOC 02 — VISÃO ESTRATÉGICA (CODE-RAG V2)

## 🎯 Objetivo
Definir a arquitetura conceitual e direção futura do sistema CODE-RAG V2, servindo como base para evolução controlada e decisões estruturais.

---

# 🧠 1. NATUREZA DO SISTEMA

CODE-RAG V2 é um sistema híbrido composto por:

- Code Intelligence Engine
- Semantic Graph Builder
- Runtime Execution Simulator
- Identity Resolution System

---

# 🧩 2. ARQUITETURA CONCEITUAL IDEAL

SOURCE CODE
  ↓
SEMANTIC LAYER
(Symbol + Relationship)
  ↓
IDENTITY LAYER
(canonical resolution)
  ↓
GRAPH LAYER
(Node + Edge)
  ↓
PERSISTENCE LAYER
(PostgreSQL)

---

# ⚖️ 3. DECISÕES ARQUITETURAIS EM ABERTO

## 3.1 Fonte de Verdade
- Identity-centric
- Graph-centric
- Semantic-centric

---

## 3.2 Papel do IdentityRegistry
- Cache de resolução
- Autoridade global
- Sistema derivado

---

## 3.3 Papel do Graph
- Estrutura final
- Projeção semântica
- Camada intermediária

---

## 3.4 Papel do Legacy
- Compatibilidade
- ETL contínuo
- Substituição progressiva

---

# 🔄 4. DIREÇÃO EVOLUTIVA

## Fase Atual
- Sistema híbrido (semantic + graph + identity)

## Fase Intermediária
- Graph como base estrutural principal

## Fase Final
- Sistema determinístico com reconstrução completa do grafo

---

# 🚨 5. PROBLEMA CENTRAL

O sistema ainda não possui uma única camada de verdade global.

---

# 🧠 6. PRINCÍPIO ARQUITETURAL FUTURO

## SINGLE SOURCE OF TRUTH PRINCIPLE

Deve existir:

- 1 fonte estrutural
- 1 sistema de identidade canônica
- 1 pipeline determinístico

---

# 📈 7. VISÃO DE EVOLUÇÃO

## Estado atual
- dual model system

## Estado futuro próximo
- graph-centric architecture

## Estado futuro ideal
- fully deterministic graph reconstruction system

---

# 📌 8. CONCLUSÃO ESTRATÉGICA

CODE-RAG V2 está em fase de consolidação arquitetural, migrando de múltiplas representações paralelas para um modelo unificado baseado em grafo determinístico e identidade canônica consistente.

