import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Conexão com o banco de dados sistema_vendas
engine = create_engine("mysql+pymysql://root:123456@localhost/sistema_vendas")

# Carregar os produtos do banco
df = pd.read_sql("SELECT produto_id, nome_produto, preco_custo, preco_venda, estoque_atual FROM produtos", con=engine)

# Converter colunas em arrays NumPy
preco_custo = df['preco_custo'].to_numpy()
preco_venda = df['preco_venda'].to_numpy()
estoque = df['estoque_atual'].to_numpy()

# Calcular lucro unitário e lucro total em estoque
lucro_unitario = preco_venda - preco_custo
lucro_total = lucro_unitario * estoque

# Criar índice de rentabilidade ((lucro / custo) * 100)
indice_rentabilidade = (lucro_unitario / preco_custo) * 100
df['rentabilidade'] = np.round(indice_rentabilidade, 2)

# Calcular a média da rentabilidade
media_rentabilidade = df['rentabilidade'].mean()

# Filtrar produtos com rentabilidade abaixo da média
abaixo_da_media = df[df['rentabilidade'] < media_rentabilidade]

print("Média de rentabilidade geral: ", round(media_rentabilidade, 2), "%")
print("\nProdutos com rentabilidade abaixo da média:")
print(abaixo_da_media[['produto_id', 'nome_produto', 'preco_custo', 'preco_venda', 'rentabilidade']])


