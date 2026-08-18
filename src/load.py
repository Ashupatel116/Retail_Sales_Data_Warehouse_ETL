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