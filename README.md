# App de Finanças Simples

Aplicativo em linha de comando para registrar entradas e saídas de dinheiro
em um arquivo JSON local. A ferramenta ajuda a acompanhar o saldo atual e
os totais movimentados em cada categoria (entradas e saídas).

## Requisitos

- Python 3.10 ou superior

## Instalação

1. Crie e ative um ambiente virtual opcional:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\\Scripts\\activate   # Windows
   ```
2. Instale o projeto (incluindo dependências de desenvolvimento):
   ```bash
   pip install -e .[dev]
   ```

## Uso

Após a instalação, um comando `finance-app` estará disponível. Também é
possível utilizar o módulo diretamente com `python -m finance_app.cli`.

### Adicionar transações

```bash
finance-app adicionar entrada "Salário" 3500
finance-app adicionar saida "Supermercado" 220.75
```

### Listar transações

```bash
finance-app listar
```

Saída esperada:

```
#  Data e hora           Tipo     Valor        Descrição
------------------------------------------------------------
 1  2023-01-10T09:00:00  Entrada  R$ 3.500,00  Salário
 2  2023-01-12T18:30:00  Saída    R$ 220,75    Supermercado
```

### Resumo financeiro

```bash
finance-app resumo
```

```
Resumo financeiro
------------------------------
Entradas: R$ 3.500,00
Saídas:   R$ 220,75
Saldo:    R$ 3.279,25
```

Por padrão os dados são armazenados no arquivo `dados_financeiros.json`
no diretório atual. Utilize a opção `--arquivo` para informar outro
local.

## Executar testes

```bash
pytest
```
