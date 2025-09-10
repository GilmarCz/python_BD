import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Etapa 1
url_bitcoin = "bitcoin_historico.csv"
df_bitcoin = pd.read_csv(url_bitcoin)
print("Dados carregados com sucesso!!!")
print("Colunas:", df_bitcoin.columns)
print("\n" + "="*60 + "\n")

# Converter Data para datetime
df_bitcoin['Data'] = pd.to_datetime(df_bitcoin['Data'], format="%d.%m.%Y")

# Ordenar por data (mais antigo para mais recente)
df_bitcoin = df_bitcoin.sort_values('Data').reset_index(drop=True)
print("DataFrame ordenado por data (mais antigo -> mais recente):")
print(df_bitcoin)
print("\n" + "="*60)

# Etapa 2 - Limpeza e transformação dos dados
for col in ['Último','Abertura','Máxima','Mínima','Vol.','Var%']:
    df_bitcoin[col] = df_bitcoin[col].astype(str)
    df_bitcoin[col] = (df_bitcoin[col]
        .str.replace('K','000')
        .str.replace('M','000000')
        .str.replace('B','000000000')
        .str.replace('%','')
        .str.replace('.','')
        .str.replace(',','.')
    )
    df_bitcoin[col] = df_bitcoin[col].astype(float)
    if col == 'Var%':
        df_bitcoin[col] = df_bitcoin[col] / 100

# Remove valores faltantes
df_bitcoin = df_bitcoin.dropna()

print("DataFrame após a limpeza e transformação:")
print(df_bitcoin.head())
print("\n" + "="*60)
print("Tipos de dados após a limpeza:")
print(df_bitcoin.dtypes)

# Etapa 3 – Separação dos dados
data_treino_fim = pd.to_datetime("2025-08-16")
data_teste_inicio = pd.to_datetime("2025-08-17")
data_teste_fim = pd.to_datetime("2025-09-01")

df_treino = df_bitcoin[df_bitcoin['Data'] <= data_treino_fim]
df_teste = df_bitcoin[(df_bitcoin['Data'] >= data_teste_inicio) & (df_bitcoin['Data'] <= data_teste_fim)]

print("Conjunto de treino:")
print(df_treino.tail())
print("\n" + "="*60 + "\n")
print("Conjunto de teste:")
print(df_teste)

# Etapa 4 – Preparação dos dados
X_treino = df_treino[['Abertura', 'Máxima', 'Mínima', 'Vol.', 'Var%']]
y_treino = df_treino['Último']
X_teste = df_teste[['Abertura', 'Máxima', 'Mínima', 'Vol.', 'Var%']]
y_teste = df_teste['Último']

# Criar e treinar o modelo
modelo = LinearRegression()
modelo.fit(X_treino, y_treino)

# Etapa 5 – Previsão e Avaliação
previsao = modelo.predict(X_teste)
erro = mean_squared_error(y_teste, previsao)
r2 = r2_score(y_teste, previsao)

print("Avaliação do Modelo:")
print(f"Erro Médio Quadrático (MSE): {erro:.2f}")
print(f"Coeficiente de Determinação (R²): {r2:.2f}")

# Etapa 6 – Visualização
plt.figure(figsize=(10,6))
plt.plot(df_teste['Data'], y_teste, label='Valor Real', marker='o')
plt.plot(df_teste['Data'], previsao, label='Previsão', marker='x')
plt.title("Previsão do Preço de Fechamento do Bitcoin")
plt.xlabel("Data")
plt.ylabel("Preço de Fechamento (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
