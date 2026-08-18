import pandas as pd


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