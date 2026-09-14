import os
import glob
import pandas as pd

caminho = os.path.join("data", "raw", "*.csv")
arquivos = sorted(glob.glob(caminho))

print("=" * 80)
print("INSPEÇÃO DAS BASES BPS (2020 A 2026)")
print("=" * 80)

encodings_para_testar = ['utf-8', 'iso-8859-1', 'latin1', 'cp1252']

for arq in arquivos:
    nome = os.path.basename(arq)
    print(f"\n>>> Arquivo: {nome}")
    
    sucesso = False
    for enc in encodings_para_testar:
        for sep in [';', ',']:
            try:
                # Lê apenas as 3 primeiras linhas para não sobrecarregar a memória
                df_amostra = pd.read_csv(arq, encoding=enc, sep=sep, nrows=3)
                if len(df_amostra.columns) > 1:
                    print(f"  Encoding: {enc} | Separador: '{sep}'")
                    print(f"  Total de colunas: {len(df_amostra.columns)}")
                    print(f"  Colunas encontradas:\n  {list(df_amostra.columns)}")
                    sucesso = True
                    break
            except Exception:
                continue
        if sucesso:
            break
            
    if not sucesso:
        print("  [ERRO] Não foi possível ler o arquivo com as configurações testadas.")

print("\n" + "=" * 80)