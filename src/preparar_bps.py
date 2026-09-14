import os
import glob
import pandas as pd
import numpy as np

print("=" * 80)
print("INICIANDO PIPELINE DE TRATAMENTO E CONSOLIDAÇÃO - BPS (2020-2026)")
print("=" * 80)

# 1. Definição de diretórios e arquivos
raw_path = os.path.join("data", "raw", "*.csv")
processed_dir = os.path.join("data", "processed")
output_file = os.path.join(processed_dir, "BPS_20_26_AndressaAlvesDeSouza.csv")

os.makedirs(processed_dir, exist_ok=True)
arquivos = sorted(glob.glob(raw_path))

if not arquivos:
    raise FileNotFoundError("Nenhum arquivo CSV encontrado em data/raw/.")

dfs = []
total_linhas_brutas = 0

# 2. Leitura e carregamento dos arquivos anuais
for arq in arquivos:
    nome = os.path.basename(arq)
    print(f"\n[+] Lendo: {nome}")
    
    df_temp = pd.read_csv(arq, sep=';', encoding='utf-8', low_memory=False)
    linhas_orig = len(df_temp)
    total_linhas_brutas += linhas_orig
    print(f"    Linhas carregadas: {linhas_orig:,}")
    
    dfs.append(df_temp)

# 3. Concatenação unificada de 2020 a 2026
print("\n[+] Consolidando bases anuais...")
df = pd.concat(dfs, ignore_index=True)
print(f"    Total de linhas acumuladas brutas: {len(df):,}")

# 4. Padronização dos nomes de colunas
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(' ', '_')
    .str.normalize('NFKD')
    .str.encode('ascii', errors='ignore')
    .str.decode('utf-8')
)

# 5. Função para conversão de valores monetários
def tratar_moeda(coluna):
    if coluna.dtype == object:
        return (
            coluna.astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace(' ', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .replace(['nan', 'None', ''], np.nan)
            .astype(float)
        )
    return coluna.astype(float)

print("\n[+] Convertendo campos de preço...")
if 'preco_total' in df.columns:
    df['preco_total'] = tratar_moeda(df['preco_total'])
if 'preco_unitario' in df.columns:
    df['preco_unitario'] = tratar_moeda(df['preco_unitario'])

# 6. Conversão de quantidades
print("[+] Convertendo quantidades...")
if 'qtd_itens_comprados' in df.columns:
    if df['qtd_itens_comprados'].dtype == object:
        df['qtd_itens_comprados'] = (
            df['qtd_itens_comprados'].astype(str)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .replace(['nan', 'None', ''], np.nan)
            .astype(float)
        )
    else:
        df['qtd_itens_comprados'] = df['qtd_itens_comprados'].astype(float)

# 7. Padronização de datas para ISO (YYYY-MM-DD)
print("[+] Padronizando colunas de data...")
for col_data in ['compra', 'insercao']:
    if col_data in df.columns:
        df[col_data] = pd.to_datetime(df[col_data], errors='coerce', dayfirst=True).dt.strftime('%Y-%m-%d')

# 8. Tratamento de nulos em campos de texto
print("[+] Tratando valores nulos textuais...")
cols_texto = df.select_dtypes(include=['object']).columns
df[cols_texto] = df[cols_texto].fillna('Não Informado')

# 9. Identificação e remoção de duplicidades exatas
linhas_antes_dup = len(df)
df.drop_duplicates(inplace=True)
duplicatas_removidas = linhas_antes_dup - len(df)
print(f"[+] Registros duplicados removidos: {duplicatas_removidas:,}")

# 10. Exportação da base final consolidada
print(f"\n[+] Gravando arquivo consolidado em: {output_file}")
df.to_csv(output_file, index=False, sep=';', encoding='utf-8')

print("\n" + "=" * 80)
print("RELATÓRIO RESUMIDO DE PROCESSAMENTO:")
print(f"  Linhas brutas somadas: {total_linhas_brutas:,}")
print(f"  Duplicidades eliminadas: {duplicatas_removidas:,}")
print(f"  Total de linhas na base final: {len(df):,}")
print(f"  Total de colunas: {len(df.columns)}")
print("=" * 80)