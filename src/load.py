import mysql.connector
from config.config import DB_CONFIG


def get_connection():

    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

    return connection


def load_dim_customer(df, connection):

    cursor = connection.cursor()

    query = """
        INSERT INTO dim_customer
        (
            customer_key,
            customer_id,
            customer_name,
            segment
        )
        VALUES (%s, %s, %s, %s)
    """

    data = [
        (
            int(row["customer_key"]),
            row["customer_id"],
            row["customer_name"],
            row["segment"]
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(query, data)

    connection.commit()

    cursor.close()

    print(f"Loaded {len(data)} rows into dim_customer")


def load_dim_product(df, connection):

    cursor = connection.cursor()

    query = """
        INSERT INTO dim_product
        (
            product_key,
            product_id,
            product_name,
            category,
            sub_category
        )
        VALUES (%s, %s, %s, %s, %s)
    """

    data = [
        (
            int(row["product_key"]),
            row["product_id"],
            row["product_name"],
            row["category"],
            row["sub_category"]
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(query, data)

    connection.commit()

    cursor.close()

    print(f"Loaded {len(data)} rows into dim_product")


def load_dim_location(df, connection):

    cursor = connection.cursor()

    query = """
        INSERT INTO dim_location
        (
            location_key,
            country,
            city,
            state,
            postal_code,
            region
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            int(row["location_key"]),
            row["country"],
            row["city"],
            row["state"],
            int(row["postal_code"]),
            row["region"]
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(query, data)

    connection.commit()

    cursor.close()

    print(f"Loaded {len(data)} rows into dim_location")


def load_dim_date(df, connection):

    cursor = connection.cursor()

    query = """
        INSERT INTO dim_date
        (
            date_key,
            full_date,
            year,
            quarter,
            month,
            month_name,
            day,
            day_name
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            int(row["date_key"]),
            row["full_date"],
            int(row["year"]),
            int(row["quarter"]),
            int(row["month"]),
            row["month_name"],
            int(row["day"]),
            row["day_name"]
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(query, data)

    connection.commit()

    cursor.close()

    print(f"Loaded {len(data)} rows into dim_date")
    
def load_fact_sales(df, connection):

    cursor = connection.cursor()

    query = """
        INSERT INTO fact_sales
        (
            transaction_id,
            date_key,
            product_key,
            customer_key,
            location_key,
            quantity,
            unit_price,
            sales_amount,
            discount,
            profit
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    data = [
        (
            row["transaction_id"],
            int(row["date_key"]),
            int(row["product_key"]),
            int(row["customer_key"]),
            int(row["location_key"]),
            int(row["quantity"]),
            float(row["unit_price"]),
            float(row["sales_amount"]),
            float(row["discount"]),
            float(row["profit"])
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(query, data)
    connection.commit()
    cursor.close()

    print(f"Loaded {len(data)} rows into fact_sales")