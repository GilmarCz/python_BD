import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split    # separa dados em treino e teste
from sklearn.linear_model import LinearRegression       # modelo de Regressão Linear
from sklearn.metrics import mean_squared_error, r2_score  # métricas de avaliação
from sqlalchemy import create_engine

# Conexão com o banco de dados MySQL (sistema_vendas)
engine = create_engine("mysql+pymysql://root:123456@localhost/sistema_vendas")

# Consulta SQL: obtém o total vendido, preço médio e faturamento de cada produto
query = """
SELECT
    p.nome_produto,
    SUM(i.quantidade) AS total_vendido,                     -- quantidade total vendida
    AVG(i.preco_unitario) AS preco_medio,                   -- preço médio de venda
    SUM(i.quantidade * i.preco_unitario) AS faturamento     -- faturamento total
FROM itens_pedido i
JOIN produtos p ON p.produto_id = i.produto_id
GROUP BY p.produto_id
"""

# Carregar o resultado da query em um DataFrame
df = pd.read_sql(query, con=engine)
#print(df.head())
print(df)

# Definir variáveis independentes (X) e dependente (y)
X = df[['total_vendido','preco_medio']]  # entradas (features)
y = df['faturamento']                    # saída (target)

# Dividir os dados em treino (70%) e teste (30%)
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Criar e treinar o modelo de regressão linear
modelo = LinearRegression()
modelo.fit(X_treino, y_treino)

# Fazer previsões no conjunto de teste
previsao = modelo.predict(X_teste)

# Avaliar o modelo com métricas
erro = mean_squared_error(y_teste, previsao)   # quanto menor, melhor
r2 = r2_score(y_teste, previsao)               # quanto mais próximo de 1, melhor

print(f"\nErro médio quadrático (MSE): {erro:.2f}")
print(f"Raiz do erro médio quadrático em R$: {math.sqrt(erro):.2f}")
print(f"Coeficiente de determinação (R²): {r2:.2f}\n")

# # Mostrar os coeficientes da regressão
# print("\nCoeficientes do modelo:")
# print(f"Impacto do total vendido: {modelo.coef_[0]:.2f}")
# print(f"Impacto do preço médio: {modelo.coef_[1]:.2f}")
# print(f"Intercepto (valor base): {modelo.intercept_:.2f}")

# Prever um novo dado
print("\nPrevisão de novo dado\n")
novo_produto = pd.DataFrame([[500,35.00]], columns=['total_vendido','preco_medio'])
previsao2 = modelo.predict(novo_produto)
print(f"Faturamento estimado para 500 unidades a R$35,00 é: {previsao2[0]:.2f}\n")

plt.figure(figsize=(10,6))
plt.plot(y_teste.values[:90], label="Valor Real", marker='o')
plt.plot(previsao[:90], label="Previsão do Modelo", marker='x')
plt.title('Comparação do valor real e da previsão de faturamento')
plt.xlabel("Índice do produto no conjunto de teste")
plt.ylabel("Faturamento (R$)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()