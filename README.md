Mini-Projeto: Análise Exploratória de Varejo

Sobre o Projeto

Realizei uma Análise Exploratória de Dados (AED) sobre a base varejo.csv, que contém registros de 50.000 compras de 1.000 clientes em uma rede de supermercados entre 2010 e 2022.

O objetivo foi identificar inconsistências, limpar a base e gerar estatísticas e insights sobre o comportamento dos clientes.

Conceito-Chave: Estrutura Item-por-Item

Cada linha do CSV representa UM ITEM de uma compra — não uma compra completa.

Exemplos:
- Se um cliente compra 3 unidades de refrigerante na mesma compra → 3 linhas idênticas (mesma DATA, CO_ID, CL_ID, PR_ID, PR_CAT, PR_NOME)
- Se um cliente compra 1 refrigerante e 1 leite na mesma nota fiscal → 2 linhas (mesma DATA, CO_ID, CL_ID, mas PR_ID, PR_CAT, PR_NOME diferentes)

Essa estrutura é típica de bases de varejo e é importante entender para não remover dados válidos por engano.

Colunas da Base

DATA: Data da compra
CO_ID: Número da nota fiscal (ID da compra)
CL_ID: Número do cliente
CL_GENERO: Sexo: M ou F
CL_EC: Estado civil: 1=Casado, 2=Divorciado, 3=Separado, 4=Solteiro, 5=Viúvo
CL_FHL: Número de filhos do cliente
CL_SEG: Segmento econômico: A, B ou C
PR_ID: Código do produto (SKU)
PR_CAT: Categoria do produto
PR_NOME: Nome do produto

Como Executar

1. Instale as dependências:
pip install pandas numpy

2. Coloque varejo.csv na mesma pasta do script.

3. Execute:
python analise_varejo.py

Etapas da Análise (Sprints)

Sprint 1 — Diagnóstico Inicial
Carrego a base e examino:
- Dimensões (linhas × colunas)
- Tipos de dados de cada coluna
- Nulos por coluna
- Resíduos textuais (#N/D)
- Duplicatas exatas

Sprint 2 — Tratamento de Tipos
Converto as colunas para tipos apropriados:
- DATA → datetime
- CL_FHL → numérica
- CL_EC → mantém como códigos (1-5)

Sprint 3 — Limpeza de Dados
Aplico decisões documentadas:

1. Resíduos #N/D → Converto para NaN real
2. PR_CAT nula → Preencho com "Sem Categoria"
3. PR_NOME nula → Removo a linha
4. CO_ID nula → Removo a linha
5. Duplicatas exatas → Removo com cuidado

Sprint 4 — Estatísticas Descritivas
Calculo para a coluna CL_FHL:
- Contagem, média, mediana, desvio padrão
- Moda, mínimo, máximo
- 1º e 3º quartis

Sprint 5 — Agrupamentos

1. Top 5 Categorias
2. Volume de itens por Gênero
3. Média de filhos por Segmento Econômico

Lógica ETL (Extract, Transform, Load)

A limpeza segue um princípio fundamental: preservar dados válidos, remover apenas ruído.

Decisões Críticas

PR_CAT | Nulo | Preencher com "Sem Categoria" | Venda é real; categoria é metadado
PR_NOME | Nulo | Remover linha | Produto sem nome é inidentificável
CO_ID | Nulo | Remover linha | Sem nº da nota fiscal, perdi rastreamento
Todas | #N/D | Converter para NaN | Artefato de exportação do Excel
Todas | 100% iguais | Remover | Erro de importação, não dado real

*O critério de tratamento de nulos e condicionais fala sobre uso de if/else, então equivalente com if/else (para fins didáticos):
df['PR_CAT'] = df['PR_CAT'].apply(lambda x: 'Sem Categoria' if pd.isna(x) else x)*

Principais Insights

1. Qualidade dos dados: a base contém resíduos de exportação (#N/D).
2. Imputação estratégica: preencher PR_CAT com "Sem Categoria" preserva vendas válidas.
3. Perfil demográfico: estatísticas de CL_FHL revelam a composição familiar dos clientes.
4. Concentração de vendas: as top 5 categorias concentram o maior volume.
5. Segmentação: diferenças entre segmentos A, B e C indicam comportamentos distintos.

Observações

Não fiz em ambiente virtual isolado, não criei o requirements.txt;
Se os commits estiverem estranhos é porquê uma parte eu fiz pelo computador e depois tive que finalizar pelo celular.

