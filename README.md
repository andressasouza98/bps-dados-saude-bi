# 📊 BPS Analytics: Gestão e Monitoramento de Gastos em Saúde (2020-2026)

## Perguntas de Negócio

| Nº | Pergunta de Negócio | Campos Necessários | Visual Sugerido | KPI Associado |
| --- | --- | --- | --- | --- |
| 1 | Qual foi a evolução anual do valor total registrado nas compras em saúde? | `ano_compra`, `preco_total` | Gráfico de Linhas | Valor total registrado |
| 2 | Quais Unidades Federativas (UF) concentram o maior montante financeiro? | `uf`, `preco_total` | Gráfico de Barras / Mapa | Valor total registrado |
| 3 | Quais instituições compradoras realizaram os maiores volumes de aquisição? | `nome_instituicao`, `preco_total` | Gráfico de Barras Horizontais | Valor total registrado |
| 4 | Quais itens (`descricao_catmat`) representam o maior custo acumulado? | `descricao_catmat`, `preco_total` | Tabela / Barras | Valor total registrado |
| 5 | Qual o preço unitário médio ponderado de itens críticos ao longo dos anos? | `descricao_catmat`, `unidade_fornecimento`, `preco_total`, `qtd_itens_comprados` | Gráfico de Linhas | Preço unitário médio ponderado |
| 6 | Qual é a distribuição das modalidades de compra empregadas pelos órgãos? | `modalidade_compra`, `ano_compra` | Gráfico de Rosca | Número de registros |
| 7 | Quais são os principais fornecedores por volume financeiro homologado? | `fornecedor`, `cnpj_fornecedor`, `preco_total` | Gráfico de Barras | Fornecedores distintos |
| 8 | Como se dividem as compras entre as diferentes esferas governamentais? | `esfera`, `preco_total` | Gráfico de Colunas / Rosca | Valor total registrado |
| 9 | Há variação expressiva de preços entre diferentes fabricantes para o mesmo produto e unidade? | `descricao_catmat`, `fabricante`, `unidade_fornecimento`, `preco_unitario` | Gráfico de Dispersão / Tabela | Preço unitário médio ponderado |
| 10 | Qual o volume total de itens hospitalares e medicamentos adquiridos por ano? | `ano_compra`, `qtd_itens_comprados` | Gráfico de Colunas | Quantidade total de itens comprados |

## 🛠️ Pipeline de ETL e Tratamento de Dados (Sprint 2)

O pipeline de extração, transformação e carga foi implementado em Python (`src/preparar_bps.py`) para unificar e sanear as bases de 2020 a 2026:

1. **Importação e Codificação:** Leitura das 7 bases anuais sob codificação `utf-8` e separador `;`, somando 342.716 registros brutos.
2. **Padronização de Esquema:** Normalização de cabeçalhos (caixa baixa, remoção de caracteres especiais e acentos).
3. **Conversão de Tipos e Formatações:**
   - **Monetários (`preco_total`, `preco_unitario`):** Remoção de prefixos (`R$`) e pontos de milhar, substituição de vírgula decimal por ponto e conversão para `float`.
   - **Quantidades (`qtd_itens_comprados`):** Limpeza e conversão para formato numérico (`float`).
   - **Datas (`compra`, `insercao`):** Padronização para formato ISO internacional (`YYYY-MM-DD`).
4. **Tratamento de Nulos e Inconsistências:** Imputação do rótulo `'Não Informado'` em atributos categóricos com valores ausentes.
5. **Deduplicação:** Remoção de 19 registros duplicados na integridade da linha.
6. **Consolidação Final:** Preservação da rastreabilidade temporal (`ano_compra`) e exportação da base unificada `BPS_20_26_AndressaAlvesDeSouza.csv` contendo 342.697 linhas e 25 colunas.

## 📈 Métricas de Negócio e Gabarito Oficial de KPIs (Sprint 3)

Os cálculos foram consolidados via Python (`src/calcular_kpis_eda.py`) sobre os 342.697 registros unificados:

| Indicador (KPI) | Fórmula / Critério | Valor Consolidado |
| --- | --- | --- |
| **Total de Registros de Compra** | Contagem total de linhas da base tratada | `342.697` |
| **Valor Total Registrado** | Soma do campo `preco_total` | `R$ 78.557.477.974,09` |
| **Quantidade Total de Itens** | Soma do campo `qtd_itens_comprados` | `57.127.143.721` unidades |
| **Instituições Compradoras Únicas** | Contagem distinta de `cnpj_instituicao` | `831` entidades |
| **Fornecedores Distintos** | Contagem distinta de `cnpj_fornecedor` | `3.502` fornecedores |
| **Preço Unitário Médio Ponderado** | `Soma(preco_total) / Soma(qtd_itens_comprados)` | `R$ 1,3751` |

### Destaques Regionais (Top 5 UFs)

- **PR:** R$ 29,18 bi (37,14%)
- **SP:** R$ 25,37 bi (32,30%)
- **CE:** R$ 5,40 bi (6,87%)
- **RJ:** R$ 5,16 bi (6,57%)
- **SC:** R$ 1,94 bi (2,47%)

### 💡 Principais Insights da Análise Exploratória (EDA)

- **Pico Financeiro em 2025:** Apesar de contabilizar 26.214 registros (volume inferior aos anos de 2020 a 2022), o ano de 2025 concentrou R$ 34,93 bilhões (44,5% do total registrado no período), indicando contratações públicas de grande vulto ou itens de elevado valor agregado.
- **Concentração Geográfica Expressiva:** As regiões Sul e Sudeste lideram os montantes acumulados:
  - **Paraná (PR):** Líder nacional com R$ 29,18 bilhões (37,14%).
  - **São Paulo (SP):** R$ 25,37 bilhões (32,30%).
  - **Ceará (CE):** R$ 5,40 bilhões (6,87%).
  - **Rio de Janeiro (RJ):** R$ 5,16 bilhões (6,57%).
  - **Santa Catarina (SC):** R$ 1,94 bilhões (2,47%).
  - *PR e SP somam, juntos, quase 70% de todo o recurso movimentado no período avaliado.*
- **Período Parcial de 2026:** Apresenta 817 registros e R$ 419,37 milhões, refletindo a extração parcial do ano corrente.
