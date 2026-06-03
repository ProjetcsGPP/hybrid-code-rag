# DOC-07

# CONTRATOS OFICIAIS E FRONTEIRAS ARQUITETURAIS DO CODE-RAG V2

Versão: 1.0

Status: NORMATIVO

Objetivo:
Formalizar os contratos oficiais do CODE-RAG V2, definir responsabilidades por camada, eliminar ambiguidades arquiteturais e impedir interpretações divergentes em futuras sessões de desenvolvimento.

---

# 1. PRINCÍPIO FUNDAMENTAL

O CODE-RAG V2 é uma arquitetura em camadas.

Cada camada possui:

* uma responsabilidade exclusiva;
* uma entrada oficial;
* uma saída oficial;
* contratos permitidos;
* contratos proibidos.

Nenhuma camada pode assumir responsabilidade de outra.

---

# 2. VISÃO GERAL DO PIPELINE OFICIAL

FLUXO OFICIAL:

ARQUIVO FONTE
↓
AST EXTRACTION
↓
ChunkContract
↓
SYMBOL RESOLUTION
↓
SymbolContract
↓
SymbolV2
↓
SEMANTIC RESOLUTION
↓
RelationshipContract
↓
RelationshipV2
↓
STABILIZATION
↓
RelationshipV2 Normalizado
↓
GRAPH BUILD
↓
GraphNodeV2
GraphEdgeV2
↓
GRAPH STORAGE
↓
QUERY / RUNTIME / RAG

---

# 3. CLASSIFICAÇÃO OFICIAL DOS CONTRATOS

Existem apenas três categorias oficiais de contratos.

## Categoria A — Transport Contracts

Responsáveis por comunicação entre camadas.

Exemplos:

ChunkContract
SymbolContract
RelationshipContract
SemanticPayload

Regra:

Não possuem comportamento.

São apenas estruturas de transporte.

---

## Categoria B — Domain Models

Representam entidades reais do domínio.

Exemplos:

SymbolV2
RelationshipV2
GraphNodeV2
GraphEdgeV2

Regra:

Possuem semântica de negócio.

Podem ser persistidos.

Podem participar do grafo.

---

## Categoria C — Runtime Contracts

Representam contexto de execução.

Exemplos:

RuntimeContextV2
SemanticRuntimeContext
NamespaceContext
RepositorySnapshot

Regra:

Nunca representam símbolos.

Nunca representam relacionamentos.

Nunca entram no grafo.

Representam apenas contexto operacional.

---

# 4. CAMADA AST

Responsabilidade:

Converter código-fonte em estrutura intermediária.

Entrada:

arquivo.py

Saída obrigatória:

ChunkContract

Arquivo responsável:

ASTChunker

Proibido:

Criar SymbolV2

Criar RelationshipV2

Criar GraphNodeV2

Criar GraphEdgeV2

Persistir qualquer informação

Modificar IdentityRegistry

Modificar GraphCore

Resultado obrigatório:

List[ChunkContract]

---

# 5. CONTRATO OFICIAL ChunkContract

Representa uma unidade semântica mínima extraída do código.

Campos obrigatórios:

id
file
name
type
raw_calls
metadata

Objetivo:

Transportar dados da AST para as camadas superiores.

Validade:

Apenas entre AST e Symbol Resolution.

Nunca deve ser persistido.

Nunca deve entrar no grafo.

---

# 6. CAMADA SYMBOL RESOLUTION

Responsabilidade:

Transformar ChunkContract em representação simbólica.

Entrada oficial:

ChunkContract

Saída intermediária:

SymbolContract

Saída final:

SymbolV2

Arquivos associados:

SemanticAdapter

SymbolAdapter

SymbolCoreV2

---

# 7. CONTRATO OFICIAL SymbolContract

Objetivo:

Representação estável de símbolo.

Campos:

id
name
type
file_path
canonical
parent
metadata

Função:

Servir de ponte entre AST e domínio.

Não participa do grafo.

Não possui identidade global.

Não deve ser persistido.

---

# 8. MODELO OFICIAL SymbolV2

Representa um símbolo real do sistema.

Exemplos:

Classe

Método

Função

Módulo

Propriedades obrigatórias:

id

canonical

name

type

file_path

metadata

Responsável por:

IdentityRegistry

IdentityService

GraphBuilder

Pode ser persistido.

Pode virar GraphNodeV2.

---

# 9. CAMADA SEMANTIC RESOLUTION

Responsabilidade:

Descobrir relações entre símbolos.

Entrada:

ChunkContract

SemanticContextV2

Tabela de símbolos

Saída:

RelationshipContract

Posteriormente:

RelationshipV2

Arquivos oficiais:

RelationshipCoreV2

RelationshipResolverV2

AssignmentResolverV2

SemanticContextV2

SemanticInferenceEngineV2

---

# 10. CONTRATO OFICIAL RelationshipContract

Representação transportável de uma relação.

Campos:

id
source
target
type
layer
status
dispatch
raw_call
confidence
provenance
framework_hint
semantic_owner
metadata

Objetivo:

Transportar inferências semânticas.

Não deve ser persistido.

Não entra diretamente no grafo.

---

# 11. MODELO OFICIAL RelationshipV2

Representa uma relação validada.

Exemplos:

CALLS

IMPORTS

INHERITS

USES

FRAMEWORK_CALL

ORM_QUERY

Características:

Identidade determinística

Possui source

Possui target

Possui metadata

Pode ser persistido

Pode virar GraphEdgeV2

---

# 12. CAMADA DE ESTADO SEMÂNTICO

Responsabilidade:

Resolver contexto local temporário.

Arquivos oficiais:

VariableState

SemanticContextV2

AssignmentResolverV2

SemanticInferenceEngineV2

ConfidenceEngineV2

Função:

Resolver significado local.

Exemplo:

repo = UserRepository()

repo.save()

Transformação:

repo
↓
UserRepository
↓
UserRepository.save

Importante:

Não modifica o grafo.

Não grava identidade.

Não persiste dados.

---

# 13. CAMADA DE STABILIZATION

Objetivo:

Normalizar resultados semânticos antes do Graph Builder.

Arquivos oficiais:

canonical_reconciliation.py

edge_deduplicator.py

graph_normalizer_v2.py

normalization_pass.py

normalization_result.py

unresolved_cleanup.py

Entrada:

List[RelationshipV2]

Saída:

List[RelationshipV2]

Responsabilidades:

Deduplicação

Reconciliação de canonical

Remoção de órfãos

Remoção de inconsistências

Normalização de identidade

Importante:

Nenhum RelationshipV2 deve entrar no GraphBuilder sem passar pela estabilização.

---

# 14. CAMADA GRAPH BUILD

Responsabilidade:

Converter domínio em estrutura de grafo.

Entrada:

BuildContextV2

Conteúdo:

List[SymbolV2]

List[RelationshipV2]

Saída:

GraphNodeV2

GraphEdgeV2

Arquivo oficial:

GraphBuilderV2

---

# 15. MODELOS DE GRAFO

GraphNodeV2

Representa:

nó persistível do grafo

GraphEdgeV2

Representa:

aresta persistível do grafo

Somente estes objetos entram em GraphCore.

Nenhum SymbolContract entra.

Nenhum RelationshipContract entra.

---

# 16. IDENTIDADE OFICIAL

Autoridade única:

IdentityRegistryV2

Responsabilidades:

Registrar símbolos

Resolver símbolos

Garantir unicidade

Mapear canonical

Mapear ids

Proibido:

Criar identidade fora do registry

Criar UUID arbitrário

Duplicar tabelas de identidade

---

# 17. RUNTIME OFICIAL

Objetivo:

Controlar execução.

Não representa domínio.

Arquivos oficiais:

RuntimeContextV2

NamespaceContext

SemanticRuntimeContext

RepositorySnapshot

---

# 18. NamespaceContext

Representa:

Workspace

Projeto

Repositório

Módulo

Branch

Função:

Construir namespace estável.

Não entra no grafo.

---

# 19. SemanticRuntimeContext

Representa:

Contexto completo da análise.

Contém:

workspace

project

repository

branch

snapshot

language profile

framework profile

Objetivo:

Permitir múltiplos repositórios simultâneos.

---

# 20. RepositorySnapshot

Representa:

Estado congelado de um repositório.

Função:

Replay

Versionamento

Comparação temporal

Análise histórica

---

# 21. GERENCIADORES DE RUNTIME

Componentes válidos:

WorkspaceManager

ProjectManager

RepositoryManager

SnapshotManager

Função:

Administrar escopo operacional.

Não manipulam símbolos.

Não manipulam relacionamentos.

Não manipulam grafo.

---

# 22. COMPONENTES LEGACY

São aceitos temporariamente:

StructuralIndexer

Legacy Extractors

Legacy Resolvers

Regra:

Todo componente legado deve terminar produzindo contratos oficiais.

Nunca deve escrever diretamente no grafo V2.

---

# 23. COMPONENTES EXPERIMENTAIS

Incluem:

RuntimeExecutionGraphV2

SemanticExecutionTraceAnalyzerV2

ScopedRuntimeGraphV2

Status:

Experimental

Não fazem parte do pipeline principal.

Podem evoluir separadamente.

---

# 24. COMPONENTES ÓRFÃOS

Definição:

Arquivo existente sem consumidor conhecido.

Critério:

Nenhum import ativo

Nenhuma integração oficial

Nenhuma chamada pelo PipelineBridge

Processo:

Catalogar

Classificar

Integrar ou remover

Nunca manter indefinidamente

---

# 25. PIPELINEBRIDGE V2

Responsabilidade:

Orquestração.

Apenas isso.

PipelineBridge:

Pode chamar:

AST

Symbol

Semantic

Stabilization

GraphBuilder

Não pode:

Executar lógica semântica própria

Executar persistência própria

Executar resolução própria

---

# 26. CONTRACT ENFORCER

Torna-se obrigatório.

Toda fronteira entre camadas deve validar contratos.

Exemplos:

AST → ChunkContract

ChunkContract → SymbolContract

RelationshipContract → RelationshipV2

RelationshipV2 → GraphBuilder

Qualquer violação:

ContractViolation

---

# 27. REGRA DE OURO

Nenhuma camada pode consumir estruturas internas da próxima camada.

Cada camada deve conhecer apenas:

seu contrato de entrada

seu contrato de saída

e nada além disso.

---

# 28. META FINAL DA V2

O CODE-RAG V2 deve ser:

Multi-linguagem

Multi-framework

Multi-repositório

Determinístico

Incremental

Auditável

Orientado a contratos

Independente de Python

Capaz de absorver conhecimento do Legacy sem absorver acoplamentos do Legacy.
