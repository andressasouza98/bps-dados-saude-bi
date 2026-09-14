# 📖 Dicionário de Dados — Banco de Preços em Saúde (BPS 2020–2026)

**Projeto:** BPS Analytics — Gestão e Monitoramento de Gastos em Saúde  
**Estudante:** Andressa Alves de Souza  
**Arquivo Consolidado:** `data/processed/BPS_20_26_AndressaAlvesDeSouza.csv`  
**Fonte Primária:** Ministério da Saúde / Banco de Preços em Saúde (BPS)  

---

## 1. Visão Geral da Base Consolidada

A base oficial consolidada reúne as transações de compras públicas de medicamentos e insumos médico-hospitalares homologadas entre os exercícios de 2020 e 2026. A estrutura foi padronizada em formato tabular, com delimitador ponto e vírgula (`;`) e codificação UTF-8.

---

## 2. Metadados e Definição das Variáveis

| Variável Padronizada | Tipo de Dado | Obrigatório | Descrição Técnica e Aplicação no Negócio |
| :--- | :--- | :---: | :--- |
| `ano_compra` | Inteiro | Sim | Ano de homologação do certame ou empenho da compra pública (2020 a 2026). Utilizado para cortes temporais e análise de evolução orçamentária. |
| `compra` | Data (ISO 8601) | Sim | Data formal da transação da compra pública (`YYYY-MM-DD`). |
| `insercao` | Data (ISO 8601) | Não | Data em que o registro foi incluído no sistema informatizado do BPS (`YYYY-MM-DD`). |
| `uf` | Texto | Sim | Sigla da Unidade Federativa da instituição pública compradora (27 estados/DF). Utilizada para mensuração de concentração regional. |
| `esfera` | Texto | Sim | Esfera administrativa governamental do órgão adquirente (`ESTADUAL`, `MUNICIPAL`, `FEDERAL`). Registros com valor '0' foram expurgados na higienização. |
| `cnpj_instituicao` | Texto (14 dígitos) | Sim | Cadastro Nacional da Pessoa Jurídica do órgão/instituição compradora pública, tratado com preenchimento de zeros à esquerda. |
| `nome_instituicao` | Texto | Não | Denominação formal da entidade pública compradora. Quando ausente na base bruta, imputado como `'Não Informado'`. |
| `modalidade_compra` | Texto | Sim | Procedimento licitatório adotado para a contratação pública (ex.: Pregão Eletrônico, Dispensa de Licitação, Inexigibilidade). |
| `cnpj_fornecedor` | Texto (14 dígitos) | Sim | CNPJ da empresa distribuidora ou prestadora contratada para o fornecimento do insumo. |
| `cnpj_fabricante` | Texto (14 dígitos) | Não | CNPJ do laboratório ou fabricante responsável pelo registro primário do produto perante a autoridade sanitária. |
| `codigo_br` | Texto | Não | Código de catalogação no catálogo unificado de materiais (CATMAT/Siasg). |
| `descricao_catmat` | Texto | Sim | Descrição padronizada da especificação técnica, princípio ativo, forma farmacêutica e concentração do item farmacêutico/hospitalar. |
| `unidade_fornecimento` | Texto | Não | Unidade física e embalagem de faturamento da aquisição (ex.: caixa, frasco, ampola, comprimido). |
| `qtd_itens_comprados` | Numérico (Float) | Sim | Quantidade física de unidades adquiridas no item da compra. |
| `preco_unitario` | Numérico (Float) | Sim | Valor pago por unidade do insumo adquirido (R$), padronizado sem separador de milhar e com ponto decimal. |
| `preco_total` | Numérico (Float) | Sim | Valor contábil homologado total da linha de contratação pública, apurado pela equação: `qtd_itens_comprados * preco_unitario`. |

---

## 3. Regras de Negócio e Validações Metodológicas

- **Tratamento de Strings Ausentes:** Valores nulos em colunas descritivas foram preenchidos de forma controlada com a cadeia `'Não Informado'`.
- **Integridade dos Identificadores:** Todos os CNPJs foram higienizados para conter exatamente 14 dígitos numéricos, preservando os zeros à esquerda (`zfill(14)`).
- **Tratamento da Métrica Preço Médio:** O preço unitário médio não deve ser apurado por média aritmética simples entre produtos distintos. A fórmula metodológica obrigatória é a média ponderada por volume:
  $$\text{Preço Médio Ponderado} = \frac{\sum \text{preco\_total}}{\sum \text{qtd\_itens\_comprados}}$$
