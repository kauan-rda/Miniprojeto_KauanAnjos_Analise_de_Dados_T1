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
linhas_antes = df.shape[0]

# O criador da base notou que há textos "#N/D" no lugar de vazios. Vamos converter para nulo real (NaN)
df[['PR_CAT', 'PR_NOME']] = df[['PR_CAT', 'PR_NOME']].replace("#N/D", np.nan)

# Removendo as linhas onde a categoria ou nome do produto estão nulos
df = df.dropna(subset=['PR_CAT', 'PR_NOME'])

# Removendo duplicatas exatas
df = df.drop_duplicates()

linhas_depois = df.shape[0]
print(f"Limpeza concluída. Linhas removidas (nulos e duplicatas): {linhas_antes - linhas_depois}")

# ==========================================

print("\n--- SPRINT 4: Estatísticas da coluna CL_FHL (Número de Filhos) ---")

# O describe() já traz quase tudo
estatisticas = df['CL_FHL'].describe()
moda = df['CL_FHL'].mode()[0]

print(f"Total de registros válidos: {estatisticas['count']}")
print(f"Média de filhos: {estatisticas['mean']:.2f}")
print(f"Mediana: {estatisticas['50%']}")
print(f"Desvio Padrão: {estatisticas['std']:.2f}")
print(f"Moda (Mais comum): {moda}")
print(f"Mínimo de filhos: {estatisticas['min']}")
print(f"Máximo de filhos: {estatisticas['max']}")
    print(f"1º Quartil (25%): {estatisticas['25%']}")
    print(f"3º Quartil (75%): {estatisticas['75%']}")