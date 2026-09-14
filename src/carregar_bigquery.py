import pandas as pd
from google.cloud import bigquery

PROJECT_ID = "projeto-bps"
DATASET_ID = "dados_bps"
TABLE_ID = "bps_consolidado"
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

PARQUET_PATH = "data/processed/bps_consolidado.parquet"

print(f"Lendo base em Parquet: {PARQUET_PATH}...")
df = pd.read_parquet(PARQUET_PATH)
print(f"Total de registros na memória: {len(df):,}")

client = bigquery.Client(project=PROJECT_ID)

job_config = bigquery.LoadJobConfig(
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
)

print(f"Enviando dados para {FULL_TABLE_ID} no BigQuery...")
job = client.load_table_from_dataframe(df, FULL_TABLE_ID, job_config=job_config)
job.result()

table = client.get_table(FULL_TABLE_ID)
print(f"Sucesso! Tabela criada com {table.num_rows:,} linhas.")