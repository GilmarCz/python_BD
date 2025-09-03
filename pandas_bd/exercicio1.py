import pandas as pd
from sqlalchemy import create_engine

# Criar engine de conexão com SQLAlchemy
engine = create_engine("mysql+pymysql://root:123456@localhost/sistema_vendas")

# 1. Liste os produtos com status "Descontinuado".
produtos = pd.read_sql("SELECT produto_id, nome_produto, status_produto FROM produtos", con=engine)
descontinuados = produtos[produtos["status_produto"] == "Descontinuado"]
print("Produtos Descontinuados:")
print(descontinuados)

# 2. Calcule o valor total do estoque (preço_venda * estoque_atual).
df_estoque = pd.read_sql("SELECT produto_id, nome_produto, preco_venda, estoque_atual FROM produtos", con=engine)
df_estoque["valor_total"] = df_estoque["preco_venda"] * df_estoque["estoque_atual"]
valor_total = df_estoque["valor_total"].sum()
print("\nValor total em estoque:", valor_total)

# 3. Filtre os fornecedores da cidade de "Maringá" e status "Ativo".
fornecedores = pd.read_sql("SELECT fornecedor_id, nome_fornecedor, cidade, status_fornecedor FROM fornecedores", con=engine)
filtros = fornecedores[(fornecedores["cidade"] == "Maringá") & (fornecedores["status_fornecedor"] == "Ativo")]
print("\nFornecedores de Maringá (Ativos):")
print(filtros)

# 4. Agrupe os pedidos por forma de pagamento e calcule o valor médio de frete.
pedidos = pd.read_sql("SELECT forma_pagamento, valor_frete FROM pedidos", con=engine)
media_frete = pedidos.groupby("forma_pagamento")["valor_frete"].mean()
print("\nValor médio de frete por forma de pagamento:")
print(media_frete)

# 5. Liste os 5 produtos com menor margem de lucro (preco_venda - preco_custo).
df_lucro = pd.read_sql("SELECT produto_id, nome_produto, preco_custo, preco_venda FROM produtos", con=engine)
df_lucro["margem_lucro"] = df_lucro["preco_venda"] - df_lucro["preco_custo"]
menores_lucros = df_lucro.nsmallest(5, "margem_lucro")
print("\n5 Produtos com menor margem de lucro:")
print(menores_lucros)

