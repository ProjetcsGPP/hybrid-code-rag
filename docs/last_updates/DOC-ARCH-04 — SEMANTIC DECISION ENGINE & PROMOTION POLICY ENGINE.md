# 📄 DOC-ARCH-04 — SEMANTIC DECISION ENGINE & PROMOTION POLICY ENGINE

Observação importante! Essa documentação foi escrita baseada nos documentos orginiais e consequequentemente, não estavam com a terminologia adequada: "Todas as referências a EXTERNAL e UNRESOLVED nestes documentos devem ser interpretadas como estados semânticos tipados derivados de ResolutionEventV2, e não como artefatos string-based legados."

## Status

CANÔNICO — ESPECIFICAÇÃO ARQUITETURAL

## Dependência

DOC-ARCH-01, DOC-ARCH-02, DOC-ARCH-03, DOC-ARCH-00

---

# 1. OBJETIVO

Este documento define o **motor decisório final da Fase de Reconciliation Semântica**, responsável por:

* avaliar candidatos semânticos (EXTERNAL / UNRESOLVED / PARTIAL)
* decidir promoção para STRICT
* rejeitar ou manter estados intermediários
* garantir consistência com Identity Layer e Contracts Layer

---

# 2. PAPEL NA ARQUITETURA

O Semantic Decision Engine (SDE) é o **último estágio lógico antes da persistência semântica enriquecida**.

Fluxo:

```
AST
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
Semantic Reconciliation
↓
👉 Semantic Decision Engine (SDE)
↓
Graph Enrichment / Persistence
```

---

# 3. RESPONSABILIDADES DO SEMANTIC DECISION ENGINE

## 3.1 Avaliação de Candidatos

O SDE recebe:

* EXTERNAL nodes
* UNRESOLVED references
* PARTIAL bindings
* cross-file candidates
* runtime hints

E produz:

* PROMOTION decision
* REJECTION decision
* DEFERRED decision

---

## 3.2 Consolidação de Evidência

O SDE NÃO decide com base em:

* ocorrência isolada
* string match simples
* heurística local

Ele deve consolidar:

* evidência multi-arquivo
* contexto de importação
* histórico de uso
* compatibilidade de contrato
* consistência com Identity Registry

---

## 3.3 Classificação Final

Saída obrigatória:

```
Decision:
  PROMOTE | REJECT | DEFER

Confidence:
  0.0 → 1.0

TargetState:
  STRICT | EXTERNAL | UNRESOLVED

Reason:
  structured explanation
```

---

# 4. PROMOTION POLICY ENGINE (PPE)

## 4.1 Função

O Promotion Policy Engine define **regras determinísticas de promoção semântica**.

Ele responde:

> “Quando um elemento deixa de ser EXTERNAL e vira STRICT?”

---

## 4.2 Regra central

```
promotion_allowed = confidence >= 0.90
```

---

## 4.3 Critérios obrigatórios de promoção

Um candidato só pode ser promovido se:

### (A) Evidência estrutural

* aparece em múltiplos chunks coerentes
* não é contradito por outros símbolos

---

### (B) Evidência de identidade

* compatível com Identity Registry
* não gera colisão canônica

---

### (C) Evidência de contrato

* respeita ChunkContract
* respeita SymbolContract
* respeita RelationshipContract

---

### (D) Evidência de contexto

* importável ou referenciável
* semanticamente consistente entre arquivos

---

# 5. TIPOS DE DECISÃO

## 5.1 PROMOTE

Converte:

```
EXTERNAL → STRICT
UNRESOLVED → STRICT
PARTIAL → STRICT
```

Somente se:

* confidence ≥ 0.90
* sem conflito estrutural

---

## 5.2 REJECT

Mantém estado original e bloqueia promoção.

Usado quando:

* conflito semântico
* ambiguidade estrutural
* colisão com Identity Registry

---

## 5.3 DEFER

Adia decisão para segundo pass.

Usado quando:

* falta de contexto cross-file
* ausência de evidência suficiente
* dependência de outro símbolo

---

# 6. RESOLUÇÃO MULTI-PASS

O SDE opera em dois níveis:

## PASS 1 — LOCAL DECISION

* análise intra-file
* heurística leve
* baixa confiança aceitável

---

## PASS 2 — GLOBAL DECISION

* análise cross-file
* consolidação de evidências
* ajuste de confiança

---

# 7. RELAÇÃO COM SEMANTIC RECONCILIATION ENGINE

O SDE NÃO reconcilia.

Ele apenas decide.

Separação clara:

| Componente            | Responsabilidade   |
| --------------------- | ------------------ |
| Reconciliation Engine | gerar candidatos   |
| Decision Engine       | avaliar candidatos |
| Promotion Engine      | aplicar resultado  |

---

# 8. SAÍDA PADRÃO DO SISTEMA

Cada decisão deve gerar um evento:

```
SemanticDecisionEventV2
```

Estrutura:

```python
{
  "symbol": "...",
  "previous_state": "EXTERNAL",
  "new_state": "STRICT",
  "decision": "PROMOTE",
  "confidence": 0.93,
  "evidence": [...],
  "reason": "multi-file binding confirmed"
}
```

---

# 9. GARANTIA DE CONSISTÊNCIA

O SDE NÃO pode:

* criar símbolos
* modificar Identity Registry
* alterar GraphBuilder
* sobrescrever contratos

Ele apenas:

👉 transforma estado semântico baseado em evidência

---

# 10. POLÍTICA DE NÃO-DETERMINISMO

O sistema deve ser:

* determinístico na decisão final
* probabilístico apenas na fase de scoring
* auditável em todas as decisões

---

# 11. MÉTRICAS DE QUALIDADE

O SDE deve expor:

* promotion_rate
* rejection_rate
* defer_rate
* confidence_distribution
* cross-file confirmation ratio

---

# 12. CRITÉRIO DE SUCESSO

O sistema é considerado correto quando:

* redução progressiva de EXTERNAL
* aumento de STRICT válido
* zero violação de Identity Registry
* estabilidade de graph consistency
* drift_score = 0.0 mantido

---

# 13. RESULTADO FINAL DA FASE 3

Com SDE + PPE operacionais:

O sistema atinge:

```
AST → SEMANTIC → IDENTITY → GRAPH → RECONCILIATION → DECISION → PERSISTENCE
```

com separação completa de responsabilidades.

---
