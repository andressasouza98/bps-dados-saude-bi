import os
import pandas as pd

caminho_base = os.path.join("data", "processed", "BPS_20_26_AndressaAlvesDeSouza.csv")

print("=" * 80)
print("CARREGANDO BASE CONSOLIDADA PARA CÁLCULO DE KPIS E EDA")
print("=" * 80)

df = pd.read_csv(caminho_base, sep=';', encoding='utf-8', low_memory=False)

# 1. Total de Registros de Compra
total_registros = len(df)

# 2. Valor Total Registrado (R$)
valor_total = df['preco_total'].sum()

# 3. Quantidade Total de Itens Comprados
qtd_total_itens = df['qtd_itens_comprados'].sum()

# 4. Total de Instituições Compradoras Distintas
total_instituicoes = df['cnpj_instituicao'].nunique()

# 5. Total de Fornecedores Distintos
total_fornecedores = df['cnpj_fornecedor'].nunique()

# 6. Preço Unitário Médio Ponderado Geral
preco_medio_ponderado = valor_total / qtd_total_itens if qtd_total_itens > 0 else 0

print("\n>>> GABARITO OFICIAL DOS 6 KPIS PRINCIPAIS (2020 - 2026):")
print(f"  1. Total de Registros de Compra:       {total_registros:,}")
print(f"  2. Valor Total Registrado:            R$ {valor_total:,.2f}")
print(f"  3. Quantidade Total de Itens:         {qtd_total_itens:,.0f}")
print(f"  4. Instituições Compradoras Únicas:   {total_instituicoes:,}")
print(f"  5. Fornecedores Distintos:            {total_fornecedores:,}")
print(f"  6. Preço Unitário Médio Ponderado:    R$ {preco_medio_ponderado:.4f}")

print("\n" + "=" * 80)
print("EVOLUÇÃO ANUAL (VALOR TOTAL E REGISTROS):")
print("=" * 80)
evolucao_anual = df.groupby('ano_compra').agg(
    total_registros=('compra', 'count'),
    valor_total=('preco_total', 'sum'),
    qtd_itens=('qtd_itens_comprados', 'sum')
).reset_index()
print(evolucao_anual.to_string(index=False))

print("\n" + "=" * 80)
print("TOP 5 UFs POR VALOR TOTAL (R$):")
print("=" * 80)
top_uf = df.groupby('uf')['preco_total'].sum().sort_values(ascending=False).head(5).reset_index()
print(top_uf.to_string(index=False))