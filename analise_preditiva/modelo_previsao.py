import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sqlalchemy import create_engine

# ================================
# 1. Conexão com o banco de dados
# ================================
engine = create_engine("mysql+pymysql://root:123456@localhost/sistema_vendas")

# ================================
# 2. Coleta os dados de vendas
# ================================
query = """
SELECT
    p.nome_produto,
    SUM(i.quantidade) AS total_vendido,                     -- total vendido por produto
    AVG(i.preco_unitario) AS preco_medio,                   -- preço médio de venda
    SUM(i.quantidade * i.preco_unitario) AS faturamento     -- faturamento total
FROM itens_pedido i
JOIN produtos p ON p.produto_id = i.produto_id
GROUP BY p.produto_id
"""

df = pd.read_sql(query, con=engine)
print("Dados carregados do banco com sucesso!")
print(df)

# ================================
# 3. Preparar dados para o modelo
# ================================
X = df[['total_vendido', 'preco_medio']]  # variáveis independentes
y = df['faturamento']                      # variável dependente

# Divisão em treino e teste (80% treino, 20% teste)
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Criar e treinar o modelo
modelo = LinearRegression()
modelo.fit(X_treino, y_treino)

# ================================
# 4. Avaliação do modelo
# ================================
previsao = modelo.predict(X_teste)

# Erros e métricas
erro = mean_squared_error(y_teste, previsao)
raiz = math.sqrt(erro)
r2 = r2_score(y_teste, previsao)

print(f"\nAvaliação do Modelo")
print(f"Erro médio quadrático (MSE): {erro:.2f}")
print(f"Raiz do erro médio quadrático (RMSE): {raiz:.2f}")
print(f"Coeficiente de determinação (R²): {r2:.2f}")


# ================================
# 5. Previsão com novos dados
# ================================
print("\nPrevisão com entrada do usuário")
qtd = float(input("Digite a quantidade vendida: "))
preco = float(input("Digite o preço médio do produto: "))

entrada = pd.DataFrame([[qtd, preco]], columns=['total_vendido', 'preco_medio'])
previsao_usuario = modelo.predict(entrada)
print(f"Previsão de faturamento: R$ {previsao_usuario[0]:.2f}")

# ================================
# 6. Gráfico comparando previsões
# ================================
plt.figure(figsize=(10,6))
plt.plot(y_teste.values[:30], label="Valor Real", marker='o')
plt.plot(previsao[:30], label="Previsão do Modelo", marker='x')
plt.title('Comparação do valor real e da previsão de faturamento')
plt.xlabel("Índice do produto no conjunto de teste")
plt.ylabel("Faturamento (R$)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
