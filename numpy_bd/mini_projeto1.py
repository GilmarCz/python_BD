import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# Conexão com o banco de dados sistema_vendas
engine = create_engine("mysql+pymysql://root:123456@localhost/sistema_vendas")

# Carregar os produtos do banco
df = pd.read_sql("""
    SELECT produto_id, nome_produto, preco_custo, preco_venda, estoque_atual
    FROM produtos
""", con=engine)

# Calcular rentabilidade no Python
df['rentabilidade'] = ((df['preco_venda'] - df['preco_custo']) / df['preco_custo']) * 100

# Média da rentabilidade
media_rentabilidade = df['rentabilidade'].mean()

# Filtrar produtos abaixo da média
abaixo_da_media = df[df['rentabilidade'] < media_rentabilidade]

print("\n Produtos com rentabilidade abaixo da média:")
print(abaixo_da_media[['produto_id', 'nome_produto', 'preco_custo', 'preco_venda', 'rentabilidade']])