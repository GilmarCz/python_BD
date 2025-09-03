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

# Converter colunas em arrays NumPy
preco_custo = df['preco_custo'].to_numpy()
preco_venda = df['preco_venda'].to_numpy()
estoque = df['estoque_atual'].to_numpy()

# ---- Cálculos principais ----
lucro_unitario = preco_venda - preco_custo
lucro_total = lucro_unitario * estoque
rentabilidade = (lucro_unitario / preco_custo) * 100

df['lucro_unitario'] = np.round(lucro_unitario, 2)
df['lucro_total'] = np.round(lucro_total, 2)
df['rentabilidade'] = np.round(rentabilidade, 2)

# ---- 1) Valor total de estoque ----
valor_total_estoque = np.sum(preco_venda * estoque)
print("\nValor total de estoque da empresa: R$", round(valor_total_estoque, 2))

# ---- 2) Produtos com lucro negativo ----
lucro_negativo = df[df['lucro_unitario'] < 0]
print("\nProdutos com lucro NEGATIVO:")
print(lucro_negativo[['produto_id', 'nome_produto', 'preco_custo', 'preco_venda', 'lucro_unitario']])

# ---- 3) Produtos com rentabilidade acima de 100% ----
rentabilidade_alta = df[df['rentabilidade'] > 100]
print("\nProdutos com rentabilidade acima de 100%:")
print(rentabilidade_alta[['produto_id', 'nome_produto', 'preco_custo', 'preco_venda', 'rentabilidade']])

# ---- 4) Criar coluna de categoria ----
df['categoria'] = np.where(df['rentabilidade'] > 100, "Alta",
                    np.where(df['rentabilidade'] >= 50, "Média", "Baixa"))

print("\nProdutos categorizados por rentabilidade:")
print(df[['produto_id', 'nome_produto', 'rentabilidade', 'categoria']].head(20))  # mostra só 20 primeiros
