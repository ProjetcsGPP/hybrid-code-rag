# 📄 DOC-ARCH-03 — IMPLEMENTAÇÃO DO SEMANTIC SCORING ENGINE FORMAL

Status: ATIVO
Versão: 1.0
Dependência: DOC-ARCH-02 (Pipeline de Reconcilição Completo)

---
Observação importante! Essa documentação foi escrita baseada nos documentos orginiais e consequequentemente, não estavam com a terminologia adequada: "Todas as referências a EXTERNAL e UNRESOLVED nestes documentos devem ser interpretadas como estados semânticos tipados derivados de ResolutionEventV2, e não como artefatos string-based legados."

# 0. NATUREZA DO DOCUMENTO

Este documento formaliza o **Semantic Scoring Engine**, removendo ambiguidade heurística e estabelecendo um modelo **determinístico, auditável e extensível** para decisão de promoção semântica.

Ele substitui:

* scoring empírico
* pesos implícitos não verificáveis
* heurísticas não rastreáveis

por:

> um modelo probabilístico estruturado com decomposição explícita de evidências.

---

# 1. OBJETIVO DO SCORING ENGINE

Determinar com precisão se um símbolo:

* EXTERNAL
* UNRESOLVED
* PARTIAL

deve ser:

* PROMOTED → STRICT
* DEFERRED
* FAILED

---

# 2. PRINCÍPIO FUNDAMENTAL

> “Nenhuma promoção semântica pode ocorrer sem decomposição explícita da evidência.”

Ou seja:

* não existe score único opaco
* toda decisão é explicável por fatores atômicos
* toda promoção deve ser auditável

---

# 3. MODELO FORMAL

O score final é uma função:

```text id="sc0re1"
S(symbol) = f(I, R, C, U, F)
```

Onde:

| Símbolo | Significado          |
| ------- | -------------------- |
| I       | Import Evidence      |
| R       | Registry Match       |
| C       | Contextual Coherence |
| U       | Usage Evidence       |
| F       | Framework Signature  |

---

# 4. NORMALIZAÇÃO DOS COMPONENTES

Cada componente é normalizado no intervalo:

```text id="norm1"
[0.0, 1.0]
```

---

# 5. DEFINIÇÃO DOS COMPONENTES

---

# 5.1 IMPORT EVIDENCE (I)

Mede se o símbolo foi explicitamente importado.

## Valores:

* 1.0 → import explícito direto
* 0.7 → import indireto / alias
* 0.3 → import inferido via AST chain
* 0.0 → sem import

---

# 5.2 REGISTRY MATCH (R)

Consulta direta ao IdentityRegistry.

## Valores:

* 1.0 → match canônico exato
* 0.8 → match namespace parcial
* 0.4 → match estrutural aproximado
* 0.0 → inexistente

---

# 5.3 CONTEXTUAL COHERENCE (C)

Mede coerência dentro do arquivo + cross-file context.

## Fórmula conceitual:

```text id="c0h3r"
C = overlap(local_context, global_context)
```

## Valores:

* 1.0 → contexto totalmente consistente
* 0.5 → parcialmente consistente
* 0.0 → incoerente

---

# 5.4 USAGE EVIDENCE (U)

Frequência e consistência de uso.

## Valores:

* 1.0 → usado em múltiplos arquivos coerentes
* 0.6 → uso moderado
* 0.2 → uso isolado
* 0.0 → não utilizado

---

# 5.5 FRAMEWORK SIGNATURE (F)

Reconhecimento de padrão de framework.

## Exemplos:

* Django ORM → 1.0
* FastAPI route → 1.0
* Python builtin → 1.0
* padrão desconhecido → 0.0

---

# 6. FUNÇÃO FINAL DO SCORE

## Fórmula consolidada:

```text id="final1"
S = (0.30 * I) +
    (0.25 * R) +
    (0.20 * C) +
    (0.15 * U) +
    (0.10 * F)
```

---

# 7. DECISÃO BASEADA NO SCORE

## 7.1 PROMOTION RULE

```text id="rule1"
S >= 0.90 → PROMOTED (STRICT)
```

---

## 7.2 PARTIAL RULE

```text id="rule2"
0.60 ≤ S < 0.90 → PARTIAL
```

---

## 7.3 DEFER RULE

```text id="rule3"
S < 0.60 → UNRESOLVED mantém estado
```

---

# 8. INTERPRETAÇÃO SEMÂNTICA DOS RESULTADOS

---

## 8.1 PROMOTED

Significa:

* símbolo pode integrar Identity Layer
* vínculo confiável estabelecido
* apto para Graph Enrichment

---

## 8.2 PARTIAL

Significa:

* evidência insuficiente para promoção
* mas não descartado
* requer segunda passagem (future reconciliation)

---

## 8.3 UNRESOLVED

Significa:

* ausência de evidência estrutural suficiente
* não deve ser interpretado como erro

---

# 9. GARANTIA DE DETERMINISMO

O scoring engine deve obedecer:

```text id="det1"
Mesmo input → mesmo output
```

Para isso:

* contexto deve ser versionado
* registry deve ser snapshot-based
* imports devem ser AST deterministic

---

# 10. RESTRIÇÕES ARQUITETURAIS

O scoring engine NÃO pode:

* criar símbolos
* alterar Identity Registry
* modificar Graph structure
* inferir entidades inexistentes
* substituir contratos existentes

---

# 11. INTERAÇÃO COM PIPELINE (DOC-ARCH-02)

Fluxo atualizado:

```text id="flow1"
Candidate Generation
↓
Context Aggregation
↓
CrossFile Resolution
↓
SEMANTIC SCORING ENGINE (DOC-ARCH-03)
↓
Decision Engine
↓
Event Emission
↓
Graph Enrichment
```

---

# 12. IMPACTO ARQUITETURAL

## 12.1 Antes

* scoring heurístico
* decisões implícitas
* baixa auditabilidade

---

## 12.2 Depois

* scoring formal
* decisões explicáveis
* rastreabilidade completa
* auditabilidade total

---

# 13. MÉTRICAS DE VALIDAÇÃO

## Objetivo técnico:

* reduzir falsos positivos de promoção
* aumentar precisão de binding
* manter drift_score = 0.0

---

# 14. RISCOS CONTROLADOS

## 14.1 Overconfidence Risk

Score alto sem evidência real

Mitigação:

* peso forte em Registry Match

---

## 14.2 Underpromotion Risk

Símbolos corretos não promovidos

Mitigação:

* Cross-file usage weighting

---

## 14.3 Context Drift Risk

Contexto inconsistente entre arquivos

Mitigação:

* snapshot-based context model

---

# 15. POSIÇÃO NA ARQUITETURA

O Scoring Engine é:

> o núcleo matemático da Semantic Reconciliation Layer

---

# 16. CONCLUSÃO

Este documento transforma a SRL de:

* pipeline heurístico

para:

* sistema probabilístico estruturado e auditável

---

# 17. PRÓXIMO DOCUMENTO NATURAL

Se a sequência continuar:

👉 DOC-ARCH-04 — SEMANTIC DECISION ENGINE & PROMOTION POLICY ENGINE

Onde:

* scoring deixa de ser isolado
* vira política de decisão global
* integração total com Identity + Graph + Contracts

---

Se quiser, o próximo passo pode ser:

* formalizar isso como código Python executável
* ou converter o modelo em grafo probabilístico (Bayesian SRL)
* ou desenhar testes contratuais para validar o scoring engine

Só me diga a direção.
