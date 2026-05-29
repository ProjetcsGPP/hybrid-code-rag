<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# entregar uma versão 2.1 com:

separação entre source_code_files, markup_files, style_files, config_files, data_files, text_files e binary_files,
e um primary_programming_language calculado só com código-fonte de verdade.
sim, eu gostaria disso.

Pronto — entreguei a versão 2.1 com separação explícita entre `source_code_files`, `markup_files`, `style_files`, `config_files`, `data_files`, `text_files` e `binary_files`, além de calcular `primary_programming_language` usando **apenas arquivos classificados como código-fonte real** .

## O que mudou

Cada arquivo agora recebe um campo `category`, que indica diretamente em qual grupo ele caiu, e isso evita misturar HTML, CSS, JSON e texto comum com linguagens de programação tradicionais . No resumo do repositório, o JSON passa a trazer contagens separadas por categoria e inclui tanto `primary_language` quanto `primary_programming_language`, sendo que o segundo considera só linguagens da lista de programação, como Python, JavaScript, TypeScript, Java, C\#, PHP, C, C++, Rust, Go, Shell e PowerShell .

## Como fica a consolidação

A análise do diretório agora monta estes números no `summary`:

- `source_code_files`
- `markup_files`
- `style_files`
- `config_files`
- `data_files`
- `text_files`
- `binary_files`
- `code_like_files`
- `primary_language`
- `primary_programming_language`
- `primary_framework`

Isso resolve exatamente o problema de uma pasta heterogênea, porque um repositório com muitos arquivos JSON e HTML não vai mais distorcer a linguagem de programação principal do projeto da mesma forma .

## Como usar

Instale as dependências com `pip install guesslang pygments`, porque essa versão continua usando a combinação híbrida de bibliotecas públicas mais heurísticas. Depois rode `python source_detector_v2_1.py caminho/do/repositorio` para diretório inteiro, ou `python source_detector_v2_1.py caminho/do/arquivo` para análise individual .[^1][^2]

## Resultado esperado

Se a pasta tiver Python, HTML, CSS, JSON, README e imagens, o resumo vai separar cada grupo e o `primary_programming_language` tenderá para Python, enquanto `primary_language` pode refletir qualquer linguagem dominante no conjunto geral, inclusive markup ou data, dependendo da distribuição . Isso deixa a leitura mais correta para cenários reais de repositório, especialmente quando há muitos arquivos auxiliares além do código-fonte principal .

## Arquivo entregue

O programa gerado é:

- `source_detector_v2_1.py`

Se você quiser, o próximo passo mais útil é eu fazer uma versão 2.2 com:

- exportação automática para arquivo `.json`,
- relatório resumido em `.md`,
- e uma opção para excluir categorias da análise principal.

<div align="center">⁂</div>

[^1]: https://guesslang.readthedocs.io

[^2]: https://stackoverflow.com/questions/325165/is-there-a-library-that-will-detect-the-source-code-language-of-a-block-of-code

