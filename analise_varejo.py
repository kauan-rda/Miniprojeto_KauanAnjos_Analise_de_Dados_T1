import pandas as pd

print("--- SPRINT 1: Carregamento ---")
# Carregando a base de dados
df = pd.read_csv('varejo.csv', encoding='utf-8')

# Mostrando numero de registros e colunas
print(f"Número de registros (linhas): {df.shape[0]}")
print(f"Número de atributos (colunas): {df.shape[1]}")

# Mostrando os tipos de dados
print("\nTipos de dados:")
print(df.dtypes)