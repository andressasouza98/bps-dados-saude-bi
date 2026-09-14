# Relatório de Inspeção Inicial e Mapeamento de Discrepâncias (2020 - 2026)

## 1. Diagnóstico Estrutural dos Arquivos
A inspeção automatizada realizada via script Python (`src/inspecionar_colunas.py`) nos 7 arquivos anuais do Banco de Preços em Saúde (BPS) resultou no seguinte mapeamento:

- **Período avaliado:** 2020, 2021, 2022, 2023, 2024, 2025 e 2026.
- **Encoding:** Padronizado em `utf-8` em todos os anos.
- **Separador:** Delimitador `;` (ponto e vírgula) em todas as bases.
- **Estrutura de Colunas:** 25 colunas idênticas em todos os períodos.
- **Identificador de Origem:** A coluna `ano_compra` já existe nativamente nas bases.

## 2. Relação de Colunas Mapeadas
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

## 3. Discrepâncias Internas e Plano de Tratamento
Embora a estrutura de cabeçalho seja idêntica, os dados brutos apresentam tratamentos necessários para o pipeline de dados da Sprint 2:
- **Campos Monetários (`preco_unitario`, `preco_total`):** Formato padrão brasileiro (`1.234,56`), exigindo limpeza de caracteres e substituição de vírgula por ponto para conversão em float.
- **Campos de Quantidade (`qtd_itens_comprados`):** Formato textual com possíveis pontos separadores de milhar, exigindo conversão numérica.
- **Datas (`compra`, `insercao`):** Padronização para formato ISO (`YYYY-MM-DD`).
- **Valores Ausentes:** Registros nulos em CNPJs ou fabricantes serão preservados como "Não informado" para não desconsiderar o valor monetário total.