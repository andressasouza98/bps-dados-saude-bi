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
