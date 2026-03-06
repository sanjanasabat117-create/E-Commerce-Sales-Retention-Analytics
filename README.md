# E-Commerce Sales & Retention Analytics

![E-Commerce Data Analytics](https://img.shields.io/badge/Domain-E--Commerce-blue)
![Tech Stack](https://img.shields.io/badge/Tech_Stack-Python_|_SQL_|_Power_BI-brightgreen)
![Status](https://img.shields.io/badge/Status-Complete-success)

## 📂 Project Methodology
To ensure this analysis provides real business value, I followed a structured 4-stage analytical workflow:
1.  **Data Engineering & Synthesis**: Built a Python pipeline to generate 3 years of transactional data with realistic seasonal trends and logical constraints (e.g., users must join before they can order).
2.  **ETL & Quality Control**: Processed raw CSVs using SQL to validate date logic and handle null values.
3.  **Advanced Analytics**: Performed cohort retention and funnel conversion analysis using PostgreSQL window functions.
4.  **Strategic Visualization**: Developed a multi-page Power BI dashboard centered around a Star Schema model to deliver insights to stakeholders.

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

### Dashboard Preview:

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

## 📈 My Strategic Recommendations
Based on the dashboard insights, I proposed the following actions to the hypothetical business team:
1. **Reduce Clothing Returns**: Since "Wrong Size" is the top return reason (15% rate), implementing an AI-size recommender could recover ~$100K in annual revenue.
2. **Regional Expansion (Tier 2/3 Cities)**: India shows a 25% yearly growth in non-metro cities. Optimizing delivery logistics and adding vernacular (regional language) search could tap into a $200K revenue opportunity.
3. **Payment Optimization (UPI/COD)**: Since mobile is the primary channel, implementing deeper UPI integration and "One-Tap" payments would reduce cart abandonment by 10%.

---
*Created by Sanjana | [GitHub Repository](https://github.com/sanjanasabat117-create/E-Commerce-Sales-Retention-Analytics) | [LinkedIn](https://www.linkedin.com/in/sanjana-sabat-7b9872271)*
