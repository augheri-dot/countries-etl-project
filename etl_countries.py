from dotenv import load_dotenv
import os

load_dotenv()

import requests
import psycopg2
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================
# EXTRACT
# =========================
def extract():
    logging.info("Mulai extract data dari API")
    url = "https://restcountries.com/v3.1/all?fields=name,capital,region"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    logging.info(f"Berhasil mengambil {len(data)} data dari API")
    return data

# =========================
# TRANSFORM
# =========================
def transform(data):
    logging.info("Mulai transform data")
    rows = []

    for item in data:
        name = item.get("name", {}).get("common")
        capitals = item.get("capital") or []
        capital = capitals[0] if capitals else None
        region = item.get("region")

        name_length = len(name) if name else 0
        capital_length = len(capital) if capital else 0
        is_asia = True if region == "Asia" else False

        rows.append(
            (
                name,
                capital,
                region,
                name_length,
                capital_length,
                is_asia
            )
        )

    df = pd.DataFrame(
        rows,
        columns=[
            "name",
            "capital",
            "region",
            "name_length",
            "capital_length",
            "is_asia"
        ]
    )

    logging.info(f"Transform selesai. Total baris: {len(df)}")
    return df

# =========================
# LOAD
# =========================
def load(df):
    logging.info("Mulai load data ke database")

    conn = None
    cur = None

    try:
        if not all([
            os.getenv("DB_HOST"),
            os.getenv("DB_NAME"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_PORT")
        ]):
            raise ValueError("Konfigurasi database di file .env belum lengkap")

        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            sslmode="require"
        )

        cur = conn.cursor()

        processed = 0
        upserted = 0

        for _, row in df.iterrows():
            cur.execute(
                """
                INSERT INTO countries (
                    name,
                    capital,
                    region,
                    name_length,
                    capital_length,
                    is_asia
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (name) DO UPDATE SET
                    capital = EXCLUDED.capital,
                    region = EXCLUDED.region,
                    name_length = EXCLUDED.name_length,
                    capital_length = EXCLUDED.capital_length,
                    is_asia = EXCLUDED.is_asia;
                """,
                (
                    row["name"],
                    row["capital"],
                    row["region"],
                    row["name_length"],
                    row["capital_length"],
                    row["is_asia"]
                )
            )
            processed += 1
            upserted += 1

        conn.commit()
        logging.info(f"Load selesai. Diproses: {processed}, Upserted: {upserted}")

    except Exception as e:
        logging.error(f"Terjadi error saat load ke database: {e}")
        if conn:
            conn.rollback()
        raise

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        logging.info("Koneksi database ditutup")
# =========================
# MAIN
# =========================
def main():
    try:
        logging.info("ETL dimulai")
        data = extract()
        df = transform(data)
        load(df)
        logging.info("ETL selesai")
    except Exception as e:
        logging.error(f"ETL gagal: {e}")

if __name__ == "__main__":
    main()