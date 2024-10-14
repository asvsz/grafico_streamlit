import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates
import numpy as np

# Carregar o arquivo CSV com tratamento de separador decimal para a coluna 'Total'
file_path = 'dados/vendas.csv'
source = pd.read_csv(file_path, sep=';', decimal=',')

# Tratando valores nulos e convertendo as colunas apropriadas
source['Total'] = pd.to_numeric(source['Total'], errors='coerce')
source['Date'] = pd.to_datetime(source['Date'], format='%m/%d/%Y', errors='coerce')

# Adicionando a opção de seleção de mês na barra lateral
month_selected = st.sidebar.selectbox(
    'Escolha o mês para visualizar os resultados:',
    options=pd.date_range(start=source['Date'].min(), end=source['Date'].max(), freq='MS').strftime("%Y-%m").tolist()
)
# Filtrando os dados com base no mês selecionado
source['Month'] = source['Date'].dt.to_period('M')
filtered_data = source[source['Month'].astype(str) == month_selected]

# Função para formatar os números com 'K' e 'M'
def formatar_com_k(x, pos):
    if x >= 1000000:
        return f'{int(x/1000000)}M'
    elif x >= 1000:
        return f'{int(x/1000)}K'
    return f'{int(x)}'

# Criando uma linha para os dois primeiros gráficos
col1, col2 = st.columns(2)

# Cores
colors = ['#B3E5FC', '#2196F3', '#FFA07A']

# Definindo tamanho das fontes
font_size_title = 20
font_size_labels = 16
font_size_ticks = 14
font_size_yticks = 14

# -------------------------------------------------------------------------------------------------------------------
#                                                 GRÁFICOS

# Gráfico 1: Faturamento diário
# Agrupar por data e cidade
grouped_data = filtered_data.groupby(['Date', 'City']).agg({'Total': 'sum'}).reset_index()

cities = grouped_data['City'].unique()

with col1:
    fig1, ax1 = plt.subplots(figsize=(10, 6))

    bar_width = 0.8

    # Criando uma lista de posições no eixo x para cada data única
    x_positions = np.arange(len(grouped_data['Date']))

    for i, city in enumerate(cities):
        city_data = grouped_data[grouped_data['City'] == city]
        ax1.bar(city_data['Date'], city_data['Total'], label=city,
                color=colors[i % len(colors)], width=bar_width, align='center')

    ax1.set_xlabel('Data', fontsize=font_size_labels)
    ax1.set_ylabel('Total', fontsize=font_size_labels)
    ax1.set_title('Faturamento Diário', fontsize=font_size_title)
    ax1.tick_params(axis='y', labelsize=font_size_yticks)  # Aumentando os rótulos do eixo y
    ax1.legend(title='Cidade', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=font_size_ticks)

    # Formatação do eixo x
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=7))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))

    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=font_size_ticks)
    plt.tight_layout()
    st.pyplot(fig1)


# Gráfico 2: Faturamento por Tipo de Produto
with col2:
    grouped_data = filtered_data.groupby(['Product line', 'City']).agg({'Total': 'sum'}).reset_index()

    fig2, ax2 = plt.subplots(figsize=(10, 6))

    for i, city in enumerate(cities):
        city_data = grouped_data[grouped_data['City'] == city]
        ax2.barh(city_data['Product line'], city_data['Total'], label=city,
                 color=colors[i % len(colors)])

    ax2.set_xlabel('Tipo de Produto', fontsize=font_size_labels)
    ax2.set_ylabel('Faturamento Total', fontsize=font_size_labels)
    ax2.set_title('Faturamento por Tipo de Produto', fontsize=font_size_title)
    ax2.tick_params(axis='x', rotation=45, labelsize=font_size_ticks)
    ax2.tick_params(axis='y', labelsize=font_size_yticks)
    ax2.legend(title='Cidade', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=font_size_ticks)
    plt.tight_layout()
    st.pyplot(fig2)

# Criando uma linha para os últimos três gráficos
col3, col4, col5 = st.columns(3)

# Gráfico 3: Faturamento por Cidade
with col3:
    grouped_data = filtered_data.groupby('City').agg({'Total': 'sum'}).reset_index()

    fig3, ax3 = plt.subplots(figsize=(10, 10))

    for i, city in enumerate(cities):
        city_data = grouped_data[grouped_data['City'] == city]
        ax3.bar(city_data['City'], city_data['Total'], label=city,
                color=colors[i % len(colors)])

    ax3.set_ylabel('Faturamento Total', fontsize=font_size_labels)
    ax3.set_xlabel('Cidade', fontsize=font_size_labels)
    ax3.set_title('Faturamento por cidade', fontsize=font_size_title)
    ax3.tick_params(axis='x', rotation=45, labelsize=font_size_ticks)
    ax3.tick_params(axis='y', labelsize=font_size_yticks)  # Aumentando os rótulos do eixo y
    ax3.yaxis.set_major_formatter(FuncFormatter(formatar_com_k))  # Formatação dos números
    plt.tight_layout()
    st.pyplot(fig3)

# Gráfico 4: Faturamento por Tipo de Pagamento
with col4:
    grouped_data = filtered_data.groupby(['Payment']).agg({'Total': 'sum'}).reset_index()

    total_faturamento = grouped_data['Total'].sum()
    grouped_data['Percentage'] = (grouped_data['Total'] / total_faturamento) * 100

    labels = grouped_data['Payment']
    sizes = grouped_data['Percentage']

    fig4, ax4 = plt.subplots(figsize=(6, 6))
    ax4.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax4.axis('equal')
    plt.title('Faturamento por Tipo de Pagamento', fontsize=font_size_title)
    ax4.legend(title='', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=font_size_ticks)
    plt.tight_layout()
    st.pyplot(fig4)

# Gráfico 5: Avaliação Média
with col5:
    grouped_data = filtered_data.groupby('City').agg({'Rating': 'sum'}).reset_index()

    fig5, ax5 = plt.subplots(figsize=(10, 10))

    for i, city in enumerate(cities):
        city_data = grouped_data[grouped_data['City'] == city]
        ax5.bar(city_data['City'], city_data['Rating'], label=city,
                color=colors[i % len(colors)])

    ax5.set_ylabel('Rating', fontsize=font_size_labels)
    ax5.set_xlabel('Cidade', fontsize=font_size_labels)
    ax5.set_title('Avaliação Média', fontsize=font_size_title)
    ax5.tick_params(axis='x', rotation=45, labelsize=font_size_ticks)
    ax5.tick_params(axis='y', labelsize=font_size_yticks)
    plt.tight_layout()
    st.pyplot(fig5)
