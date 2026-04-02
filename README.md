# Countries ETL Project

## Deskripsi
Project ini adalah mini ETL pipeline untuk mengambil data negara dan ibu kota dari API RestCountries, mentransformasi data, lalu menyimpannya ke Supabase PostgreSQL. Data kemudian divisualisasikan melalui dashboard Streamlit.

---

## Arsitektur
API RestCountries → Python ETL → Supabase PostgreSQL → Streamlit Dashboard

---

## Teknologi
- Python
- requests
- pandas
- psycopg2
- python-dotenv
- Supabase PostgreSQL
- Streamlit
- Plotly

---

## Setup Project

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup environment variables
Buat file .env di folder project:
```env
DB_HOST=your_host
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_PORT=5432
```

## Cara Menjalankan ETL
```bash
python etl_countries.py
```

## Cara Menjalankan Dashboard
```bash
streamlit run dashboard_countries.py
```
Lalu buka di browser:
```
http://localhost:8501
```

## Contoh Query SQL
```sql
SELECT 
    name,
    capital,
    region,
    name_length,
    capital_length,
    is_asia
FROM countries
LIMIT 10;
```

## Fitur
### ETL
- Extract data dari API
- Transform (data cleaning + enrichment)
- Load ke PostgreSQL
- Logging
- Error handling
- Idempotent pipeline (ON CONFLICT)

## Dashboard
- KPI (total negara, region)
- Filter region
- Search negara
- Visualisasi distribusi region

## Hasil
- Data bersih dan tidak duplikat
- Pipeline ETL modular
- Dashboard interaktif

## Live Demo
https://countries-etl-project-bzvcyx4t8apew83jcgjvnw.streamlit.app/

