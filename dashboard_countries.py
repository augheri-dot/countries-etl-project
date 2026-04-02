import streamlit as st
import pandas as pd
import psycopg2

st.set_page_config(page_title="Dashboard Ibu Kota Negara", layout="wide")

def get_connection():
    return psycopg2.connect(
        host=st.secrets["db_host"],
        database=st.secrets["db_name"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        port=st.secrets["db_port"],
        sslmode="require"
    )

@st.cache_data
def load_data():
    conn = get_connection()
    query = """
        SELECT
            id,
            name,
            capital,
            region,
            name_length,
            capital_length,
            is_asia
        FROM countries
        ORDER BY name;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

try:
    df = load_data()

    st.title("Dashboard Data Ibu Kota Negara")
    st.caption("Dashboard sederhana untuk eksplorasi data negara, ibu kota, dan region.")

    total_negara = len(df)
    total_region = df["region"].nunique()

    col1, col2 = st.columns(2)
    col1.metric("Total Negara", total_negara)
    col2.metric("Total Region", total_region)

    st.markdown("---")

    region_list = ["Semua"] + sorted(df["region"].dropna().unique().tolist())
    selected_region = st.selectbox("Pilih Region", region_list)

    filtered_df = df.copy()
    if selected_region != "Semua":
        filtered_df = filtered_df[filtered_df["region"] == selected_region]

    search = st.text_input("Cari Negara")
    if search:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search, case=False, na=False)
        ]

    st.subheader("Jumlah Negara per Region")
    region_counts = (
        filtered_df.groupby("region")
        .size()
        .reset_index(name="total_negara")
        .sort_values("total_negara", ascending=False)
    )

    if not region_counts.empty:
        st.bar_chart(region_counts.set_index("region"))
    else:
        st.info("Tidak ada data untuk filter yang dipilih.")

    st.subheader("Data Negara")
    st.dataframe(filtered_df, use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="countries_filtered.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Terjadi error: {e}")