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
|---|---|
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