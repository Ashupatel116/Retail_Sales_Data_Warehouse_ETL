from src.extract import extract_data

from src.transform import (
    transform_customer,
    transform_product,
    transform_location,
    transform_date,
    transform_sales
)

from src.load import (
    get_connection,
    load_dim_customer,
    load_dim_product,
    load_dim_location,
    load_dim_date,
    load_fact_sales
)


def main():

    # Extract data
    df = extract_data()

    # Transform data
    customer_df = transform_customer(df)
    product_df = transform_product(df)
    location_df = transform_location(df)
    date_df = transform_date(df)

    fact_sales_df = transform_sales(
        df,
        customer_df,
        product_df,
        location_df,
        date_df
    )

    # Validate fact table
    print("\n----- FACT KEY VALIDATION -----")

    print("Missing date_key:", fact_sales_df["date_key"].isna().sum())
    print("Missing product_key:", fact_sales_df["product_key"].isna().sum())
    print("Missing customer_key:", fact_sales_df["customer_key"].isna().sum())
    print("Missing location_key:", fact_sales_df["location_key"].isna().sum())

    print("Duplicate fact rows:", fact_sales_df.duplicated().sum())

    print("Fact row count:", len(fact_sales_df))
    print("Raw row count:", len(df))

    # Show transformed data
    print("\n----- CUSTOMER DIMENSION -----")
    print(customer_df.head())
    print("Shape:", customer_df.shape)

    print("\n----- PRODUCT DIMENSION -----")
    print(product_df.head())
    print("Shape:", product_df.shape)

    print("\n----- LOCATION DIMENSION -----")
    print(location_df.head())
    print("Shape:", location_df.shape)

    print("\n----- DATE DIMENSION -----")
    print(date_df.head())
    print("Shape:", date_df.shape)

    print("\n----- FACT SALES -----")
    print(fact_sales_df.head())
    print("Shape:", fact_sales_df.shape)

    # Load data into MySQL
    print("\n----- LOADING DATA -----")

    connection = get_connection()

    load_dim_customer(customer_df, connection)
    load_dim_product(product_df, connection)
    load_dim_location(location_df, connection)
    load_dim_date(date_df, connection)
    load_fact_sales(fact_sales_df, connection)

    connection.close()

    print("\nData loaded successfully!")


if __name__ == "__main__":
    main()