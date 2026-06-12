# DOC-E

Observação importante! Essa documentação foi escrita baseada nos documentos orginiais e consequequentemente, não estavam com a terminologia adequada: "Todas as referências a EXTERNAL e UNRESOLVED nestes documentos devem ser interpretadas como estados semânticos tipados derivados de ResolutionEventV2, e não como artefatos string-based legados."

# FECHAMENTO ARQUITETURAL DA FASE 3 E PLANO DE ELIMINAÇÃO DE LEGADOS

Status:
EM EXECUÇÃO

Data:
2026-06-09

---

# 1. OBJETIVO

Este documento consolida o estado arquitetural real do CODE-RAG V2 após a implementação da arquitetura Contract-Driven e define as ações obrigatórias para encerramento definitivo da Fase 3.

O objetivo principal não é adicionar novas funcionalidades.

O objetivo é concluir a migração arquitetural iniciada nos documentos anteriores e remover definitivamente mecanismos herdados que ainda coexistem com a arquitetura atual.

---

# 2. SITUAÇÃO ENCONTRADA

Durante auditoria realizada após estabilização dos contratos de identidade, verificou-se que o sistema possui duas arquiteturas operando simultaneamente.

## Arquitetura Nova

Baseada em:

* IdentityRegistryV2
* ResolutionEventV2
* ResolutionWorkflowEngineV2
* Contratos tipados
* Contract-Driven Testing
* Graph Boundary Enforcement
* Semantic Closure Controlada

Esta arquitetura encontra-se funcional.

---

## Arquitetura Legada

Baseada em:

* external::
* UNRESOLVED::
* promotion loops
* lazy external materialization
* fallback string-based resolution

Esta arquitetura ainda permanece parcialmente ativa.

---

# 3. DIAGNÓSTICO DA FASE 3

A Fase 3 não está incompleta.

A Fase 3 está em processo de consolidação.

O trabalho principal já foi realizado.

O que resta é eliminar mecanismos antigos que continuam coexistindo com a arquitetura nova.

---

# 4. INVENTÁRIO DE DÍVIDA ARQUITETURAL

## 4.1 Produção de external::

Arquivos identificados:

pipeline_v2/core/identity/identity_service_v2.py

pipeline_v2/core/semantic/inheritance/inheritance_resolver_v2.py

Problema:

Ainda produzem:

external::<symbol>

quando a resolução falha.

Isto contradiz o contrato atual baseado em ResolutionEventV2.

---

## 4.2 Consumo de external::

Arquivos identificados:

pipeline_v2/core/closure/semantic_closure_loop.py

pipeline_v2/core/graph/graph_core.py

pipeline_v2/core/graph/boundary/graph_boundary_enforcer_v2.py

Problema:

A arquitetura continua tratando external:: como estado operacional válido.

Isto não deveria mais existir.

---

## 4.3 Consumo de UNRESOLVED::

Arquivos identificados:

graph_core.py

graph_boundary_enforcer_v2.py

semantic_closure_loop.py

Problema:

UNRESOLVED:: ainda participa da lógica de execução.

O estado correto deve ser representado por ResolutionEventV2.

---

# 5. ESTADO DE MATURIDADE

Contratos Tipados:
100%

Identity Registry:
100%

Resolution Workflow:
100%

Contract-Driven Tests:
100%

Semantic Normalization:
95%

Graph Enforcement:
90%

Closure Layer:
70%

Remoção de external::
40%

Remoção de UNRESOLVED::
80%

Coerência Arquitetural Global:
75%

---

# 6. AÇÕES OBRIGATÓRIAS

## ETAPA A

Eliminar geração de external::

Arquivos:

identity_service_v2.py

inheritance_resolver_v2.py

Substituir:

return f"external::{ref}"

por eventos formais:

ResolutionEventV2(
FAILED_RESOLUTION
)

---

## ETAPA B

Refatorar SemanticClosureLoopV2

Objetivo:

Parar de depender de:

external::

Passar a operar exclusivamente sobre:

ResolutionEventV2

---

## ETAPA C

Eliminar Lazy External Materialization

Arquivo:

graph_core.py

Remover:

_external_node_ids

lazy_materialized

external node synthesis

Objetivo:

GraphCore não deve criar identidades.

GraphCore apenas consome identidades válidas.

---

## ETAPA D

Transformar GraphBoundaryEnforcerV2 em autoridade única

Todo bloqueio estrutural deve ocorrer antes da persistência.

GraphCore não deve conter regras duplicadas de validação.

---

## ETAPA E

Eliminar dependência operacional de UNRESOLVED::

Substituir por:

ResolutionEventTypeV2.FAILED_RESOLUTION

ResolutionEventTypeV2.REJECTED

---

# 7. AUDITORIA DE LIMPEZA DE REPOSITÓRIO

Após conclusão da consolidação arquitetural deverá ser executada auditoria completa de arquivos.

Objetivo:

Identificar:

* módulos mortos
* adapters obsoletos
* workflows abandonados
* implementações substituídas
* contratos não utilizados
* testes legados
* engines paralelas

---

# 8. INVENTÁRIO DE ARQUIVOS CANDIDATOS À REMOÇÃO

A lista abaixo NÃO autoriza exclusão imediata.

Ela apenas define os principais suspeitos para auditoria.

resolution_state_v2.py

legacy semantic adapters não utilizados

resolvers antigos substituídos por ResolutionWorkflow

mecanismos baseados em external::

mecanismos baseados em UNRESOLVED::

testes criados para comportamentos já removidos

implementações paralelas de identidade

---

# 9. CRITÉRIO DE ENCERRAMENTO DA FASE 3

A Fase 3 somente será considerada encerrada quando:

1. Nenhum componente operacional produzir external::

2. Nenhum componente operacional produzir UNRESOLVED::

3. Closure Layer operar exclusivamente por ResolutionEventV2

4. GraphCore deixar de sintetizar identidades

5. GraphBoundaryEnforcer tornar-se autoridade única de entrada

6. Toda suíte Contract-Driven permanecer verde

7. Primeiro teste E2E completo do pipeline for aprovado

Fluxo esperado:

AST
↓
Relationship
↓
Identity
↓
Graph
↓
Closure
↓
Final Semantic Graph

sem mocks estruturais.

---

# 10. PRÓXIMA MISSÃO

Após encerramento da Fase 3:

Executar Auditoria Arquitetural Completa.

Objetivos:

* remoção definitiva de legados
* redução de complexidade
* redução de duplicidade
* redução de acoplamento
* preparação da Fase 4

Nenhuma funcionalidade nova deverá ser iniciada antes da conclusão desta auditoria.
