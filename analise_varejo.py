import pandas as pd
import numpy as np

print("=" * 55)
print("  SPRINT 1: Carregamento e Diagnóstico Inicial")
print("=" * 55)

# Carrego a base e exibo as dimensões e os tipos de cada coluna
# para ter uma visão geral antes de qualquer modificação.
df = pd.read_csv('varejo.csv', encoding='utf-8')

print(f"Registros (linhas) : {df.shape[0]}")
print(f"Atributos (colunas): {df.shape[1]}")

print("\nTipos de dados:")
print(df.dtypes)

# Verifico nulos por coluna para mapear onde estão os problemas.
print("\nValores nulos por coluna (antes da limpeza):")
print(df.isnull().sum().to_string())

# Verifico duplicatas exatas para saber o volume de ruído na base.
print(f"\nLinhas duplicadas encontradas: {df.duplicated().sum()}")

# Verifico a presença do resíduo textual '#N/D' nas colunas de produto,
# pois esse valor mascarado como texto não é detectado pelo isnull().
print(f"\nRegistros com '#N/D' em PR_CAT : {(df['PR_CAT']  == '#N/D').sum()}")
print(f"Registros com '#N/D' em PR_NOME: {(df['PR_NOME'] == '#N/D').sum()}")


print("\n" + "=" * 55)
print("  SPRINT 2: Tratamento de Tipos")
print("=" * 55)

# Converto DATA para datetime para permitir analises temporais.
# Uso errors='coerce' para que datas mal formatadas virem NaT
# em vez de travar a execução.
df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
datas_invalidas = df['DATA'].isnull().sum()
print("Coluna 'DATA' convertida para datetime.")
if datas_invalidas > 0:
    print(f"  Datas inválidas convertidas para NaT: {datas_invalidas}")
else:
    print("  Nenhuma data inválida encontrada.")

# Garanto que CL_FHL seja numerico, pois é a coluna central
# das estatisticas descritivas da Sprint 4.
df['CL_FHL'] = pd.to_numeric(df['CL_FHL'], errors='coerce')
print("Coluna 'CL_FHL' garantida como numérica.")


print("\n" + "=" * 55)
print("  SPRINT 3: Limpeza de Dados")
print("=" * 55)

linhas_antes = df.shape[0]

# Converto '#N/D' para NaN real nas colunas de produto.
# Esse residuo vem de exportações do Excel e precisa ser
# tratado antes das etapas de imputação e remoção.
df[['PR_CAT', 'PR_NOME']] = df[['PR_CAT', 'PR_NOME']].replace('#N/D', np.nan)
print("Resíduos '#N/D' convertidos para NaN em PR_CAT e PR_NOME.")

# PR_CAT: preencho com 'Sem Categoria' para preservar o registro de venda.
# Justificativa: a transação continua valida mesmo sem categoria classificada;
# descartar causaria perda desnecessaria de dados de vendas.
df['PR_CAT'] = df['PR_CAT'].fillna('Sem Categoria')
print("Nulos em PR_CAT preenchidos com 'Sem Categoria'.")

# PR_NOME: removo as linhas onde o nome do produto é nulo.
# Justificativa: um produto sem nome não é identificavel para agrupamentos
# e analises de categoria, tornando o registro inutil para a analise.
linhas_pre_nome = df.shape[0]
df = df.dropna(subset=['PR_NOME'])
removidos_nome = linhas_pre_nome - df.shape[0]
print(f"Nulos em PR_NOME: {removidos_nome} linha(s) removida(s).")

# Valido o CO_ID (identificador de compra).
# Em bases de supermercado, um mesmo CO_ID pode aparecer em varias linhas
# (uma por produto do carrinho) — isso é comportamento esperado, não duplicata.
print(f"\nCO_IDs distintos (pedidos únicos): {df['CO_ID'].nunique()}")
print(f"Média de itens por pedido        : {df.shape[0] / df['CO_ID'].nunique():.1f}")
nulos_coid = df['CO_ID'].isnull().sum()
if nulos_coid > 0:
    print(f"  CO_ID nulos encontrados: {nulos_coid} — registros removidos.")
    df = df.dropna(subset=['CO_ID'])
else:
    print("  Nenhum CO_ID nulo encontrado.")

# Removo duplicatas exatas — linhas 100% identicas em todas as colunas.
linhas_pre_dup = df.shape[0]
df = df.drop_duplicates()
print(f"\nDuplicatas exatas removidas: {linhas_pre_dup - df.shape[0]}")

print(f"\nLimpeza concluída.")
print(f"  Linhas antes : {linhas_antes}")
print(f"  Linhas depois: {df.shape[0]}")
print(f"  Total removido: {linhas_antes - df.shape[0]}")


print("\n" + "=" * 55)
print("  SPRINT 4: Estatísticas Descritivas — CL_FHL (Filhos)")
print("=" * 55)

# Uso o describe() como base e calculo a moda separadamente,
# pois ela não esta incluida no retorno padrão do metodo.
stats = df['CL_FHL'].describe()
moda  = df['CL_FHL'].mode()[0]

print(f"  Registros válidos  : {int(stats['count'])}")
print(f"  Média              : {stats['mean']:.2f}")
print(f"  Mediana            : {stats['50%']:.1f}")
print(f"  Desvio Padrão      : {stats['std']:.2f}")
print(f"  Moda               : {moda:.0f}")
print(f"  Mínimo             : {stats['min']:.0f}")
print(f"  Máximo             : {stats['max']:.0f}")
print(f"  1º Quartil (25%)   : {stats['25%']:.1f}")
print(f"  3º Quartil (75%)   : {stats['75%']:.1f}")


print("\n" + "=" * 55)
print("  SPRINT 5: Agrupamentos e Insights")
print("=" * 55)

# Agrupamento 1: identifico as categorias com maior volume de itens
# vendidos para entender o giro de produtos no varejo.
print("\n[1] Top 5 Categorias com mais itens vendidos:")
print(df['PR_CAT'].value_counts().head(5).to_string())

# Agrupamento 2: comparo o total de compras por genero do cliente
# para identificar o perfil predominante de consumo.
print("\n[2] Total de Compras por Gênero (CL_GENERO):")
vendas_genero = (
    df.groupby('CL_GENERO')['CO_ID']
    .count()
    .reset_index()
    .rename(columns={'CO_ID': 'Total de Compras'})
    .sort_values('Total de Compras', ascending=False)
)
print(vendas_genero.to_string(index=False))

# Agrupamento 3: uso pivot_table para revelar o perfil familiar
# medio de cada segmento de cliente (CL_SEG).
print("\n[3] Média de Filhos por Segmento de Cliente (CL_SEG):")
media_filhos = df.pivot_table(
    index='CL_SEG',
    values='CL_FHL',
    aggfunc='mean'
).rename(columns={'CL_FHL': 'Média de Filhos'})
print(media_filhos.round(2).to_string())


print("\n" + "=" * 55)
print("  CONCLUSÕES GERAIS")
print("=" * 55)
print("1. A base apresentou resíduos '#N/D' nas colunas de produto,")
print("   exigindo conversão para NaN antes de qualquer limpeza.")
print("2. Optei por preservar registros com PR_CAT nula imputando")
print("   'Sem Categoria', evitando perda desnecessária de vendas.")
print("3. Registros com PR_NOME nula foram removidos por não permitirem")
print("   identificação do produto nas análises de agrupamento.")
print("4. As estatísticas de CL_FHL revelam o perfil familiar médio")
print("   dos clientes, dado útil para campanhas segmentadas.")
print("5. As top 5 categorias concentram o maior giro de produtos,")
print("   orientando decisões de reposição de estoque.")
print("6. A variação da média de filhos entre segmentos indica perfis")
print("   de consumo distintos a serem explorados em análises futuras.")
