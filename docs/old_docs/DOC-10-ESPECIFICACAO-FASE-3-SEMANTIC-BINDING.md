# DOC-10 — ESPECIFICAÇÃO DA FASE 3

## Semantic Binding e Reference Resolution

Status: RASCUNHO INICIAL

Data: 2026-06-02

Projeto: CODE-RAG V2

Dependência obrigatória:

* DOC-01
* DOC-02
* DOC-03
* DOC-04
* DOC-05
* DOC-06
* DOC-07
* DOC-08
* DOC-09

---

# 1. OBJETIVO DA FASE

A Fase 2 encerrou a estabilização da identidade.

Foi comprovado por auditoria que:

* Registry é autoridade única.
* Não existem identidades paralelas.
* Não existem nós órfãos.
* Não existem símbolos perdidos.
* Não existem símbolos inferidos indevidamente.
* Drift = 0.0.

Portanto, o próximo problema arquitetural do CODE-RAG V2 não é mais identidade.

O novo problema é:

RESOLUÇÃO SEMÂNTICA.

---

# 2. PROBLEMA OBSERVADO

Durante a ingestão completa do projeto Django analisado foram encontrados:

Files: 151

Chunks: 1854

Symbols: 1854

Relationships: 4942

Nodes: 3732

Distribuição:

STRICT: 1835

EXTERNAL: 1897

Quase metade do grafo é composta por nós classificados como EXTERNAL.

Exemplos:

external::UNRESOLVED::timezone.now

external::UNRESOLVED::admin.display

external::UNRESOLVED::User.objects.filter

external::UNRESOLVED::getattr

external::UNRESOLVED::hasattr

---

# 3. DEFINIÇÕES OFICIAIS

## 3.1 STRICT SYMBOL

Símbolo criado diretamente pelo pipeline.

Exemplos:

accounts.models.User

accounts.services.AuthorizationService

accounts.views.UserViewSet

Características:

* possui identidade canônica;
* está registrado no Registry;
* possui nó no Graph.

---

## 3.2 EXTERNAL SYMBOL

Referência encontrada durante a análise mas não vinculada a um símbolo conhecido.

Exemplos:

timezone.now

admin.display

User.objects.filter

Características:

* não possui binding;
* permanece fora do domínio semântico resolvido.

---

## 3.3 RESOLVED SYMBOL

Referência originalmente EXTERNAL que foi vinculada a um símbolo canônico.

Exemplo:

Antes:

external::UNRESOLVED::User.objects.filter

Depois:

apps.accounts.models.User

---

# 4. OBJETIVOS DA FASE 3

A Fase 3 deve reduzir progressivamente a quantidade de EXTERNAL.

Objetivo inicial:

Reduzir EXTERNAL em pelo menos 50%.

Objetivo ideal:

Resolver todo EXTERNAL que pertença ao repositório analisado.

---

# 5. ETAPA 3A — INVENTÁRIO DE EXTERNAL

Nenhuma implementação deve ser iniciada antes desta etapa.

Será criado um relatório contendo:

* lista completa dos EXTERNAL;
* frequência;
* categoria;
* origem.

Classificações mínimas:

* IMPORT
* SELF
* ORM
* BUILTIN
* FRAMEWORK
* THIRD_PARTY
* UNKNOWN

Resultado esperado:

Mapa quantitativo do problema.

---

# 6. ETAPA 3B — IMPORT BINDING

Objetivo:

Resolver símbolos importados.

Exemplo:

from apps.accounts.models import User

Uso:

User.objects.filter(...)

Binding esperado:

apps.accounts.models.User

Fonte principal:

imports_context

já produzido pelo ASTChunker.

---

# 7. ETAPA 3C — SELF RESOLUTION

Objetivo:

Resolver referências iniciadas por self.

Exemplo:

self.save()

Resultado esperado:

CurrentClass.save

ou

CurrentClass.save_method

dependendo da granularidade adotada.

---

# 8. ETAPA 3D — ORM RESOLUTION

Objetivo:

Resolver referências ORM.

Exemplo:

User.objects.filter()

Resultado esperado:

User

ou

User.QuerySet

(conforme decisão arquitetural posterior)

---

# 9. ETAPA 3E — BUILTIN CLASSIFICATION

Objetivo:

Evitar tentativas de resolução para elementos que nunca deverão gerar símbolos.

Exemplos:

getattr

hasattr

len

str

dict

Esses elementos devem permanecer classificados como BUILTIN.

---

# 10. NOVA CAMADA ARQUITETURAL

Será introduzido um componente dedicado.

Nome provisório:

SemanticBinderV2

Responsabilidades:

* resolver imports;
* resolver aliases;
* resolver self;
* resolver ORM;
* produzir referências canônicas.

Restrições:

* não criar símbolos;
* não alterar identidade;
* não registrar objetos;
* não modificar Registry.

A autoridade continua sendo a Identity Layer.

---

# 11. REGRAS DE SEGURANÇA

A Fase 3 não poderá:

* modificar IdentityRegistry;
* modificar IdentityStrategy;
* modificar SymbolFactory;
* modificar RelationshipFactory;
* modificar GraphBuilder.

Esses componentes encontram-se congelados após validação completa da Fase 2.

---

# 12. CRITÉRIOS DE ACEITAÇÃO

A Fase 3 será considerada concluída quando:

1. houver classificação formal dos EXTERNAL;
2. houver resolução automática de imports;
3. houver resolução automática de self;
4. houver resolução automática de ORM;
5. a auditoria continuar apresentando:

drift_score = 0.0

missing_in_graph = []

orphan_graph_nodes = []

inferred_nodes = []

6. a quantidade de EXTERNAL for significativamente reduzida.

---

# 13. PRÓXIMA ATIVIDADE

Criar o primeiro instrumento da Fase 3:

External Symbol Inventory Report

Objetivo:

Mapear os 1897 nós EXTERNAL encontrados durante a ingestão completa.

Nenhuma implementação deverá ocorrer antes da conclusão desse relatório.
