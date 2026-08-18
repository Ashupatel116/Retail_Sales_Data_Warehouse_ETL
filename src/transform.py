import pandas as pd


def transform_date(df):

    # Convert Order Date from string to actual datetime
    order_dates = pd.to_datetime(
        df["Order Date"],
        format="%m/%d/%Y"
    )

    date_df = pd.DataFrame()

    # Generate every date between minimum and maximum order date
    date_df["full_date"] = pd.date_range(
        start=order_dates.min(),
        end=order_dates.max(),
        freq="D"
    )

    # Create date key
    date_df["date_key"] = (
        date_df["full_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    date_df["year"] = date_df["full_date"].dt.year

    date_df["quarter"] = date_df["full_date"].dt.quarter

    date_df["month"] = date_df["full_date"].dt.month

    date_df["month_name"] = date_df["full_date"].dt.month_name()

    date_df["day"] = date_df["full_date"].dt.day

    date_df["day_name"] = date_df["full_date"].dt.day_name()

    date_df = date_df[
        [
            "date_key",
            "full_date",
            "year",
            "quarter",
            "month",
            "month_name",
            "day",
            "day_name"
        ]
    ]

    return date_df

def transform_location(df):

    location_df = (
        df[
            [
                "Country",
                "City",
                "State",
                "Postal Code",
                "Region"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    location_df.insert(
        0,
        "location_key",
        range(1, len(location_df) + 1)
    )

    location_df = location_df.rename(
        columns={
            "Country": "country",
            "City": "city",
            "State": "state",
            "Postal Code": "postal_code",
            "Region": "region"
        }
    )

    return location_df

def transform_customer(df):

    customer_df = (
        df[
            [
                "Customer ID",
                "Customer Name",
                "Segment"
            ]
        ]
        .drop_duplicates(subset=["Customer ID"])
        .reset_index(drop=True)
    )

    customer_df.insert(
        0,
        "customer_key",
        range(1, len(customer_df) + 1)
    )

    customer_df = customer_df.rename(
        columns={
            "Customer ID": "customer_id",
            "Customer Name": "customer_name",
            "Segment": "segment"
        }
    )

    return customer_df


def transform_product(df):

    product_df = (
        df[
            [
                "Product ID",
                "Product Name",
                "Category",
                "Sub-Category"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    product_df.insert(
        0,
        "product_key",
        range(1, len(product_df) + 1)
    )

    product_df = product_df.rename(
        columns={
            "Product ID": "product_id",
            "Product Name": "product_name",
            "Category": "category",
            "Sub-Category": "sub_category"
        }
    )

    return product_df

def transform_sales(
    df,
    customer_df,
    product_df,
    location_df,
    date_df
):

    sales_df = df.copy()

    # Convert Order Date
    sales_df["Order Date"] = pd.to_datetime(
        sales_df["Order Date"],
        format="%m/%d/%Y"
    )

    # Customer Key

    customer_lookup = customer_df[
        ["customer_id", "customer_key"]
    ]

    sales_df = sales_df.merge(
        customer_lookup,
        left_on="Customer ID",
        right_on="customer_id",
        how="left"
    )

    # Product Key

    product_lookup = product_df[
        ["product_id", "product_name" ,"product_key"]
    ]

    sales_df = sales_df.merge(
        product_lookup,
        left_on=["Product ID",
                 "Product Name"
        ],
        right_on=["product_id",
                  "product_name"
        ],
        how="left"
    )

    # Location Key

    location_lookup = location_df[
        [
            "country",
            "city",
            "state",
            "postal_code",
            "region",
            "location_key"
        ]
    ]

    sales_df = sales_df.merge(
        location_lookup,
        left_on=[
            "Country",
            "City",
            "State",
            "Postal Code",
            "Region"
        ],
        right_on=[
            "country",
            "city",
            "state",
            "postal_code",
            "region"
        ],
        how="left"
    )

    # Date Key

    date_lookup = date_df[
        ["full_date", "date_key"]
    ]

    sales_df = sales_df.merge(
        date_lookup,
        left_on="Order Date",
        right_on="full_date",
        how="left"
    )

    # Create Fact Table

    fact_sales = sales_df[
        [
            "Order ID",
            "date_key",
            "product_key",
            "customer_key",
            "location_key",
            "Quantity",
            "Sales",
            "Discount",
            "Profit"
        ]
    ].copy()

    # Rename columns
    fact_sales = fact_sales.rename(
        columns={
            "Order ID": "transaction_id",
            "Quantity": "quantity",
            "Sales": "sales_amount",
            "Discount": "discount",
            "Profit": "profit"
        }
    )

    # Calculate unit price
    fact_sales["unit_price"] = (
        fact_sales["sales_amount"] /
        fact_sales["quantity"]
    )

    # Reorder columns
    fact_sales = fact_sales[
        [
            "transaction_id",
            "date_key",
            "product_key",
            "customer_key",
            "location_key",
            "quantity",
            "unit_price",
            "sales_amount",
            "discount",
            "profit"
        ]
    ]

    return fact_sales
