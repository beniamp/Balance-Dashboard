import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import jdatetime


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


# defining gregorian datetime in order to properly selecting date input 
def persian_to_gregorian(date):
  year , month, day = date.split('-')
  year = int(year)
  month = int(month)
  day = int(day)

  persian_date = jdatetime.date(year, month, day)
  gre_date = persian_date.togregorian()
  return gre_date

df_orders['Gregorian_Date'] = df_orders['Date_Formatted'].apply(persian_to_gregorian)



categories_ord = ['All categories'] + df_orders['Category'].unique().tolist()
categories_stc = ['All categories'] + df_stocks['Category'].unique().tolist()

sorted_dates_gregorian = df_orders['Gregorian_Date'].unique()
sorted_dates_gregorian = sorted(sorted_dates_gregorian)


# Date range selection using calendar widget
b1, b2 = st.columns(2)
start_date, end_date = b1.date_input(
    "Select Date Range",
    value=[sorted_dates_gregorian[0], sorted_dates_gregorian[-1]],
    min_value=sorted_dates_gregorian[0],
    max_value=sorted_dates_gregorian[-1]
)
selected_category = b2.selectbox('Select Category', categories_ord)

def gregorian_to_persian(gregorian_date):
    persian_date = persian.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    return f'{persian_date[0]:04}-{persian_date[1]:02}-{persian_date[2]:02}'

# Convert the selected Gregorian dates back to Persian format
start_date_persian = gregorian_to_persian(start_date)
end_date_persian = gregorian_to_persian(end_date)

st.write(f'Current period range:{start_date_persian} to {end_date_persian}')


if selected_cat_ord != 'All categories': 
    filtered_ord = df_orders[df_orders['Category'] == selected_cat_ord]
    filtered_stc = df_stocks[df_stocks['category'] == selected_cat_ord]
else:
    filtered_ord = df_orders 
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

st.plotly_chart(unit_stock_price_distribution(filtered_stc))











