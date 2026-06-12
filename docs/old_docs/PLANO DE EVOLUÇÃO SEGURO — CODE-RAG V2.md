PLANO DE EVOLUÇÃO SEGURO — CODE-RAG V2
(Baseado no estado real DOC 08+)
🧱 FASE 0 — ESTABILIZAÇÃO DO ESTADO REAL (OBRIGATÓRIA)
🎯 Objetivo

Garantir que o sistema atual está 100% consistente com o modelo operacional real descrito nos DOC 08+.

🔍 0.1 Auditoria de consistência Postgres ↔ Runtime

Verificar:

symbols possuem project_id
relationships possuem project_id
edges/nodes estão alinhados
não existem registros órfãos
GraphBuilder não cria identidade paralela

📌 Saída:

relatório de inconsistências
lista de correções incrementais
🔍 0.2 Verificação de GraphNodeV2

Confirmar:

GraphNodeV2 NÃO gera ID
GraphNodeV2 NÃO persiste
GraphNodeV2 é apenas projection layer

📌 Ação:

bloquear qualquer uso como identidade
🔍 0.3 Validação Identity (FECHADO)

Garantir:

IdentityRegistry NÃO é modificado
não existe fallback alternativo
não existe duplicação de resolução

📌 Resultado:

Identity congelado como primitive estável

🧩 FASE 1 — CONSOLIDAÇÃO DO MODELO DE PROJETO (MULTI-PROJECT CORE)
🎯 Objetivo

Finalizar a camada de multi-projeto sem impacto no core semântico.

🔧 1.1 Enforcement de project_id global

Garantir:

todo SYMBOL possui project_id
toda RELATIONSHIP possui project_id
todo EDGE possui project_id
todo runtime trace possui project_id

📌 Sem exceção.

🔧 1.2 ProjectResolver central

Criar lógica única:

detecta projeto ativo
resolve escopo de análise
impede cross-project leakage acidental

📌 Importante:
não altera identidade nem grafo — só escopo.

🔧 1.3 Isolamento semântico por projeto

Cada execução deve garantir:

símbolos não cruzam projetos
relações não vazam entre projetos
runtime graph é sempre scoped
🧠 FASE 2 — CONSOLIDAÇÃO DO GRAPH LAYER (SEM NOVAS ABSTRAÇÕES)
🎯 Objetivo

Eliminar inconsistências entre:

SYMBOL → NODE
RELATIONSHIP → EDGE
runtime graph → persisted graph
🔧 2.1 Canonical Graph Mapping

Fixar regra:

Origem	Destino
Symbol	Node
Relationship	Edge

📌 Sem exceções.

🔧 2.2 GraphBuilderV2 estabilizado

Garantir:

não cria entidades novas
apenas transforma
não reinterpreta semântica
não duplica nodes
🔧 2.3 Graph Projection Layer reforçado

GraphNodeV2:

apenas leitura
apenas view
nunca source-of-truth
🔄 FASE 3 — DRIFT ENGINE (EVOLUÇÃO CONTROLADA)
🎯 Objetivo

Aumentar inteligência sem afetar estrutura.

🔧 3.1 Tipos de drift já definidos (expandir cobertura)

O Drift Engine deve capturar:

orphan symbols
missing edges
runtime mismatch
stale projections
unresolved references
🔧 3.2 Drift não corrige automaticamente

Regra:

Drift Engine apenas detecta e classifica

Correção é:

pipeline separado
incremental
auditável
🔧 3.3 Drift scoring unificado

Criar score por:

projeto
módulo
símbolo
🧠 FASE 4 — SEMANTIC REPLAY ENGINE (EVOLUÇÃO SEGURA)
🎯 Objetivo

Permitir reconstrução semântica incremental sem quebrar estado atual.

🔧 4.1 Replay baseado em PostgreSQL

Fonte única:

symbols
relationships
runtime traces
🔧 4.2 Replay NÃO recalcula identidade

Regra crítica:

Identity nunca é recalculada

🔧 4.3 Replay incremental

Permitir:

replay por arquivo
replay por módulo
replay por projeto
⚙️ FASE 5 — CONFIDENCE PROPAGATION (SEM ALTERAR SEMÂNTICA BASE)
🎯 Objetivo

Melhorar qualidade sem alterar estrutura.

🔧 5.1 Propagação baseada em relationships
confidence symbol → relationship → edge
🔧 5.2 Ajuste local, não global
não reescrever grafo inteiro
não reavaliar identidade
não recalcular estrutura
🧩 FASE 6 — OTIMIZAÇÃO DE PERSISTÊNCIA
🎯 Objetivo

Reduzir inconsistência entre runtime e Postgres.

🔧 6.1 Write-path único

Tudo deve passar por:

GraphRepositoryPostgresV2

🔧 6.2 Proibir writes diretos em runtime graph

Runtime graph:

somente leitura estrutural

🔧 6.3 Snapshot consistency layer

Snapshots:

por projeto
por versão de ingestão
🚫 REGRAS ABSOLUTAS (NÃO NEGOCIÁVEIS)
❌ PROIBIDO
reabrir IdentityRegistry
criar nova camada de identidade
duplicar GraphNodeV2 como fonte de verdade
criar “novo grafo paralelo”
introduzir novo modelo Symbol/Node/Edge
ignorar project_id
bypassar PostgreSQL
✔ OBRIGATÓRIO
evolução incremental
uso exclusivo do schema existente
respeito à separação semantic vs structural
PostgreSQL como verdade
GraphNodeV2 apenas projeção
🧭 ORDEM DE EXECUÇÃO RECOMENDADA
Fase 0 — auditoria
Fase 1 — project_id enforcement
Fase 2 — graph stabilization
Fase 6 — persistência única
Fase 3 — drift engine expansion
Fase 4 — replay engine
Fase 5 — confidence propagation
📌 RESULTADO ESPERADO DO PLANO

Ao final:

sistema multi-projeto real
grafo consistente com Postgres
identidade estável e congelada
runtime previsível
drift controlado e mensurável
evolução incremental sem reescrita estrutural

🧭 CHECKLIST TÉCNICO EXECUTÁVEL — CODE-RAG V2
🧱 1. MODULE: POSTGRESQL (SOURCE OF TRUTH LAYER)
🎯 Objetivo

Garantir consistência absoluta do estado persistido.

✔ 1.1 Schema enforcement global
 Confirmar project_id em:
 graph_v1.symbols
 graph_v1.relationships
 graph_runtime.call_traces
 graph_runtime.drift_events
 Validar NOT NULL em project_id
 Validar índices por project_id
✔ 1.2 Integrity constraints
 Garantir FK lógica entre:
symbols.project_id → projects.project_id
relationships.project_id → projects.project_id
 Detectar registros órfãos
 Corrigir incrementalmente (sem reset)
✔ 1.3 Write-path único
 Confirmar que SOMENTE GraphRepositoryPostgresV2 escreve:
 symbols
 relationships
 nodes
 edges
 Bloquear writes diretos de:
 GraphBuilderV2
 RuntimeExecutionGraphV2
✔ 1.4 Snapshot consistency
 Implementar snapshot por project_id
 Garantir versionamento incremental
 Validar reprodutibilidade parcial
🧠 2. MODULE: IDENTITY LAYER (CONGELADO)
🎯 Objetivo

Garantir estabilidade absoluta sem evolução.

✔ 2.1 Imutabilidade
 IdentityRegistryV2 NÃO pode ser alterado
 Nenhuma nova função de resolução adicionada
 Nenhum fallback paralelo permitido
✔ 2.2 Usage audit
 Verificar uso apenas em:
 resolução de símbolos
 linking estrutural
 Detectar qualquer tentativa de duplicação de identity logic
✔ 2.3 Isolation check
 Identity NÃO pode:
 persistir dados
 gerar IDs próprios
 competir com PostgreSQL
🧩 3. MODULE: SYMBOL CORE
🎯 Objetivo

Garantir coerência semântica com escopo de projeto.

✔ 3.1 project_id enforcement
 todo Symbol possui project_id
 SymbolExtractor injeta project_id automaticamente
 bloquear symbols sem projeto
✔ 3.2 Symbol integrity
 validar:
symbol_id único
symbol_path consistente
parent_symbol_id válido
✔ 3.3 Relationship binding
 garantir que symbols só geram relationships dentro do mesmo project_id
🔗 4. MODULE: RELATIONSHIP CORE
🎯 Objetivo

Garantir consistência semântica antes da transformação em grafo.

✔ 4.1 Relationship validity
 source_symbol_id existe
 target_symbol_id existe
 confidence entre 0–1
✔ 4.2 project scope enforcement
 relationships não cruzam project_id
✔ 4.3 semantic purity
 RelationshipCoreV2 não gera nodes
 RelationshipCoreV2 não gera edges
🧱 5. MODULE: GRAPH BUILDER V2
🎯 Objetivo

Converter semântica em estrutura sem introduzir identidade.

✔ 5.1 Mapping fixo
 Symbol → Node
 Relationship → Edge
✔ 5.2 No identity generation
 GraphBuilder NÃO cria IDs semânticos novos
 GraphBuilder NÃO altera identity resolution
✔ 5.3 project isolation
 nodes e edges sempre com project_id
 impedir merge cross-project
✔ 5.4 idempotência
 mesma entrada → mesmo grafo
 sem duplicação de nodes
🟪 6. MODULE: RUNTIME GRAPH
🎯 Objetivo

Garantir projeção segura e não-autoritativa.

✔ 6.1 GraphNodeV2 constraints
 NÃO gera identidade
 NÃO persiste
 NÃO cria IDs
 apenas view/projection
✔ 6.2 read-only enforcement
 runtime graph proibido de escrever no Postgres
✔ 6.3 projection consistency
 GraphNodeV2 sempre derivado de:
nodes
edges
🟨 7. MODULE: DRIFT ENGINE
🎯 Objetivo

Detectar inconsistências sem alterar estado.

✔ 7.1 detection coverage
 orphan symbols
 missing edges
 runtime mismatch
 stale projections
✔ 7.2 no auto-fix
 Drift Engine NÃO altera dados
 apenas gera eventos
✔ 7.3 drift events persistence
 salvar em graph_runtime.drift_events
 sempre com project_id
🔄 8. MODULE: SEMANTIC REPLAY ENGINE
🎯 Objetivo

Reconstituir estado semântico incremental.

✔ 8.1 source of truth
 PostgreSQL only
 nunca runtime graph como base
✔ 8.2 replay isolation
 replay por project_id
 replay por módulo
 replay por símbolo
✔ 8.3 identity constraint
 NÃO recalcular IdentityRegistry
🧠 9. MODULE: CONFIDENCE PROPAGATION
🎯 Objetivo

Melhorar qualidade sem alterar estrutura.

✔ 9.1 propagation rules
 symbol → relationship → edge
✔ 9.2 local-only updates
 nunca recalcular grafo inteiro
 nunca alterar identidade
⚙️ 10. MODULE: PROJECT INTELLIGENCE LAYER
🎯 Objetivo

Garantir multi-projeto real.

✔ 10.1 project detection
 detectar linguagem
 detectar framework
 detectar runtime
✔ 10.2 project assignment
 todo símbolo pertence a um project_id
✔ 10.3 isolation enforcement
 proibir vazamento entre projetos
🚨 11. GLOBAL SAFETY RULES (APLICA EM TODOS OS MÓDULOS)
❌ PROIBIDO
reabrir IdentityRegistry
criar nova ontologia
duplicar Symbol/Node/Edge model
criar graph paralelo
ignorar project_id
escrever fora do Postgres
alterar GraphNodeV2 como identidade
✔ OBRIGATÓRIO
incremental changes only
Postgres is source of truth
projection ≠ identity
semantic ≠ structural separation
no speculative architecture
📌 RESULTADO FINAL DO CHECKLIST

Se todos os módulos forem concluídos:

✔ sistema multi-projeto real
✔ grafo consistente com Postgres
✔ identidade estável e congelada
✔ runtime previsível e seguro
✔ drift monitorado
✔ evolução incremental sem ruptura