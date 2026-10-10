import psycopg2
import os

database_name = os.environ.get("DATABASE_NAME")

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def create_all():
    print("Creating tables ...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Companies (
            company_id SERIAL PRIMARY KEY,
            company_name VARCHAR NOT NULL UNIQUE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR NOT NULL UNIQUE,
            description VARCHAR,
            price FLOAT,
            active BOOLEAN DEFAULT true,
            company_id INT REFERENCES Companies(company_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Warranties (
            warranty_id SERIAL PRIMARY KEY,
            warranty_months INT NOT NULL,
            product_id INT REFERENCES Products(product_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR NOT NULL UNIQUE
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
            product_id INT REFERENCES Products(product_id),
            category_id INT REFERENCES Categories(category_id)
        );
    """)

    conn.commit()

