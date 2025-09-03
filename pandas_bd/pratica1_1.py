import pandas as pd
from sqlalchemy import create_engine

# Criar engine de conexão
engine = create_engine("mysql+pymysql://root:123456@localhost/sistema_vendas")

query = """
SELECT
    p.nome_produto,
    SUM(i.quantidade) AS total_vendido,
    SUM(i.quantidade * i.preco_unitario) AS total_faturado
FROM itens_pedido i
JOIN produtos p ON i.produto_id = p.produto_id
GROUP BY p.nome_produto
ORDER BY total_vendido DESC
"""

df_vendas = pd.read_sql(query, con=engine)
print(df_vendas.head(10))
