# DOC-11 — INVESTIGAÇÃO DOS SÍMBOLOS UNRESOLVED

## Objetivo

Registrar oficialmente as descobertas realizadas durante a análise dos símbolos classificados como UNRESOLVED após a estabilização da identidade semântica.

---

# Métricas Observadas

Relatório obtido:

```text
External Nodes: 1491
Unresolved Nodes: 406
```

---

# Classificação Inicial dos UNRESOLVED

Os símbolos identificados pertencem a diferentes categorias.

A partir deste momento é proibido tratar todos os UNRESOLVED como um único problema arquitetural.

---

# Categoria A — Builtins Python

Exemplos observados:

```text
len
str
int
bool
set
sorted
getattr
hasattr
```

## Diagnóstico

São símbolos conhecidos da linguagem.

Não representam falhas de identidade.

Representam ausência de classificação específica.

## Futuro Desejado

Exemplo:

```text
builtin::len
builtin::str
builtin::int
```

---

# Categoria B — Framework Symbols

Exemplos observados:

```text
transaction.atomic
timezone.now
JsonResponse
AnonymousUser
ValidationError
```

## Diagnóstico

São símbolos conhecidos do Django.

Não representam símbolos desconhecidos.

Representam ausência de resolução de framework.

---

# Categoria C — Attribute Chains

Exemplos observados:

```text
UserAuthzState.objects.get_or_create
UserRole.objects.filter.exists
Permission.objects.filter.values_list
```

## Diagnóstico

O símbolo-base é conhecido.

A cadeia de atributos não está sendo decomposta corretamente.

---

# Caso Investigado — UserAuthzState

Código analisado:

```python
from .models import UserAuthzState

UserAuthzState.objects.get_or_create(...)
```

Diagnóstico:

O símbolo UserAuthzState é interno.

Importado explicitamente.

Deveria ser resolvido pelo Identity Registry.

Conclusão:

Falha de resolução de atributos.

Não é falha de identidade.

---

# Caso Investigado — GROUP_PERMISSIONS

Exemplo:

```text
GROUP_PERMISSIONS.items
```

Diagnóstico:

GROUP_PERMISSIONS é constante interna.

O símbolo-base deveria ser resolvido.

O método items pertence ao tipo dicionário.

Conclusão:

Outro exemplo de falha de resolução de atributos.

---

# Categoria D — Local Symbols

Exemplo:

```text
_DryRunRollback
```

Código analisado:

```python
def _run_dry():

    class _DryRunRollback(Exception):
        pass
```

Diagnóstico:

Símbolo local.

Não pertence ao namespace global do módulo.

Conclusão:

Não representa falha arquitetural.

Representa ausência de suporte a símbolos locais.

---

# Conclusão Geral

A investigação demonstrou que:

* a identidade semântica permanece estável;
* o Identity Registry permanece funcional;
* os relatórios refletem adequadamente o estado atual do sistema.

Os problemas restantes concentram-se em mecanismos de resolução semântica avançada.

---

# Diretriz Oficial

Nenhuma intervenção futura poderá utilizar apenas a contagem de UNRESOLVED como indicador arquitetural.

Todo símbolo UNRESOLVED deve ser previamente classificado antes de qualquer decisão técnica.
