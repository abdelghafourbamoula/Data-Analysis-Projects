import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Streamlit Dashboard',
    page_icon=':bar_chart:',
    layout="wide"
)

@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io='supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000
    )
    df['hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df

df = get_data_from_excel()

# Sidebar
st.sidebar.header('Select Filter here')

city = st.sidebar.multiselect(
    'Select the City :',
    options=df['City'].unique(),
    default=df['City'].unique(),
)

customer_type = st.sidebar.multiselect(
    'Select the Customer Type',
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique(),
)

gender = st.sidebar.multiselect(
    'Select the Gender :',
    options=df['Gender'].unique(),
    default=df['Gender'].unique(),
)

df_selection = df.query("City == @city & Customer_type == @customer_type & Gender == @gender")

# main page
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# TOP KPI'S
total_sales = round(df_selection['Total'].sum(), 2)
avg_rating = round(df_selection['Rating'].mean(), 2)
stars_rating = ':star:' * int(round(avg_rating, 0))
avg_rating_by_transaction = round(df_selection['Total'].mean(), 2)

left_col, middle_col, right_col = st.columns(3)

with left_col:
    st.markdown("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with middle_col:
    st.markdown("Average Rating:")
    st.markdown(f"{avg_rating} {stars_rating}")

with right_col:
    st.markdown("Average Sales Per Transaction:")
    st.subheader(f"US $ {avg_rating_by_transaction}")

st.markdown('---')

# sales by product line [bar chart]
sales_by_product_line = df_selection.groupby(['Product line']).sum()[['Total']].sort_values(by='Total')

fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation='h',
    title="<b>Sales by Product Lines</b>",
    # template='plotly_white',
    color='Total',
    color_continuous_scale='PuBuGn'
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(showgrid=False)
)

# sales by hour line [bar chart]
sales_by_hour = df_selection.groupby(['hour']).sum()['Total']

fig_hourly_sales = px.bar(
    sales_by_hour,
    y='Total',
    x=sales_by_hour.index,
    title='<b>Sales by Hour</b>',
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template='plotly_white',
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=False)
)

left_col, right_col = st.columns(2)
left_col.plotly_chart(fig_hourly_sales, use_container_width=True)
right_col.plotly_chart(fig_product_sales, use_container_width=True)

# sales by year [line]
sales_by_date = df_selection.groupby(['Date']).sum()['Total'].reset_index()

fig_sales_by_date = px.area(
    sales_by_date,
    x='Date',
    y='Total',
    title='<b>Total Sales by Date</b>',
    color_discrete_sequence=["#CD0054"] * len(sales_by_product_line),
    template='plotly_white',
)

fig_sales_by_date.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
)

st.plotly_chart(fig_sales_by_date, use_container_width=True)

# gross income [scatter]
rating_group = df.groupby('Rating').sum().reset_index()

fig_gross_income = px.scatter(
    rating_group,
    x='Rating',
    y='gross income',
    size='Total',
    hover_name='Total',
    color='gross margin percentage',
    color_continuous_scale='Plasma'
)

fig_gross_income.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=False)
)

left_col, right_col = st.columns([1,3])
right_col.plotly_chart(fig_gross_income, use_container_width=True)
with left_col:
    st.markdown('#')
    st.markdown("Number of Sales:")
    st.subheader(f":round_pushpin: {len(df_selection)}")
    st.markdown("Average of Tax:")
    st.subheader(f":card_index: {round(df['Tax 5%'].mean(),2)} %")
    st.markdown("Number of Product lines:")
    st.subheader(f":beginner: {len(df_selection['Product line'].unique())}")


table_cols = ['Date', 'Product line','Unit price', 'Quantity', 'Tax 5%', 'Payment', 'Rating', 'cogs', 'gross income']
st.dataframe(df_selection[table_cols], use_container_width=True)

# hide streamlit style
hide_style = """
    <style>
        #MainMenu {visibility: hidden}
        footer {visibility: hidden}
        header {visibility: hidden}
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)