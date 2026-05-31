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

# ==========================================

print("\n--- SPRINT 2: Tratamento de Tipos ---")
# Convertendo a coluna de Data para datetime
if 'Data' in df.columns:
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    print("Coluna 'Data' convertida para datetime com sucesso.")

# ==========================================

print("\n--- SPRINT 3: Limpeza de Dados ---")
# 1. Identificar problemas
print("Valores nulos por coluna (Antes):")
print(df.isnull().sum())
print(f"Duplicatas encontradas: {df.duplicated().sum()}")

# 2. Tratamento de Nulos
# Preenchendo categorias vazias com 'Sem Categoria' (Critério de Avaliação 4)
if 'Categoria' in df.columns:
    df['Categoria'] = df['Categoria'].fillna('Sem Categoria')

# Tratando outras colunas numéricas (exemplo: dimensões/valores) preenchendo com 0 ou mediana
# Justificativa: Preservar as linhas para não perder dados de clientes/datas válidas.
if 'Valor' in df.columns:
    df['Valor'] = df['Valor'].fillna(df['Valor'].median())

# 3. Tratamento de Duplicatas
df = df.drop_duplicates()
print("\nDuplicatas removidas e valores nulos tratados.")