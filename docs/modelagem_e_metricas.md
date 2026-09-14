# 📐 Regras de Modelagem de Dados, Agregações e Métricas - BPS

Este documento estabelece as diretrizes de governança de dados, tipagem, fórmulas calculadas e critérios metodológicos para visualização no Looker Studio.

---

## 1. Matriz de Agregações: Quando utilizar cada operação

| Campo da Base | Tipo de Dado | Agregação Padrão | Operações Permitidas | Operações Proibidas / Não Recomendadas | Justificativa de Negócio |
| --- | --- | --- | --- | --- | --- |
| `preco_total` | Moeda (Numérico) | **SOMA (SUM)** | Soma, Média, Mediana | Contagem como métrica financeira | Representa o gasto monetário total da transação. |
| `qtd_itens_comprados` | Numérico | **SOMA (SUM)** | Soma, Média, Máximo, Mínimo | Contagem simples | Representa o volume físico total de unidades adquiridas. |
| `preco_unitario` | Moeda (Numérico) | **NENHUMA (None)** | Mediana pontual, Média ponderada | **SOMA (SUM)** *(Totalmente Proibida)* | Somar preços unitários de itens heterogêneos produz um valor sem significado econômico real. |
| `cnpj_instituicao` | Texto | **CONTAGEM DISTINTA (COUNT_DISTINCT)** | Contagem distinta | Soma, Média | Avalia o alcance institucional (quantos órgãos distintos compraram). |
| `cnpj_fornecedor` | Texto | **CONTAGEM DISTINTA (COUNT_DISTINCT)** | Contagem distinta | Soma, Média | Avalia a diversidade e concentração do mercado fornecedor. |
| `compra` / `ano_compra` | Data / Numérico | **CONTAGEM (COUNT)** | Contagem simples de transações | Soma de ano | Mede o número de registros (volume operacional de licitações/compras). |

---

## 2. Regra de Ouro: Proibição da Soma de Preços Unitários e Uso da Média Ponderada

### ❌ Por que NUNCA somar `preco_unitario`?

Se uma instituição compra 1.000.000 de comprimidos de paracetamol a R$ 0,10 e 2 tomógrafos a R$ 500.000,00, a soma simples dos preços unitários resultaria em R$ 500.000,10. Esse número não expressa o gasto total real (que foi de R$ 1.100.000,00) nem o preço médio das unidades.

### Fórmula Correta: Preço Unitário Médio Ponderado

Em qualquer nível de agrupamento (seja por produto, por ano, por UF ou geral), o preço unitário deve ser calculado ponderando o valor pelo volume físico real:

$$\text{Preço Médio Ponderado} = \frac{\sum \text{preco\_total}}{\sum \text{qtd\_itens\_comprados}}$$

---

## 3. Critérios Obrigatórios para Comparação de Preços entre Produtos

Para comparar preços de itens entre anos, estados ou fornecedores de forma justa e sem viés estatístico:

1. **Chave de Produto (`descricao_catmat` ou `codigo_br`):** Nunca comparar itens de descrições genéricas diferentes.
2. **Homogeneidade da Unidade de Fornecimento (`unidade_fornecimento` / `unidade_medida`):**
   - É mandatório filtrar ou segmentar por unidade idêntica (ex.: comparar *Comprimido* apenas com *Comprimido*, e não com *Caixa c/ 100 comprimidos* ou *Frasco c/ 500 ml*).
3. **Avaliação por Mediana vs. Média:**
   - Em compras públicas hospitalares, valores atípicos (outliers) decorrentes de pequenas compras de emergência podem inflacionar a média aritmética. Em análises de detalhe por item, utiliza-se a **Mediana** ou a **Média Ponderada**.

---

## 4. Dicionário de Campos Calculados para o Looker Studio

| Nome da Métrica no Looker Studio | Tipo | Fórmula no Looker Studio | Finalidade no Dashboard |
| --- | --- | --- | --- |
| **Valor Total Homologado** | Moeda (BRL) | `SUM(preco_total)` | KPI Geral e Gráficos de Valor |
| **Total de Itens Adquiridos** | Numérico | `SUM(qtd_itens_comprados)` | KPI de Volume Físico |
| **Total de Transações** | Numérico | `COUNT(compra)` | KPI de Frequência de Compras |
| **Instituições Únicas** | Numérico | `COUNT_DISTINCT(cnpj_instituicao)` | KPI de Órgãos Compradores |
| **Fornecedores Únicos** | Numérico | `COUNT_DISTINCT(cnpj_fornecedor)` | KPI de Competitividade |
| **Preço Médio Ponderado** | Moeda (BRL) | `SUM(preco_total) / SUM(qtd_itens_comprados)` | Monitoramento de Variação de Preço |
| **Ticket Médio por Transação** | Moeda (BRL) | `SUM(preco_total) / COUNT(compra)` | Análise de Vulto das Compras |
