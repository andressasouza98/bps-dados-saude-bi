# 📊 Guia de Implementação e Arquitetura do Dashboard - Looker Studio

## 1. Fonte de Dados e Pipeline de Ingestão (BigQuery)

### 1.1 Arquitetura da Solução

- **Base de Origem:** `BPS_20_26_AndressaAlvesDeSouza.csv` (342.697 registros | 25 colunas).
- **Otimização de Armazenamento:** Devido às restrições de upload direto do BigQuery Sandbox (limite de 100 MB para CSVs via navegador), a base foi convertida para o formato colunar **Apache Parquet** (`bps_consolidado.parquet`), atingindo **16,3 MB** (~80% de taxa de compressão) com integridade total de linhas e preservação dos tipos de dados.
- **Pipeline de Carga Automatizada:** Ingestão realizada via script Python (`src/carregar_bigquery.py`) utilizando a API oficial `google-cloud-bigquery` e autenticação com credenciais de aplicação (`gcloud auth application-default login`).
- **Destino Analítico:** Projeto `projeto-bps` | Dataset `dados_bps` | Tabela `bps_consolidado` (342.697 linhas validadas).
- **Conexão no Looker Studio:** Conector nativo **BigQuery** -> `projeto-bps` -> `dados_bps` -> `bps_consolidado`.

### 1.2 Registro de Decisão Técnica (ADR)

- **Desafio:** Erro inesperado e bloqueio de limite de arquivo (100 MB) no upload pelo console web do GCP.

- **Solução:** Conversão local para Parquet com `pyarrow` + `pandas` e carga programática direta via Job de API (`LoadJobConfig` com `WRITE_TRUNCATE`).

---

## 2. Configuração dos Campos Calculados no Looker Studio

Ao conectar a tabela no Looker Studio, clique em **+ Adicionar Campo** (*Add Field*) e configure os campos métricos calculados:

1. **Preço Médio Ponderado**
   - **Fórmula:** `SUM(preco_total) / SUM(qtd_itens_comprados)`
   - **Tipo de Dados:** Moeda > Real brasileiro (BRL)

2. **Total de Instituições Compradoras**
   - **Fórmula:** `COUNT_DISTINCT(cnpj_instituicao)`
   - **Tipo de Dados:** Numérico > Número

3. **Total de Fornecedores Distintos**
   - **Fórmula:** `COUNT_DISTINCT(cnpj_fornecedor)`
   - **Tipo de Dados:** Numérico > Número

4. **Ticket Médio por Transação**
   - **Fórmula:** `SUM(preco_total) / COUNT(compra)`
   - **Tipo de Dados:** Moeda > Real brasileiro (BRL)

---

## 3. Estrutura e Layout do Painel (Storytelling em Saúde Pública)

### A. Cabeçalho e Controles Globais (Filtros)

- **Título do Painel:** Panorama de Compras Públicas em Saúde — BPS (2020 a 2026)
- **Filtros Interativos:**
  - Lista suspensa: `ano_compra`
  - Lista suspensa: `uf`
  - Lista suspensa: `esfera` (Federal, Estadual, Municipal)
  - Controle de busca por texto: `descricao_catmat` (Item)

### B. Linha de Indicadores Centrais (Cartões de Visão Geral - KPIs)

1. **Total de Transações:** `COUNT(compra)` -> Referência: **342,7 mil**
2. **Gasto Total Homologado:** `SUM(preco_total)` -> Referência: **R$ 78,56 bi**
3. **Volume de Itens Adquiridos:** `SUM(qtd_itens_comprados)` -> Referência: **57,13 bi**
4. **Preço Médio Ponderado Geral:** `Preço Médio Ponderado` -> Referência: **R$ 1,38**
5. **Órgãos Compradores:** `COUNT_DISTINCT(cnpj_instituicao)` -> Referência: **831**
6. **Fornecedores Atendidos:** `COUNT_DISTINCT(cnpj_fornecedor)` -> Referência: **3,5 mil**

### C. Seção Visual e Análise das Perguntas de Negócio

1. **Evolução Temporal dos Gastos:** Gráfico de linhas combinadas com dimensão `ano_compra` e métricas `preco_total` e `qtd_itens_comprados`.
2. **Concentração Geográfica:** Gráfico de barras horizontais ou mapa coroplético por `uf` exibindo `preco_total`.
3. **Top 10 Fornecedores Homologados:** Gráfico de barras horizontais com dimensão `fornecedor` por `preco_total`.
4. **Distribuição por Modalidade de Compra:** Gráfico de rosca ou barras com dimensão `modalidade_compra` e contagem de registros.
5. **Tabela de Preços e Itens Críticos:** Tabela detalhada contendo `descricao_catmat`, `unidade_fornecimento`, `SUM(qtd_itens_comprados)`, `SUM(preco_total)` e `Preço Médio Ponderado`.
