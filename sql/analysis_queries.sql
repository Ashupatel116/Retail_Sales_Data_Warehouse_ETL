USE retail_dw;


-- 1. Total Sales

SELECT
    SUM(sales) AS total_sales
FROM fact_sales;


-- 2. Total Profit

SELECT
    SUM(profit) AS total_profit
FROM fact_sales;


-- 3. Total Quantity Sold

SELECT
    SUM(quantity) AS total_quantity
FROM fact_sales;


-- 4. Sales and Profit by Category

SELECT
    p.category,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY p.category
ORDER BY total_sales DESC;


-- 5. Sales by Region

SELECT
    l.region,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_location l
    ON f.location_key = l.location_key
GROUP BY l.region
ORDER BY total_sales DESC;


-- 6. Sales by Year

SELECT
    d.year,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;


-- 7. Monthly Sales Trend

SELECT
    d.year,
    d.month,
    d.month_name,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_date d
    ON f.date_key = d.date_key
GROUP BY
    d.year,
    d.month,
    d.month_name
ORDER BY
    d.year,
    d.month;


-- 8. Top 10 Products by Sales

SELECT
    p.product_id,
    p.product_name,
    SUM(f.sales) AS total_sales
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_sales DESC
LIMIT 10;


-- 9. Top 10 Products by Profit

SELECT
    p.product_id,
    p.product_name,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_id,
    p.product_name
ORDER BY total_profit DESC
LIMIT 10;


-- 10. Customer Segment Performance

SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS customers,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_customer c
    ON f.customer_key = c.customer_key
GROUP BY c.segment
ORDER BY total_sales DESC;


-- 11. Loss-Making Products

SELECT
    p.product_id,
    p.product_name,
    SUM(f.sales) AS total_sales,
    SUM(f.profit) AS total_profit
FROM fact_sales f
JOIN dim_product p
    ON f.product_key = p.product_key
GROUP BY
    p.product_id,
    p.product_name
HAVING SUM(f.profit) < 0
ORDER BY total_profit;


-- 12. Sales by Ship Mode

SELECT
    ship_mode,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM fact_sales
GROUP BY ship_mode
ORDER BY total_sales DESC;