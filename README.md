# 📊 BPS Analytics: Gestão e Monitoramento de Gastos em Saúde (2020-2026)

## Perguntas de Negócio

| Nº | Pergunta de Negócio | Campos Necessários | Visual Sugerido | KPI Associado |
|---|---|---|---|---|
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