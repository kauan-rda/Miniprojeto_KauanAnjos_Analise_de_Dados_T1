# Mini-Projeto: Análise Exploratória de Varejo

## 📌 Sobre o Projeto
Este projeto realiza uma Análise Exploratória de Dados (AED) em uma base real de varejo (`Base Varejo.csv`). O objetivo é limpar inconsistências de formatação e gerar estatísticas sobre o comportamento e demografia dos clientes.

## 🛠️ Como Executar
1. Instale as bibliotecas necessárias: `pip install pandas numpy`
2. Certifique-se de que o arquivo `Base Varejo.csv` está na mesma pasta.
3. Execute o script principal:
   ```bash
   python analise_varejo.py

Tratamento e Qualidade de Dados
Durante a etapa de limpeza, identificamos que a base continha colunas fantasmas geradas na exportação (Unnamed: 10 a 13) e campos de produtos preenchidos com o texto "#N/D". Utilizamos o numpy para converter essas anomalias textuais em nulos reais (NaN) para, então, removê-los e garantir que as análises estatísticas não fossem corrompidas.

Principais Insights
Demografia: A estatística descritiva da coluna CL_FHL detalha o número de filhos dos clientes, trazendo média, mediana, desvios e limites (máximo e mínimo).

Segmentação: A tabela dinâmica revela o perfil familiar de acordo com o segmento de compra do cliente (CL_SEG).

Estoque e Giro: Através da contagem de valores, listamos os produtos (PR_CAT) com maior giro comercial.