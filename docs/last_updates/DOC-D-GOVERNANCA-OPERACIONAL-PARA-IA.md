# DOC-D — GOVERNANÇA OPERACIONAL PARA IA

Status: ATIVO

Prioridade: ALTA

Leitura Obrigatória: SIM

Objetivo:

Complementar o DOC-A, o DOC-B e o DOC-C com um conjunto mínimo de controles operacionais voltados à continuidade entre chats, redução de inferência indevida, estabilidade semântica e prevenção de reabertura de decisões já encerradas.

Este documento existe para reduzir ambiguidade sem voltar a expandir excessivamente a documentação do projeto.

---

# 1. POSIÇÃO OFICIAL DESTE DOCUMENTO

Este documento NÃO substitui:

* DOC-A — Constituição Arquitetural Oficial;
* DOC-B — Estado Operacional Oficial;
* DOC-C — Roadmap Oficial e Protocolo de Continuidade.

Este documento complementa os três.

Sua função é:

* reforçar controles normativos de continuidade;
* consolidar terminologia operacional crítica;
* registrar decisões congeladas de alto impacto;
* padronizar o comportamento esperado de futuras IAs e chats.

---

# 2. FINALIDADE PRÁTICA

Este documento foi criado para evitar os problemas já observados anteriormente:

* perda de contexto entre chats;
* reabertura de decisões encerradas;
* inferência livre sem validação no código real;
* confusão entre camadas arquiteturais;
* uso inconsistente dos termos STRICT, EXTERNAL, UNRESOLVED e PARTIAL;
* propostas corretas em teoria, mas incompatíveis com o estado real do repositório;
* criação de componentes, contratos ou fluxos não autorizados.

---

# 3. MATRIZ OFICIAL DE DECISÕES CONGELADAS

As seguintes decisões são consideradas CONGELADAS.

Somente podem ser reabertas mediante evidência técnica obtida a partir do código real, testes, auditoria ou falha comprovada.

| Tema | Decisão congelada | Status de reabertura |
|------|-------------------|----------------------|
| Identidade | Identity Registry permanece autoridade central de identidade | PROIBIDA sem evidência |
| Canonical Identity | Identidade canônica permanece consolidada | PROIBIDA sem evidência |
| Path Identity | Identidade baseada em path não deve ser reintroduzida como autoridade principal | PROIBIDA sem evidência |
| Aliases | Aliases não podem voltar a ser identidade principal | PROIBIDA sem evidência |
| GraphBuilder | GraphBuilder continua sendo autoridade estrutural | PROIBIDA sem evidência |
| Relationship Layer | Relationship Layer continua sendo autoridade semântica local | PROIBIDA sem evidência |
| Reconciliation | Semantic Reconciliation só atua pós Contract Validation | PROIBIDA sem evidência |
| Ingestão | Não resolver tudo durante a ingestão | PROIBIDA sem evidência |
| Contracts First | Migração continua incremental, sem refatoração massiva | PROIBIDA sem evidência |
| Legacy | Legacy continua sendo referência comportamental, não autoridade arquitetural final | PROIBIDA sem evidência |

---

# 4. GLOSSÁRIO OPERACIONAL DE ESTADOS

Este glossário deve ser usado de forma consistente em toda análise futura.

## STRICT

Símbolo, relacionamento ou resolução considerada semanticamente vinculada ao domínio conhecido do sistema.

Implica:

* vínculo canônico válido;
* compatibilidade com a Identity Layer;
* possibilidade de participação confiável no grafo.

---

## EXTERNAL

Referência identificada pelo pipeline, porém ainda não vinculada a um símbolo interno resolvido.

Pode representar:

* framework;
* stdlib;
* third-party;
* símbolo ainda não reconciliado;
* cadeia parcialmente compreendida.

EXTERNAL não significa automaticamente erro.

---

## UNRESOLVED

Referência ainda não promovida semanticamente.

Pode significar:

* ausência de binding atual;
* falta de classificação específica;
* limitação de contexto local;
* necessidade de reconciliação posterior.

UNRESOLVED não significa automaticamente símbolo desconhecido.

---

## PARTIAL

Resolução incompleta, mas não totalmente cega.

Indica que parte da estrutura foi compreendida, porém ainda não houve promoção para vínculo canônico confiável.

---

## PROMOTED

Elemento previamente EXTERNAL, UNRESOLVED ou PARTIAL que, após reconciliação válida, foi promovido para resolução semanticamente confiável.

---

## FROZEN

Decisão, componente ou regra cujo debate foi encerrado.

Somente pode ser reaberto por evidência técnica.

---

## ACTIVE

Componente ou camada atualmente integrante do pipeline oficial.

---

## ORPHAN

Arquivo, componente ou estrutura sem consumidor ativo comprovado no pipeline atual.

Não deve ser removido automaticamente.

Deve antes ser classificado.

---

## EXPERIMENTAL

Componente válido, porém fora do pipeline principal.

Pode evoluir separadamente sem redefinir o estado oficial do sistema.

---

# 5. TABELA OFICIAL DE FRONTEIRAS ENTRE CAMADAS

| Camada | Pode fazer | Não pode fazer |
|--------|------------|----------------|
| AST Layer | Extrair estrutura intermediária | Criar identidade, criar grafo, persistir, resolver semântica final |
| Symbol Layer | Produzir representação simbólica | Criar grafo estrutural, persistir decisões finais fora do fluxo oficial |
| Semantic / Relationship Layer | Inferir relações e contexto semântico local | Criar identidade paralela, decidir persistência final, sobrescrever GraphBuilder |
| Resolution Layer | Apoiar binding e resolução local | Tornar-se autoridade estrutural ou de persistência |
| Identity Layer | Resolver, indexar e garantir unicidade canônica | Decidir semântica, modelar grafo, invadir runtime sem contrato |
| Graph Layer | Projetar domínio em estrutura persistível | Resolver significado, reinterpretar identidade, inventar semântica |
| Persistence Layer | Registrar estado oficial canônico | Reinterpretar domínio ou substituir camadas superiores |
| Reconciliation Layer | Reconciliar EXTERNAL / UNRESOLVED / PARTIAL após validação | Criar identidade nova, alterar Registry arbitrariamente, alterar GraphBuilder, sobrescrever decisões já STRICT |
| Runtime / Context | Manter contexto operacional | Virar símbolo, relacionamento ou autoridade de domínio |

---

# 6. PROTOCOLO MÍNIMO PARA NOVOS CHATS

Todo novo chat deve seguir esta ordem mínima.

## Etapa 1 — Leitura obrigatória

Ler obrigatoriamente:

1. DOC-A
2. DOC-B
3. DOC-C
4. DOC-D

---

## Etapa 2 — Confirmação obrigatória

Antes de qualquer proposta técnica, o chat deve confirmar explicitamente:

```text
DOCUMENTOS LIDOS
ESTADO COMPREENDIDO
FASE IDENTIFICADA
DECISÕES CONGELADAS RESPEITADAS
AGUARDANDO ÁRVORE DE DIRETÓRIOS E ARQUIVOS
```

---

## Etapa 3 — Evidência obrigatória

Antes de propor implementação, o chat deve:

* solicitar árvore de diretórios;
* solicitar arquivos afetados;
* ler código real;
* validar imports, consumidores e pontos de entrada;
* identificar impacto arquitetural;
* somente então propor plano incremental.

---

# 7. REGRA OFICIAL DE INTERPRETAÇÃO DOS RELATÓRIOS

Nenhum relatório poderá ser interpretado apenas por contagem bruta.

As seguintes regras passam a ser obrigatórias:

* contagem de UNRESOLVED não prova falha arquitetural por si só;
* contagem de EXTERNAL não prova erro de pipeline por si só;
* todo grupo relevante deve ser classificado antes de qualquer decisão técnica;
* builtins, frameworks, attribute chains e símbolos locais devem ser separados antes de qualquer conclusão.

---

# 8. REGRA OFICIAL DE PROPOSTA TÉCNICA

Nenhuma proposta será considerada válida se:

* inventar componente não autorizado sem necessidade comprovada;
* inferir comportamento sem ler o código real;
* reabrir tema congelado sem evidência;
* confundir semântica com estrutura;
* confundir identidade com persistência;
* confundir runtime com domínio;
* propor refatoração massiva sem justificativa auditável.

Toda proposta válida deve informar explicitamente:

* problema observado;
* evidência encontrada no código;
* camada impactada;
* risco arquitetural;
* plano incremental;
* critério de validação.

---

# 9. REGISTRO ENXUTO DE MUDANÇA OBRIGATÓRIO

A partir deste documento, cada evolução relevante pode ser registrada de forma curta, sem gerar um novo documento narrativo extenso.

Formato recomendado:

## CHANGELOG DE FASE

### ID

FASE-3-YYYY-MM-DD-NN

### Objetivo

Descrever o objetivo específico da mudança.

### Evidência

Arquivos analisados, testes, grep, auditoria ou relatórios utilizados.

### Alterações

Lista curta dos arquivos e mudanças executadas.

### Decisão

O que foi decidido e por quê.

### Resultado

PASS / FAIL / PARCIAL.

### Impacto arquitetural

Qual camada foi afetada e quais ficaram protegidas.

### Próximo passo autorizado

Qual é a próxima atividade válida após esta mudança.

---

# 10. NÍVEL DE PRIORIDADE DE INFORMAÇÃO PARA IA

Quando houver limitação de contexto, a prioridade de retenção para qualquer IA deve ser:

## Prioridade 1 — obrigatório sempre manter

* missão do projeto;
* arquitetura oficial;
* decisões congeladas;
* fase atual;
* componentes congelados;
* regra de leitura do código real.

## Prioridade 2 — manter quando relevante para implementação

* métricas operacionais atuais;
* lista de vazamentos conhecidos;
* classificação de unresolved;
* critérios de aceitação da fase.

## Prioridade 3 — consultar sob demanda

* histórico detalhado de auditorias antigas;
* justificativas narrativas mais longas;
* documentos superados por consolidação posterior.

---

# 11. DOCUMENTOS OFICIAIS DE ENTRADA

Para continuidade normal do projeto, a pilha mínima oficial passa a ser:

1. DOC-A — Constituição Arquitetural Oficial
2. DOC-B — Estado Operacional Oficial
3. DOC-C — Roadmap Oficial e Protocolo de Continuidade
4. DOC-D — Governança Operacional para IA

Documentos históricos e evolutivos anteriores permanecem como referência complementar, mas deixam de ser base obrigatória de entrada.

---

# 12. REGRA FINAL

O objetivo deste documento não é aumentar a documentação.

O objetivo é impedir regressão de contexto.

A documentação oficial do CODE-RAG deve permanecer:

* curta o suficiente para ser reutilizável por IA;
* forte o suficiente para impedir inferência livre;
* precisa o suficiente para proteger a arquitetura;
* operacional o suficiente para orientar evolução incremental real.
