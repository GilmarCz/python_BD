import pandas as pd
from sqlalchemy import create_engine

# Criar engine de conexão
engine = create_engine("mysql+pymysql://root:123456@localhost/sistema_vendas")

# # Carregar tabelas necessárias
produtos = pd.read_sql("SELECT produto_id, nome_produto FROM produtos", con=engine)
itens = pd.read_sql("SELECT produto_id, quantidade, preco_unitario FROM itens_pedido", con=engine)

# Juntar tabelas (merge pelo produto_id)
df_vendas = pd.merge(itens, produtos, on="produto_id")

# Calcular quantidade total e valor total por produto
relatorio = df_vendas.groupby(["produto_id", "nome_produto"]).agg(
    quantidade_total=("quantidade", "sum"),
    valor_total=("preco_unitario", lambda x: (x * df_vendas.loc[x.index, "quantidade"]).sum())
).reset_index()

# Ordenar pelo mais vendido
relatorio = relatorio.sort_values(by="quantidade_total", ascending=False)

print("Produtos mais vendidos:")
print(relatorio.head(10))  # mostra os 10 mais vendidos

print("Itens de pedido:")
print(itens.head())
print("Total de itens:", len(itens))

print("Produtos cadastrados:", produtos["produto_id"].nunique())
print("Produtos nos itens_pedido:", itens["produto_id"].nunique())

print("IDs de produtos nos pedidos que não estão em produtos:")
print(set(itens["produto_id"]) - set(produtos["produto_id"]))

df_vendas = pd.merge(itens, produtos, on="produto_id", how="left")
