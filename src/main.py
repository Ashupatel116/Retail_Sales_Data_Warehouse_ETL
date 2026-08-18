from src.extract import extract_data
from src.transform import transform_customer, transform_product


def main():

    df = extract_data()

    customer_df = transform_customer(df)
    product_df = transform_product(df)

    print("\n----- CUSTOMER DIMENSION -----")
    print(customer_df.head())

    print("\nCustomer Shape:")
    print(customer_df.shape)

    print("\n----- PRODUCT DIMENSION -----")
    print(product_df.head())

    print("\nProduct Shape:")
    print(product_df.shape)


if __name__ == "__main__":
    main()