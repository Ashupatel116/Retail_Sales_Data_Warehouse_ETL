USE retail_dw;

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key INT PRIMARY KEY AUTO_INCREMENT,
    customer_id VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    segment VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_key INT PRIMARY KEY AUTO_INCREMENT,
    product_id VARCHAR(20) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_location (
    location_key INT PRIMARY KEY AUTO_INCREMENT,
    country VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code INT,
    region VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    day INT NOT NULL,
    day_name VARCHAR(20) NOT NULL
);

CREATE TABLE fact_sales (
    sales_key INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id VARCHAR(30) NOT NULL,
    date_key INT NOT NULL,
    product_key INT NOT NULL,
    customer_key INT NOT NULL,
    location_key INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(12,2) NOT NULL,
    sales_amount DECIMAL(14,2) NOT NULL,
    discount DECIMAL(5,2) NOT NULL,
    profit DECIMAL(14,2) NOT NULL,

    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (location_key) REFERENCES dim_location(location_key)
);