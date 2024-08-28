import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from xlsxwriter import Workbook
#import pyodbc as odbc


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


# Clean up category data
df_orders['Category'] = df_orders['Category'].replace('گوشی موبایل ', 'گوشی موبایل')
categories = ['All Categories'] + df_orders['Category'].unique().tolist()

# Formatting and cleaning date values
df_orders['Date_Formatted'] = df_orders['Date_Formatted'].fillna('0000-00-00')
df_orders = df_orders[df_orders['Date_Formatted'] != '0000-00-00']

# Ensure date is a string format
df_orders['Date_value'] = df_orders['Date_Formatted'].str.replace('-', '').astype(str)
sorted_dates = sorted(df_orders['Date_Formatted'].unique())

# Function to convert Persian date to Gregorian date
def persian_to_gregorian(persian_date_str):
    year, month, day = map(int, persian_date_str.split('-'))
    gregorian_date = persian.to_gregorian(year, month, day)
    return datetime(gregorian_date[0], gregorian_date[1], gregorian_date[2])
    
# Convert Persian dates to Gregorian
df_orders['Gregorian_Date'] = df_orders['Date_Formatted'].apply(persian_to_gregorian)

# Date range selection using calendar widget
b1, b2 = st.columns(2)
sorted_dates_gregorian = sorted(df_orders['Gregorian_Date'].unique())
start_date, end_date = b1.date_input(
    "Select Date Range",
    value=[sorted_dates_gregorian[0], sorted_dates_gregorian[-1]],
    min_value=sorted_dates_gregorian[0],
    max_value=sorted_dates_gregorian[-1]
)
selected_category = b2.selectbox('Select Category', categories)

# Convert Gregorian dates back to Persian format
def gregorian_to_persian(gregorian_date):
    persian_date = persian.from_gregorian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    return f'{persian_date[0]:04}-{persian_date[1]:02}-{persian_date[2]:02}'

# Convert the selected Gregorian dates back to Persian format
start_date_persian = gregorian_to_persian(start_date)
end_date_persian = gregorian_to_persian(end_date)

# Calculate the number of days in the selected range
num_days = (end_date - start_date).days + 1

# Calculate the previous date range
previous_start_date = start_date - timedelta(days=num_days)
previous_end_date = end_date - timedelta(days=num_days)

previous_start_date_persian = gregorian_to_persian(previous_start_date)
previous_end_date_persian = gregorian_to_persian(previous_end_date)

# Filter DataFrame by date and category
filtered_df = df_orders[
    (df_orders['Gregorian_Date'] >= start_date) &
    (df_orders['Gregorian_Date'] <= end_date)
]

# Filter DataFrame by current and previous date ranges
current_filtered_df = df_orders[(df_orders['Date_Formatted'] >= start_date_persian) & (df_orders['Date_Formatted'] <= end_date_persian)]
previous_filtered_df = df_orders[(df_orders['Date_Formatted'] >= previous_start_date_persian) & (df_orders['Date_Formatted'] <= previous_end_date_persian)]

# Apply category filter if necessary
if selected_category != 'All Categories':
    current_filtered_df = current_filtered_df[current_filtered_df['Category'] == selected_category]
    previous_filtered_df = previous_filtered_df[previous_filtered_df['Category'] == selected_category]

st.write(f'Domain of period time: {num_days}')
st.write(f'Current period range: {start_date_persian} to {end_date_persian}')
st.write(f'Previous period range: {previous_start_date_persian} to {previous_end_date_persian}')

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



st.plotly_chart(unit_stock_price_distribution(df_stocks))
col1, col2, col3, col4 = st.columns((5, 5, 5, 5))
with col1: 
    st.markdown("Up to 500 Thousand")
    st.plotly_chart(unit_stock_price_distribution1(df_stocks))
with col2:
    st.markdown("500 Thousand to 2.5 Millions")
    st.plotly_chart(unit_stock_price_distribution2(df_stocks))
with col3:
    st.markdown("2.5 Millions to 8 Millions")
    st.plotly_chart(unit_stock_price_distribution3(df_stocks))
with col4: 
    st.markdown("8 Millions to 200 Millions")
    st.plotly_chart(unit_stock_price_distribution4(df_stocks))

    
st.plotly_chart(unit_order_price_distribution(df_orders))
col1, col2, col3, col4 = st.columns((5, 5, 5, 5))
with col1:
    st.markdown("Up to 500 Thousand")
    st.plotly_chart(unit_order_price_distribution1(df_orders))
with col2:
    st.markdown("500 Thousand to 2.5 Millions")
    st.plotly_chart(unit_order_price_distribution2(df_orders))
with col3:
    st.markdown("2.5 Millions to 8 Millions")
    st.plotly_chart(unit_order_price_distribution3(df_orders))
with col4:
    st.markdown("8 Millions to 200 Millions")
    st.plotly_chart(unit_order_price_distribution4(df_orders))













