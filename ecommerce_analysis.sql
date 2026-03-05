-- ======================================================================
-- E-Commerce Sales and Retention Analysis SQL Script
-- Platform: PostgreSQL (Standard ANSI SQL compatible)
-- ======================================================================


-- ==========================================
-- 1. SCHEMA CREATION
-- ==========================================

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    country VARCHAR(50),
    join_date DATE,
    age INT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category VARCHAR(50),
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    cost DECIMAL(10,2)
);

CREATE TABLE sessions (
    session_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    session_start TIMESTAMP,
    duration_seconds INT,
    is_bounce INT,
    device VARCHAR(50)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id),
    session_id INT REFERENCES sessions(session_id),
    order_date TIMESTAMP,
    total_amount DECIMAL(10,2),
    status VARCHAR(50)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    unit_price DECIMAL(10,2)
);

CREATE TABLE returns (
    return_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    return_date TIMESTAMP,
    reason VARCHAR(100)
);

-- ==========================================
-- 2. SALES & PROFITABILITY KPIs
-- ==========================================

-- Query 1: Overall Revenue, Cost, and Profit Margin by Category
SELECT 
    p.category,
    SUM(oi.quantity * oi.unit_price) AS total_revenue,
    SUM(oi.quantity * p.cost) AS total_cost,
    SUM(oi.quantity * oi.unit_price) - SUM(oi.quantity * p.cost) AS total_profit,
    ROUND((SUM(oi.quantity * oi.unit_price) - SUM(oi.quantity * p.cost)) / 
          SUM(oi.quantity * oi.unit_price) * 100, 2) AS profit_margin_pct
FROM 
    order_items oi
JOIN 
    products p ON oi.product_id = p.product_id
JOIN 
    orders o ON oi.order_id = o.order_id
WHERE 
    o.status != 'Cancelled'
GROUP BY 
    p.category
ORDER BY 
    total_revenue DESC;

-- Query 2: Year-over-Year (YoY) Monthly Sales Growth
WITH MonthlyRevenue AS (
    SELECT 
        DATE_TRUNC('month', order_date) AS month_start,
        SUM(total_amount) AS current_month_revenue
    FROM 
        orders
    WHERE 
        status != 'Cancelled'
    GROUP BY 
        DATE_TRUNC('month', order_date)
)
SELECT 
    month_start,
    current_month_revenue,
    LAG(current_month_revenue, 12) OVER(ORDER BY month_start) AS previous_year_month_revenue,
    ROUND((current_month_revenue - LAG(current_month_revenue, 12) OVER(ORDER BY month_start)) / 
          LAG(current_month_revenue, 12) OVER(ORDER BY month_start) * 100, 2) AS yoy_growth_pct
FROM 
    MonthlyRevenue
ORDER BY 
    month_start;


-- ==========================================
-- 3. CUSTOMER RETENTION (COHORT ANALYSIS)
-- ==========================================

-- Query 3: Monthly Customer Retention Rates based on First Purchase
WITH FirstPurchase AS (
    SELECT 
        user_id,
        DATE_TRUNC('month', MIN(order_date)) AS cohort_month
    FROM 
        orders
    GROUP BY 
        user_id
),
CohortActivity AS (
    SELECT 
        o.user_id,
        fp.cohort_month,
        DATE_TRUNC('month', o.order_date) AS activity_month,
        EXTRACT(YEAR FROM AGE(DATE_TRUNC('month', o.order_date), fp.cohort_month)) * 12 + 
        EXTRACT(MONTH FROM AGE(DATE_TRUNC('month', o.order_date), fp.cohort_month)) AS month_index
    FROM 
        orders o
    JOIN 
        FirstPurchase fp ON o.user_id = fp.user_id
),
CohortSizes AS (
    SELECT 
        cohort_month,
        COUNT(DISTINCT user_id) AS initial_size
    FROM 
        FirstPurchase
    GROUP BY 
        cohort_month
),
RetentionMatrix AS (
    SELECT 
        ca.cohort_month,
        cs.initial_size,
        ca.month_index,
        COUNT(DISTINCT ca.user_id) AS active_users
    FROM 
        CohortActivity ca
    JOIN 
        CohortSizes cs ON ca.cohort_month = cs.cohort_month
    GROUP BY 
        ca.cohort_month, cs.initial_size, ca.month_index
)
SELECT 
    cohort_month,
    initial_size,
    month_index,
    active_users,
    ROUND((active_users::DECIMAL / initial_size) * 100, 2) AS retention_rate_pct
FROM 
    RetentionMatrix
WHERE 
    month_index > 0
ORDER BY 
    cohort_month, month_index;


-- ==========================================
-- 4. CONVERSION AND FUNNEL ANALYSIS
-- ==========================================

-- Query 4: Session to Order Conversion Rate by Device
SELECT 
    s.device,
    COUNT(DISTINCT s.session_id) AS total_sessions,
    COUNT(DISTINCT CASE WHEN s.is_bounce = 1 THEN s.session_id END) AS bounce_sessions,
    COUNT(DISTINCT o.order_id) AS successful_orders,
    ROUND(COUNT(DISTINCT CASE WHEN s.is_bounce = 1 THEN s.session_id END)::DECIMAL / 
          COUNT(DISTINCT s.session_id) * 100, 2) AS bounce_rate_pct,
    ROUND(COUNT(DISTINCT o.order_id)::DECIMAL / 
          COUNT(DISTINCT s.session_id) * 100, 2) AS conversion_rate_pct
FROM 
    sessions s
LEFT JOIN 
    orders o ON s.session_id = o.session_id AND o.status != 'Cancelled'
GROUP BY 
    s.device
ORDER BY 
    conversion_rate_pct DESC;


-- ==========================================
-- 5. RETURN ANALYTICS
-- ==========================================

-- Query 5: Product Return Rate and Top Return Reasons by Category
WITH CategoryMetrics AS (
    SELECT 
        p.category,
        SUM(oi.quantity) AS total_items_sold,
        COUNT(r.return_id) AS total_items_returned
    FROM 
        order_items oi
    JOIN 
        products p ON oi.product_id = p.product_id
    LEFT JOIN 
        returns r ON oi.order_id = r.order_id AND oi.product_id = r.product_id
    GROUP BY 
        p.category
)
SELECT 
    cm.category,
    cm.total_items_sold,
    cm.total_items_returned,
    ROUND((cm.total_items_returned::DECIMAL / cm.total_items_sold) * 100, 2) AS return_rate_pct,
    MODE() WITHIN GROUP (ORDER BY r.reason) AS most_common_return_reason
FROM 
    CategoryMetrics cm
LEFT JOIN 
    products p ON cm.category = p.category
LEFT JOIN 
    returns r ON p.product_id = r.product_id
GROUP BY 
    cm.category, cm.total_items_sold, cm.total_items_returned, cm.total_items_returned
ORDER BY 
    return_rate_pct DESC;
