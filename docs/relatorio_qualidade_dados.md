# Relatório de Qualidade de Dados e Consolidação - BPS (2020 - 2026)

## 1. Diagnóstico Estrutural dos Arquivos Brutos

A inspeção automatizada realizada via script Python (`src/inspecionar_colunas.py`) nos 7 arquivos anuais do Banco de Preços em Saúde (BPS) resultou no seguinte mapeamento:

- **Período avaliado:** 2020 a 2026 (7 arquivos anuais).
- **Encoding:** Padronizado em `utf-8` em todos os anos.
- **Separador:** Delimitador `;` (ponto e vírgula) em todas as bases.
- **Estrutura de Colunas:** 25 colunas idênticas em todos os períodos.
- **Identificador de Origem:** A coluna `ano_compra` já existe nativamente nas bases.

## 2. Relação de Colunas Mapeadas (25 Colunas)

1. `ano_compra`
2. `nome_instituicao`
3. `esfera`
4. `cnpj_instituicao`
5. `municipio_instituicao`
6. `uf`
7. `compra`
8. `insercao`
9. `codigo_br`
10. `descricao_catmat`
11. `unidade_fornecimento`
12. `generico`
13. `anvisa`
14. `modalidade_compra`
15. `tipo_compra`
16. `capacidade`
17. `unidade_medida`
18. `unidade_fornecimento_capacidade`
19. `cnpj_fornecedor`
20. `fornecedor`
21. `cnpj_fabricante`
22. `fabricante`
23. `qtd_itens_comprados`
24. `preco_unitario`
25. `preco_total`

## 3. Contagem de Linhas por Arquivo Bruto

| Ano do Arquivo | Linhas Carregadas |
| --- | --- |
| `bps_2020.csv` | 84.819 |
| `bps_2021.csv` | 83.622 |
| `bps_2022.csv` | 88.991 |
| `bps_2023.csv` | 31.992 |
| `bps_2024.csv` | 26.258 |
| `bps_2025.csv` | 26.215 |
| `bps_2026.csv` | 819 |
| **Total Bruto Acumulado** | **342.716** |

## 4. Tratamentos e Limpeza Aplicados

- **Padronização de Cabeçalhos:** Conversão para caixa baixa, remoção de acentuação e substituição de espaços por sublinhados (`_`).
- **Valores Monetários (`preco_total`, `preco_unitario`):** Limpeza do símbolo `R$`, remoção de pontos de milhar e substituição de vírgula decimal por ponto, convertendo os campos em `float`.
- **Quantidades (`qtd_itens_comprados`):** Remoção de separadores e conversão segura para formato numérico (`float`).
- **Datas (`compra`, `insercao`):** Conversão para formato ISO (`YYYY-MM-DD`).
- **Campos Categóricos com Nulos:** Preenchimento de ausências com `'Não Informado'` para não comprometer somatórios financeiros.
- **Deduplicação:** Remoção de duplicidades completas entre registros.

## 5. Balanço Final da Consolidação

- **Total de linhas brutas:** 342.716
- **Duplicidades eliminadas:** 19
- **Total de registros na base final:** 342.697
- **Total de colunas:** 25
- **Arquivo de saída gerado:** `data/processed/BPS_20_26_AndressaAlvesDeSouza.csv`

## 6. Gabarito de Indicadores Oficiais (2020 a 2026)

Consolidação realizada via script analítico (`src/calcular_kpis_eda.py`):

| Indicador | Métrica Aplicada | Valor Consolidado |
| --- | --- | --- |
| **Total de Registros de Compra** | Contagem total de linhas da base tratada | `342.697` |
| **Valor Total Registrado** | Soma do campo `preco_total` | `R$ 78.557.477.974,09` |
| **Quantidade Total de Itens** | Soma do campo `qtd_itens_comprados` | `57.127.143.721` unidades |
| **Instituições Compradoras Únicas** | Contagem distinta de `cnpj_instituicao` | `831` entidades |
| **Fornecedores Distintos** | Contagem distinta de `cnpj_fornecedor` | `3.502` fornecedores |
| **Preço Unitário Médio Ponderado** | `Soma(preco_total) / Soma(qtd_itens_comprados)` | `R$ 1,3751` |

## 7. Principais Insights da Análise Exploratória (EDA)

- **Pico Financeiro em 2025:** Apesar de contabilizar 26.214 registros (volume inferior aos anos de 2020 a 2022), o ano de 2025 concentrou R$ 34,93 bilhões (44,47% do total registrado em todo o período), apontando aquisições centralizadas de elevado valor agregado ou grandes contratos de fornecimento.
- **Concentração Geográfica Expressiva:**
  - **Paraná (PR):** Líder nacional com R$ 29,18 bilhões (37,14%).
  - **São Paulo (SP):** R$ 25,37 bilhões (32,30%).
  - **Ceará (CE):** R$ 5,40 bilhões (6,87%).
  - **Rio de Janeiro (RJ):** R$ 5,16 bilhões (6,57%).
  - **Santa Catarina (SC):** R$ 1,94 bilhões (2,47%).
  - *Os estados do Paraná e de São Paulo respondem juntos por aproximadamente 69,4% de todo o recurso movimentado no banco de preços.*
- **Evolução Temporal e Cobertura de 2026:** Os dados de 2026 contabilizam 817 registros e R$ 419,37 milhões, representando uma base parcial em consolidação referente ao exercício corrente.
