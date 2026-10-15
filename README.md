# Organizador Financeiro Pessoal CLI & Dashboard Analítico

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Versão do Python" /> <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite3" /> <img src="https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black" alt="Power BI" /> <img src="https://img.shields.io/badge/DAX-Data%20Analysis-orange?style=for-the-badge" alt="DAX" /> <img src="https://img.shields.io/badge/Interface-CLI%20Terminal-black?style=for-the-badge" alt="Interface CLI" /> <img src="https://img.shields.io/badge/Licença-MIT-green?style=for-the-badge" alt="Licença MIT" />

Sistema em linha de comando (CLI) para controle financeiro pessoal, desenvolvido em Python modular com SQLite, emissão de relatórios mensais, exportação de dados em CSV e integração direta com dashboard interativo em Power BI.

## Sobre o Projeto

O **Organizador Financeiro Pessoal** é uma aplicação voltada para quem busca registrar e acompanhar receitas e despesas de forma prática diretamente pelo terminal, aliando a agilidade de um sistema CLI à robustez analítica do Business Intelligence.

O sistema organiza movimentações por categorias, monitora saldos, calcula a distribuição percentual de despesas por categoria e permite a exportação do histórico completo via CSV (`extrato_financeiro.csv`). Integrado a ele, um dashboard interativo no **Power BI** consome esses dados para fornecer análises de evolução temporal diária, ranking de despesas por categoria e acompanhamento em tempo real dos principais KPIs financeiros.

A aplicação foi construída com foco em boas práticas de engenharia de software e análise de dados, separando claramente as camadas de interface, fluxo de controle, persistência relacional e modelagem analítica.

---

## Demonstração

### Menu Principal (CLI)
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

### Dashboard Analítico (Power BI)

![Prévia do Dashboard Financeiro](power_bi/assets/preview_dashboard.png)

O relatório foi desenvolvido em **Dark Theme** personalizado (com layout de suporte desenhado no Canva), otimizando a hierarquia visual e legibilidade dos dados:
* **KPIs Centrais:** Cards dinâmicos com Total de Receitas, Total de Despesas, Saldo Líquido e Volume de Lançamentos do período.
* **Evolução Diária:** Gráfico de linhas temporal comparando a curva de entradas (verde) versus despesas (coral).
* **Despesas por Categoria:** Gráfico horizontal ordenado do maior para o menor desembolso, identificando gargalos financeiros.
* **Últimas Movimentações:** Exibição contextual da última receita e última despesa registradas com descrição, data e formatação condicional de sinal.
* **Segmentação Temporal:** Filtro de período entre datas alimentado por dimensão de calendário dedicada.

---

## Funcionalidades

### Aplicação Python (CLI)
- **Lançamentos com Data Flexível:** Registre receitas e despesas informando uma data específica (`AAAA-MM-DD`) ou simplesmente pressionando `<Enter>` para preencher automaticamente com a data atual.
- **Categorização Personalizável:** Conjunto nativo de categorias padrão (*Salário, Alimentação, Transporte, Moradia, etc.*) com suporte para cadastro dinâmico de novas categorias classificadas como `RECEITA` ou `DESPESA`.
- **Relatório de Fechamento Mensal:** Consulta por mês de referência (`AAAA-MM`) ou mês corrente, detalhando receitas, despesas, saldo líquido e a representação percentual de cada categoria nos gastos.
- **Detalhamento de Transações do Mês:** Exibição cronológica de todas as despesas individuais lançadas dentro do período filtrado.
- **Extrato Recente:** Visualização rápida das 15 transações mais recentes registradas.
- **Exclusão com Confirmação:** Remoção segura de registros por ID com checagem de existência e confirmação prévia do usuário.
- **Exportação para CSV:** Geração do arquivo `extrato_financeiro.csv` estruturado com separador `;` e codificado em `utf-8-sig`, garantindo compatibilidade direta com Power BI, Excel e Google Sheets.

### Análise e Modelagem (Power BI)
- **Template Reutilizável (`.pbit`):** Arquivo de modelo distribuído sem dados sensíveis embutidos; conecta-se imediatamente ao CSV gerado pela CLI.
- **Star Schema com Dimensão Calendário (`dCalendario`):** Tabela de datas calculada via DAX com granularidade de ano, mês, ano-mês e dia da semana, garantindo filtros contínuos e inteligência temporal.
- **Medidas DAX Padronizadas:** Cálculos dinâmicos isolados em tabela dedicada (`_Medidas`), incluindo formatação de moeda com sinal (`+ R$` / `- R$`), cores hexadecimais condicionais e busca de últimos registros via `TOPN`.

---

## Arquitetura e Engenharia de Dados

O projeto adota separação clara de responsabilidades entre interface, orquestração, banco relacional e camada de consumo analítico:

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
                              │
                              │ Opção 7 (Exportar CSV)
                              ▼
                     [ extrato_financeiro.csv ]
                              │
                              ▼
                 ┌──────────────────────────┐
                 │   Power BI (.pbit)       │
                 │   Modelo Star Schema     │
                 │   dCalendario 1:N Fato   │
                 └──────────────────────────┘
```

---

## Modelo de Dados (SQLite)

O banco de dados SQLite opera com suporte a chaves estrangeiras ativado (`PRAGMA foreign_keys = ON`) e restrições de integridade (*CHECK constraints*):

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
* **`categorias` (1) ──── (N) `transacoes`**: Uma categoria pode conter múltiplas movimentações vinculadas, enquanto cada transação referencia obrigatoriamente uma única categoria válida via chave estrangeira (`categoria_id`).
* **Índices:** Os índices criados sobre as colunas `data_registro` e `categoria_id` otimizam consultas, ordenações e operações de junção (`JOIN`) frequentes sobre o histórico financeiro.

---

## 📂 Estrutura de Arquivos

```text
organizador-financeiro-python/
│
├── .gitignore
├── .gitattributes
├── LICENSE
├── README.md
│
├── database.py                   # Gerenciamento do SQLite, DDL, queries e exportação CSV
├── interface.py                  # Formatação de terminal, cores ANSI e validações
├── main.py                       # Ponto de entrada (entrypoint) e loop principal
│
└── power_bi/                     # Módulo de Business Intelligence
    ├── template/
    │   └── VisaoGeralFinancas.pbit  # Template do Power BI pronto para conexão
    ├── assets/
    │   ├── DashboardWallpaper.png # Background customizado (Canva)
    │   └── preview_dashboard.png  # Captura demonstrativa para documentação
    └── data/
        └── extrato_exemplo.csv    # Dataset fictício de exemplo (25 lançamentos)
```

---

## Como Executar

### 1. Aplicação Python
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/organizador-financeiro-python.git
   cd organizador-financeiro-python
   ```
2. Execute a aplicação (requer Python 3.8+):
   ```bash
   python main.py
   ```
3. Registre movimentações e utilize a **Opção 7** para exportar seu `extrato_financeiro.csv`.

### 2. Abrir o Dashboard no Power BI
O modelo analítico foi configurado para carregar diretamente a base demonstrativa segura (extrato_exemplo.csv), permitindo explorar o painel de imediato:

1. Acesse a pasta power_bi/template/ e abra o arquivo VisaoGeralFinancas.pbit no Power BI Desktop.
2. O dashboard abrirá pré-conectado à base de demonstração localizada em power_bi/data/extrato_exemplo.csv, com todos os visuais, cartões e métricas DAX calculados.
3. Para usar com os seus dados pessoais gerados pelo Python:
   - No Power BI Desktop, vá em Página Inicial > Transformar Dados (Power Query). 
   - Na etapa Fonte da consulta extrato_financeiro, altere o caminho do arquivo para apontar para o seu extrato_financeiro.csv na raiz do projeto. 
   - Clique em Fechar e Aplicar.

---

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).