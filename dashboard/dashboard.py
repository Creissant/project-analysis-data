import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')
from streamlit_folium import folium_static
import folium

#load data
customers_df = pd.read_csv("customers_df.csv")
order_items_df = pd.read_csv("order_items_df.csv")
order_orderItem_df = pd.read_csv("order_orderItem_df.csv")
order_payments_df = pd.read_csv("order_payments_df.csv")
order_reviews_df = pd.read_csv("order_reviews_df.csv")
orderItem_product_df = pd.read_csv("orderItem_product_df.csv")
orders_customers_df = pd.read_csv("orders_customers_df.csv")
sample_geolocation = pd.read_csv("sample_geolocation.csv")


with st.sidebar:
    # Judul dan deskripsi
    st.markdown("# Varrel E-commerce Dashboard")
    st.markdown("Welcome to Varrel E-commerce Dashboard, where you can explore various insights and analytics!")

    # Menambahkan logo perusahaan
    st.image("Logo.png", use_column_width=True)

st.header(':chart_with_upwards_trend::sparkles: Varrel E-commerce Dashboard :sparkles::chart_with_upwards_trend:')

st.subheader('Orders per Month')

# Konversi kolom order_purchase_timestamp menjadi tipe data datetime
order_orderItem_df['order_purchase_timestamp'] = pd.to_datetime(order_orderItem_df['order_purchase_timestamp'])

# Resample berdasarkan bulan dan hitung jumlah order
monthly_orders_df = order_orderItem_df.resample(rule='M', on='order_purchase_timestamp').agg({
    "order_id": "nunique",
    "price": "sum"
})

# Ubah indeks menjadi string format bulan-tahun
monthly_orders_df.index = monthly_orders_df.index.strftime('%Y-%m')

# Reset indeks
monthly_orders_df = monthly_orders_df.reset_index()

# Ubah nama kolom
monthly_orders_df.rename(columns={
    "order_id": "order_count",
    "price": "revenue"
}, inplace=True)

# Buat visualisasi di Streamlit
st.line_chart(monthly_orders_df.set_index("order_purchase_timestamp"))

st.subheader('Review Score Distribution')

# Hitung jumlah review unik untuk setiap skor review
review_counts = order_reviews_df.groupby('review_score')['review_id'].nunique().sort_index()

# Buat visualisasi di Streamlit
st.bar_chart(review_counts)


st.subheader('Customer Demographics')

customer_counts_city = customers_df.groupby('customer_city')['customer_id'].nunique().sort_values(ascending=True)
customer_counts_state = customers_df.groupby('customer_state')['customer_id'].nunique().sort_values(ascending=True)

# Membuat visualisasi menggunakan Matplotlib
fig, ax = plt.subplots(1, 2, figsize=(12, 8))

# Bar chart untuk jumlah pelanggan berdasarkan kota
ax[0].barh(customer_counts_city.tail(10).index, customer_counts_city.tail(10), color='darksalmon')
ax[0].set_title('Number of Customers by City')

# Bar chart untuk jumlah pelanggan berdasarkan negara bagian
ax[1].barh(customer_counts_state.tail(10).index, customer_counts_state.tail(10), color='lightcoral')
ax[1].set_title('Number of Customers by State')

# Menampilkan grafik
st.pyplot(fig)

st.subheader('Top 5 Product Categories')

result = orderItem_product_df.groupby(by="product_category_name").agg({
    "order_item_id": "sum",
    "price": "sum"
})

result_sorted = result.sort_values(by="order_item_id", ascending=False)

# Ambil 5 kategori produk yang paling sering dibeli
top_categories = result_sorted.head(5)

# Ambil 5 kategori produk yang paling sering dibeli
top_categories = result_sorted.head(5)

# Ambil 5 kategori produk yang paling jarang dibeli
bottom_categories = result_sorted.tail(5)

# Menampilkan visualisasi dalam dua kolom
col1, col2 = st.columns(2)

with col1:
    plt.figure(figsize=(10, 6))
    plt.bar(top_categories.index, top_categories['order_item_id'], color='darkkhaki')
    plt.title('Top 5 Most Purchased Product Categories')
    plt.xlabel(None)
    plt.ylabel('Total Number of Items Sold')
    plt.xticks(rotation=45)  # Rotasi label sumbu x agar tidak bertabrakan
    st.pyplot(plt.gcf())

with col2:
    plt.figure(figsize=(10, 6))
    plt.bar(bottom_categories.index, bottom_categories['order_item_id'], color='orange')
    plt.title('Top 5 Least Purchased Product Categories')
    plt.xlabel(None)
    plt.ylabel('Total Number of Items Sold')
    plt.xticks(rotation=45)  # Rotasi label sumbu x agar tidak bertabrakan
    st.pyplot(plt.gcf())


st.subheader('Geospatial Analysis of Customers (Sample of 1000 Customers)')

with open('geolocation_map.html', 'r') as f:
    map_html = f.read()

st.components.v1.html(map_html, width=800, height=600)

st.caption('Copyright (c) Varrel')