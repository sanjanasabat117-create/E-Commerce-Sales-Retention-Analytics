# E-Commerce Sales & Retention Analytics

![E-Commerce Data Analytics](https://img.shields.io/badge/Domain-E--Commerce-blue)
![Tech Stack](https://img.shields.io/badge/Tech_Stack-Python_|_SQL_|_Power_BI-brightgreen)
![Status](https://img.shields.io/badge/Status-Complete-success)

## 📌 Project Overview
This project is an end-to-end data analytics solution designed to evaluate e-commerce performance, uncover sales trends, and analyze customer retention. Using a synthetic dataset representing a global retail footprint, this project simulates a real-world business environment where actionable insights are extracted through Python, SQL, and Power BI.

The analysis tackles critical business questions regarding revenue growth, product return rates, session-to-order conversions, and long-term customer loyalty (cohort retention).

## 🚀 Business Problems Addressed
1. **Sales & Profitability Tracking**: Identifying the most profitable product categories and evaluating year-over-year growth.
2. **Customer Retention**: Understanding user drop-off over time through cohort analysis.
3. **Funnel Conversion rates**: Analyzing how many user sessions actively convert into successful orders, and examining bounce rates across device types.
4. **Returns Management**: Determining the monetary impact of product returns and identifying the most common return reasons to improve quality control.

## 🛠️ Tech Stack & Skills Demonstrated
* **Python (pandas, numpy, faker)**: Used to engineer 5 interconnected synthetic datasets (Users, Products, Sessions, Orders, Returns) representing 5,000 users and complex timestamp relationships.
* **SQL (PostgreSQL)**: Complex querying involving CTEs (Common Table Expressions), Window Functions (`LAG`, `OVER`), aggregation, and multi-table joins.
* **Power BI / DAX**: Star Schema data modeling, custom DAX measures for YTD Sales and Profit Margins, and dynamic dashboard creation.
* **Data Concepts**: ETL pipelines, Entity-Relationship Modeling, Cohort Analysis, Funnel Analytics.

## 📊 Data Architecture
The data models follow a standard Star Schema optimized for OLAP analytics:
* **Fact Tables**: `orders`, `order_items`, `returns`
* **Dimension Tables**: `users`, `products`, `sessions`

*(To generate the data locally, run `python data_generator.py` which will output CSVs into the `/data` folder.)*

## 💡 Key SQL Insights (Highlights)
You can find the comprehensive SQL queries in `ecommerce_analysis.sql`. Some major analytical highlights include:
1. **YoY Growth Analysis**: Uses window functions to track trailing 12-month revenue growth to highlight seasonal performance.
2. **Monthly Cohort Retention**: Uses intricate CTEs and date truncation to build a traditional "triangle" retention matrix, tracking active user percentages month-by-month.
3. **Session-to-Order Conversions**: Aggregates bounce rates and tracks funnel attrition broken down by device type.

## 📊 Dashboard Visualizations
The analysis is presented through a 3-page interactive Power BI dashboard. For a detailed breakdown of each page with full-resolution screenshots, please see:

👉 **[View Detailed Dashboard Analysis](DASHBOARD.md)**

### Quick KPI Highlights
* **Total Revenue**: $2.10M
* **Profit Margin**: 40.82%
* **Conversion Rate**: 14.4%
* **Top Category**: Electronics

---

## 🧠 Challenges & Human Insights
*(Why this project is realistic)*
* **Date Consistency**: Engineering the data so that a product is never returned *before* it's bought, and users don't place orders *before* they join.
* **Complex SQL**: The cohort retention matrix required advanced logic to "pivot" dates into monthly indexes, a common real-world hurdle for Data Analysts.
* **Aesthetic vs Functional**: Balancing high-level KPIs with granular operational data (like return reasons) to serve both Executives and Operations Managers.

## 📈 Key Business Recommendations
1. **Reduce Clothing Returns**: Since "Wrong Size" is a top return reason, implementing an AI-size recommender could save ~5% in revenue leakage.
2. **Optimize Mobile Checkout**: With Mobile being the primary device, even a 1% increase in conversion rate would significantly boost the $2.1M baseline.
3. **Retention Strategy**: Focus on the 2nd-month drop-off seen in the cohort analysis by launching a "New Member" loyalty discount.

---
*Created by Sanjana | [GitHub Repository](https://github.com/sanjanasabat117-create/E-Commerce-Sales-Retention-Analytics) | [LinkedIn](https://www.linkedin.com/in/yourprofile)*

