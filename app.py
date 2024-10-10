import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file_path = 'dados/vendas.csv'

# Carregar o arquivo CSV com tratamento de separador decimal para a coluna 'Total'
source = pd.read_csv(file_path, sep=';', decimal=',')

# Tratando valores nulos e convertendo as colunas apropriadas
source['Total'] = pd.to_numeric(source['Total'], errors='coerce')
source['Date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y', errors='coerce')


# 1. Gráfico

# Agrupando os dados por semana (intervalo de 7 dias) e cidade, somando os totais
source['Week'] = source['Date'].dt.to_period('W')
grouped_data = source.groupby([source['Week'], 'City']).agg({'Total': 'sum'}).reset_index()

# Plotando o gráfico de barras com cores diferenciadas para diferentes cidades
fig, ax = plt.subplots(figsize=(10, 6))

# Usando uma paleta de cores para diferentes cidades
cities = grouped_data['City'].unique()
colors = plt.get_cmap('tab20').colors

# Definindo a largura das barras
bar_width = 0.8
x_positions = np.arange(len(grouped_data['Week'].unique()))

# Plotando o gráfico de barras
for i, city in enumerate(cities):
    city_data = grouped_data[grouped_data['City'] == city]


    ax.bar(city_data['Week'].dt.strftime('%d/%m/%Y'), city_data['Total'], label=city,
           color=colors[i % len(colors)], width=bar_width, align='center')

# Configurando o gráfico
ax.set_xlabel('Semana')
ax.set_ylabel('Total')
ax.set_title('Faturamento por a cada 7 dias')
ax.tick_params(axis='x', rotation=45)

ax.legend(title='Cidade', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()

st.pyplot(fig)


# 2. Gráfico

grouped_data = source.groupby(['Product line', 'City']).agg({'Total': 'sum'}).reset_index()

cities = grouped_data['City'].unique()

# Plotando o gráfico de barras com faturamento por tipo de produto
fig2, ax = plt.subplots(figsize=(10, 6))

for i, city in enumerate(cities):
    city_data = grouped_data[grouped_data['City'] == city]

    ax.barh(city_data['Product line'], city_data['Total'], label=city,
            color=colors[i % len(colors)])

# Configurando o gráfico
ax.set_xlabel('Tipo de Produto')
ax.set_ylabel('Faturamento Total')
ax.set_title('Faturamento Total por Tipo de Produto')
ax.tick_params(axis='x', rotation=45)  # Rotaciona os nomes dos produtos no eixo X para melhor visualização

# Adicionando a legenda fora do gráfico
ax.legend(title='Cidade', bbox_to_anchor=(1.05, 1), loc='upper left')

# Ajustando o layout para não sobrepor os elementos
plt.tight_layout()

st.pyplot(fig2)
