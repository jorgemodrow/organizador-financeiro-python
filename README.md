# Organizador Financeiro Pessoal CLI

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Versão do Python" /> <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite3" /> <img src="https://img.shields.io/badge/Interface-CLI%20Terminal-black?style=for-the-badge" alt="Interface CLI" /> <img src="https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge" alt="Licença MIT" />

Sistema em linha de comando (CLI) para controle financeiro pessoal, desenvolvido em Python modular com SQLite, emissão de relatórios mensais e exportação de dados em CSV.

## Sobre o Projeto

O **Organizador Financeiro Pessoal** é uma aplicação voltada para quem busca registrar e acompanhar receitas e despesas de forma prática diretamente pelo terminal.

O sistema organiza movimentações por categorias, monitora saldos, calcula a distribuição percentual de despesas por categoria e permite a exportação do histórico completo para planilhas e ferramentas analíticas via CSV.

A aplicação foi construída com foco em boas práticas de modularização, separando as camadas de interface, fluxo de controle e persistência de dados.

## Demonstração

### Menu Principal
```text
=================================================================
                 ORGANIZADOR FINANCEIRO PESSOAL
=================================================================
1 - Lançar Novo Gasto / Despesa
2 - Lançar Nova Receita / Ganho
3 - Ver Fechamento Mensal
4 - Ver Últimos Lançamentos (Extrato)
5 - Excluir Transação
6 - Cadastrar Categoria Personalizada
7 - Exportar Dados para CSV (Excel / BI)
8 - Sair
-----------------------------------------------------------------
Sua opção: 3

=================================================================
                  CONSULTA DE FECHAMENTO MENSAL
=================================================================
Mês de referência (AAAA-MM ou <Enter> para o mês atual): 2026-10
=================================================================
                    FECHAMENTO MENSAL - [2026-10]
=================================================================
Total de Entradas (Receitas): R$    3500.00
Total de Saídas   (Despesas): R$    1420.50
SALDO DO MÊS: R$    2079.50

=================================================================
                     DISTRIBUIÇÃO DOS GASTOS
=================================================================
CATEGORIA                 TOTAL (R$)   % DO MÊS
-----------------------------------------------------------------
Moradia                   R$   800.00     56.3%
Alimentação               R$   450.50     31.7%
Transporte                R$   170.00     12.0%

=================================================================
                         TODOS OS GASTOS
=================================================================
DATA        DESCRIÇÃO              CATEGORIA       VALOR (R$)
-----------------------------------------------------------------
2026-10-02  Aluguel Residencial    Moradia         R$   800.00
2026-10-03  Supermercado           Alimentação     R$   320.50
2026-10-04  Recarga Cartão         Transporte      R$   170.00
2026-10-05  Almoço Restaurante     Alimentação     R$   130.00
-----------------------------------------------------------------

Pressione <Enter> para voltar ao menu
```

## Funcionalidades
- Lançamentos com Data Flexível: Registre receitas e despesas informando uma data específica (AAAA-MM-DD) ou simplesmente pressionando <Enter> para preencher automaticamente com a data atual.
- Categorização Personalizável: Conjunto nativo de categorias padrão (Salário, Alimentação, Transporte, Moradia, etc.) com suporte para cadastro de novas categorias classificadas como RECEITA ou DESPESA.
- Relatório de Fechamento Mensal: Consulta por qualquer mês de referência (AAAA-MM) ou mês corrente, detalhando receitas, despesas, saldo líquido e a representação percentual de cada categoria nos gastos.
- Detalhamento de Transações do Mês: Exibição cronológica de todas as despesas individuais lançadas dentro do período filtrado.
- Extrato Recente: Visualização rápida das 15 transações mais recentes registradas.
- Exclusão com Confirmação: Remoção segura de registros por ID com checagem de existência e confirmação prévia do usuário.
- Exportação para CSV: Geração do arquivo extrato_financeiro.csv codificado em utf-8-sig, garantindo compatibilidade direta com planilhas (Excel, Google Sheets) e ferramentas de análise.

## Arquitetura e Fluxo de Execução

O projeto adota separação clara de responsabilidades entre interface, orquestração e banco de dados:

```text
[ Usuário ]
    │
    ▼
┌──────────────────┐
│     main.py      │  ── Controle de fluxo, menu e orquestração das operações
└─────────┬────────┘
          │
    ┌─────┴────────────────┐
    ▼                      ▼
┌─────────────────┐  ┌─────────────────┐
│  interface.py   │  │   database.py   │
│                 │  │                 │
│ Formatação,     │  │ Queries SQL,    │
│ cores ANSI e    │  │ índices e       │
│ validação de I/O│  │ conexão SQLite  │
└─────────────────┘  └────────┬────────┘
                              │
                              ▼
                     [( financas_pessoais.db )]
```

## Modelo de Dados

O banco de dados SQLite opera com suporte a chaves estrangeiras ativado (PRAGMA foreign_keys = ON) e restrições de integridade (CHECK constraints):

```sql
    CREATE TABLE categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('RECEITA', 'DESPESA'))
    );

    CREATE TABLE transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL CHECK (valor > 0),
        data_registro TEXT NOT NULL,
        categoria_id INTEGER NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    );

    CREATE INDEX idx_transacoes_data ON transacoes(data_registro);
    CREATE INDEX idx_transacoes_cat ON transacoes(categoria_id);
```

### Relacionamento e Índices:
* **`categorias` (1) ──── (N) `transacoes`**: Uma categoria pode conter múltiplas movimentações vinculadas, enquanto cada transação referencia obrigatoriamente uma única categoria válida via chave estrangeira (`categoria_id`)[cite: 7].
* **Índices:** Os índices criados sobre as colunas `data_registro` e `categoria_id` auxiliam consultas, ordenações e operações de junção (`JOIN`) frequentes sobre o histórico financeiro.

## 📂 Estrutura de Arquivos

```text
├── database.py     # Gerenciamento do SQLite, inicialização e consultas
├── interface.py    # Utilitários de terminal, cores ANSI e leitura de entradas
├── main.py         # Ponto de entrada (entrypoint) e orquestração do menu
├── LICENSE         # Arquivo com os termos da licença MIT
└── README.md       # Documentação do projeto
```

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).
