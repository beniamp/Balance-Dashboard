import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import jdatetime
from convertdate import persian



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



if selected_category != 'All categories': 
    filtered_ord = df_orders[df_orders['Category'] == selected_category]
    filtered_stc = df_stocks[df_stocks['Category'] == selected_category]
else:
    filtered_ord = df_orders 
    filtered_stc = df_stocks


filtered_ord = filtered_ord[(filtered_ord['Gregorian_Date'] >= start_date) & (filtered_ord['Gregorian_Date'] <= end_date)]


idx = st.slider(
    "Select Division Number",
    min_value=0,
    max_value=200,
    value=100)

agg_orders = filtered_ord.groupby(['ProductNameColor', 'Date_Formatted', 'Gregorian_Date', 'Category']).agg({'Quantity': 'sum', 'UnitBasePrice': 'sum'}).reset_index()
agg_stocks = filtered_stc.groupby(['ProductColorName', 'Category', 'Brand']).agg({'Quantity': 'sum', 'BasePrice': 'max'}).reset_index()
df_joined = pd.merge(agg_orders, agg_stocks, right_on='ProductColorName', left_on='ProductNameColor', how='outer')

df_joined['ProductNameColor'] = df_joined['ProductNameColor'].fillna(df_joined['ProductColorName'])
df_joined['Category_x'] = df_joined['Category_x'].fillna(df_joined['Category_y']) 
df_joined['Quantity_x'] = df_joined['Quantity_x'].fillna(0)
df_joined['UnitBasePrice'] = df_joined['UnitBasePrice'].fillna(df_joined['BasePrice'])

df_joined['ProductColorName'] = df_joined['ProductColorName'].fillna(df_joined['ProductNameColor'])
df_joined['Category_y'] = df_joined['Category_y'].fillna(df_joined['Category_x'])
df_joined['Brand'] = df_joined['Brand'].fillna('نامشخص')
df_joined['BasePrice'] = df_joined['BasePrice'].fillna(df_joined['UnitBasePrice'])

df_joined = df_joined.rename(columns={'ProductNameColor': 'ProductO', 'ProductColorName': 'ProductS',
                          'UnitBasePrice': 'BasePriceOrder', 'BasePrice': 'BasePriceStock',
                          'Quantity_x': 'Volume', 'Quantity_y': 'Availability',
                          'Category_x': 'CategoryO', 'Category_y': 'categoryS'})


df_joined['BasePriceOrder'] = df_joined['BasePriceOrder'].fillna(0)
df_joined['BasePriceStock'] = df_joined['BasePriceStock'].fillna(0)


min_price = df_joined['BasePriceStock'].min()
max_price = df_joined['BasePriceStock'].max()
print(min_price, max_price)  # Ensure both are float


# Define bin edges
bin_edges = [min_price + i * (max_price - min_price) / idx for i in range(idx + 1)]
bin_labels = [f'{int(bin_edges[i]):,}-{int(bin_edges[i+1]):,}' for i in range(len(bin_edges)-1)]


#df_joined['PriceRange'] = pd.cut(df_joined['BasePriceOrder'], bins=bin_edges, labels=bin_labels, include_lowest=True)
df_joined['PriceRangeS'] = pd.cut(df_joined['BasePriceStock'], bins=bin_edges, labels=bin_labels, include_lowest=True)

price_ranges = df_joined['PriceRangeS'].unique().sort_values()

start_range = st.selectbox('Starter', price_ranges)
ending_range = st.selectbox('Ending', price_ranges, index=len(price_ranges) - 1)
df_joined = df_joined[(df_joined['PriceRangeS'] >= start_range) & (df_joined['PriceRangeS'] <= ending_range)]


df_joined['PriceRangeS'] = pd.cut(df_joined['BasePriceStock'], bins=bin_edges, labels=bin_labels, include_lowest=True)

price_range_distributionS = df_joined.groupby('PriceRangeS').agg({'Availability': 'max'}).reset_index()
price_range_distributionO = df_joined.groupby('PriceRangeS').agg({'Volume': 'sum'}).reset_index()

price_ranges = df_joined['PriceRangeS'].unique()

# Create bar chart
fig1 = px.bar(price_range_distributionO, x='PriceRangeS', y='Volume',
             title='Distribution of Price Ranges Over Ordered Volume',
             labels={'PriceRange': 'Price Range', 'Volume': 'Total Volume'},
             color='Volume', color_continuous_scale='viridis')


st = df_joined.groupby(['ProductS']).agg({'PriceRangeS': 'max', 'Availability': 'max'}).reset_index().sort_values(by='PriceRangeS', ascending=False)
st_grouped = st.groupby('PriceRangeS', as_index=False)['Availability'].sum()

# Create bar chart
fig2 = px.bar(st_grouped, x='PriceRangeS', y='Availability',
             title='Distribution of Price Ranges Over Stock Availability',
             labels={'PriceRange': 'Price Range', 'Availability': 'Total Availability'},
             color='Availability', color_continuous_scale='viridis')



    
st.plotly_chart(fig1)

st.plotly_chart(fig2)


price_ranges = df_joined['PriceRangeS'].unique().sort_values()
price_range_table = st.selectbox('Select According Price Range', price_ranges)
df_joined = df_joined[df_joined['PriceRangeS'] == price_range_table]
df_joined['Availability'] = df_joined['Availability'].fillna(0)
df_joined = df_joined[['ProductO','Date_Formatted', 'CategoryO', 'Brand', 'Volume', 'Availability', 'PriceRangeS']].reset_index(drop=True)
grouped = df_joined.groupby('ProductO').agg({'Volume': 'sum', 'Availability': 'max'}).reset_index()

st.dataframe(grouped)










