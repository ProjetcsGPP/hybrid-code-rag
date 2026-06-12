# DOC-C — ROADMAP OFICIAL E PROTOCOLO DE CONTINUIDADE

Status: ATIVO

Objetivo:

Garantir continuidade do projeto sem perda de contexto entre chats.

---

# 1. FASE AUTORIZADA

FASE 3

Semantic Reconciliation Layer

---

# 2. OBJETIVO DA FASE

Resolver:

* EXTERNAL
* UNRESOLVED
* PARTIAL

sem alterar:

* Identity Layer
* Graph Layer
* Contracts aprovados

---

# 3. FOCO ATUAL

Attribute Resolution

Builtin Resolution

Framework Resolution

Cross-File Resolution

Qualidade dos relatórios semânticos

---

# 4. SEMANTIC RECONCILIATION LAYER

Posição:

Contract Validation
↓
Semantic Reconciliation
↓
Graph Enrichment

---

# 5. COMPONENTES AUTORIZADOS

UnresolvedRegistry

SemanticCandidateEngine

CrossFileResolver

ReconciliationEngine

GraphEnricher

SemanticReconciliationReport

---

# 6. REGRAS DA RECONCILIAÇÃO

Nunca:

* criar identidade;
* alterar Registry;
* alterar GraphBuilder;
* sobrescrever decisões da Identity Layer.

Somente promover:

EXTERNAL

ou

UNRESOLVED

quando houver confiança suficiente.

---

# 7. CRITÉRIO DE PROMOÇÃO

confidence >= 0.90

---

# 8. CRITÉRIOS DE ACEITAÇÃO

Reduzir significativamente:

external::UNRESOLVED::*

Mantendo:

drift_score = 0.0

missing_in_graph = []

orphan_graph_nodes = []

inferred_nodes = []

---

# 9. PROCEDIMENTO OBRIGATÓRIO PARA NOVOS CHATS

Antes de qualquer proposta:

1. Ler DOC-A.
2. Ler DOC-B.
3. Ler DOC-C.
4. Solicitar árvore de diretórios.
5. Solicitar arquivos necessários.
6. Ler código real.
7. Validar impacto arquitetural.
8. Produzir plano incremental.
9. Somente então propor alterações.

---

# 10. CONFIRMAÇÃO OBRIGATÓRIA

Todo novo chat deve responder:

DOCUMENTOS LIDOS

ESTADO COMPREENDIDO

FASE IDENTIFICADA

AGUARDANDO ÁRVORE DE DIRETÓRIOS E ARQUIVOS

Sem essa confirmação nenhuma proposta técnica deve ser considerada válida.

---

# 11. REGRA FINAL

É proibido inferir arquitetura, componentes ou problemas sem análise do código real.

Toda decisão deve partir:

dos documentos oficiais
+
do estado atual do código-fonte
+
das evidências produzidas pela auditoria.
