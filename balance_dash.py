import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



# Defining the Component of Connection String
DRIVER_NAME = "{ODBC Driver 17 for SQL Server}"
SERVER_NAME = "aminpour-lap"
DATABASE_NAME = "order_management"
USERNAME = "DGSERVICE\b.aminpour"


connection_string = f"""
    DRIVER={DRIVER_NAME};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""



#conn = odbc.connect(connection_string, pooling=False)
#cursor = conn.cursor()


# Returning All the Values from Fields and Records in Desired Table 
#query1 = """
#    SELECT * 
#    FROM order_management.dbo.orders_0101_0505
#"""

#result = cursor.execute(query1).fetchall()


# Page setting
st.set_page_config(layout="wide")

# Load custom CSS
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



# importing corresponding flat data
df_stocks = pd.read_csv('Stocks.csv')
df_orders = pd.read_csv('Orders.csv')

categories_ord = ['All categories'] + df_orders['Category'].unique().tolist()
categories_stc = ['All categories'] + df_stocks['Category'].unique().tolist()

selected_cat_ord = st.selectbox('categories for order table', categories_ord)

if selected_cat_ord != 'All categories': 
    filtered_ord = df_orders[df_orders['Category'] == selected_cat_ord]
else:
    filtered_ord = df_orders 




selected_cat_stc = st.selectbox('categories for stock table', categories_stc)

if selected_cat_stc != 'All categories':
    filtered_stc = df_stocks[df_stocks['Category'] == selected_cat_stc] 
else:
    filtered_stc = df_stocks



def unit_stock_price_distribution(df):
    # Define price bins with a more scalable approach
    min_price = 0
    max_price = 200000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/80 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['BasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity', title='Distribution of Stocks Unit Prices and Quantity Sold',
                 color_discrete_sequence=['gold'])
    
    return fig

def unit_stock_price_distribution1(df):
    # Define price bins with a more scalable approach
    min_price = 0
    max_price = 5000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['BasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['gold'])
    
    return fig

def unit_stock_price_distribution2(df):
    # Define price bins with a more scalable approach
    min_price = 5000000
    max_price = 25000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['BasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['gold'])
    
    return fig


def unit_stock_price_distribution3(df):
    # Define price bins with a more scalable approach
    min_price = 25000000
    max_price = 80000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['BasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['gold'])
    
    return fig

def unit_stock_price_distribution4(df):
    # Define price bins with a more scalable approach
    min_price = 80000000
    max_price = 200000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['BasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['gold'])
    
    return fig






def unit_order_price_distribution(df):
    # Define price bins with a more scalable approach
    min_price = 0
    max_price = 200000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/80 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['UnitBasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity', title= 'Distribution of Orders Unit Prices and Quantity Sold',
                 color_discrete_sequence=['silver'])
    
    return fig

def unit_order_price_distribution1(df):
    # Define price bins with a more scalable approach
    min_price = 0
    max_price = 5000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['UnitBasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['silver'])
    
    return fig


def unit_order_price_distribution2(df):
    # Define price bins with a more scalable approach
    min_price = 5000000
    max_price = 25000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['UnitBasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['silver'])
    
    return fig


def unit_order_price_distribution3(df):
    # Define price bins with a more scalable approach
    min_price = 25000000
    max_price = 80000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['UnitBasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['silver'])
    
    return fig

def unit_order_price_distribution4(df):
    # Define price bins with a more scalable approach
    min_price = 80000000
    max_price = 200000000
    # Define bin edges; these values can be adjusted as needed
    bin_edges = [min_price + i*(max_price-min_price)/40 for i in range(81)]
    bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]
    # Assign bin labels to each price
    df['PriceRange'] = pd.cut(df['UnitBasePrice'], bins=bin_edges, labels=bin_labels, include_lowest=True)
    # Aggregate quantity sold within each price range
    price_range_distribution = df.groupby('PriceRange').sum()[['Quantity']].reset_index()
    # Create bar chart
    fig = px.bar(price_range_distribution, x='PriceRange', y='Quantity',
                 color_discrete_sequence=['silver'])
    
    return fig






    
st.plotly_chart(unit_order_price_distribution(filtered_ord))
col1, col2, col3, col4 = st.columns((5, 5, 5, 5))
with col1:
    st.markdown("Up to 500 Thousand")
    st.plotly_chart(unit_order_price_distribution1(filtered_ord))
with col2:
    st.markdown("500 Thousand to 2.5 Millions")
    st.plotly_chart(unit_order_price_distribution2(filtered_ord))
with col3:
    st.markdown("2.5 Millions to 8 Millions")
    st.plotly_chart(unit_order_price_distribution3(filtered_ord))
with col4:
    st.markdown("8 Millions to 200 Millions")
    st.plotly_chart(unit_order_price_distribution4(filtered_ord))


st.plotly_chart(unit_stock_price_distribution(filtered_stc))
col1, col2, col3, col4 = st.columns((5, 5, 5, 5))
with col1: 
    st.markdown("Up to 500 Thousand")
    st.plotly_chart(unit_stock_price_distribution1(filtered_stc))
with col2:
    st.markdown("500 Thousand to 2.5 Millions")
    st.plotly_chart(unit_stock_price_distribution2(filtered_stc))
with col3:
    st.markdown("2.5 Millions to 8 Millions")
    st.plotly_chart(unit_stock_price_distribution3(filtered_stc))
with col4: 
    st.markdown("8 Millions to 200 Millions")
    st.plotly_chart(unit_stock_price_distribution4(filtered_stc))










