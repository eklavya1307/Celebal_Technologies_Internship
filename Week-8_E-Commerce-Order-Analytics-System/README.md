# Week 8 - E-Commerce Order Analytics System

## 📌 Project Overview

The **E-Commerce Order Analytics System** is an end-to-end data
analytics project developed using **Python, Pandas, SQLite, and SQL**.
It simulates a real-world e-commerce environment by generating realistic
datasets, cleaning and validating them, loading them into SQLite,
performing advanced SQL analytics, and generating business reports
through a Command Line Interface (CLI).

This project was developed as part of the **Celebal Technologies Data
Engineering Internship -- Week 8 Assignment**.

------------------------------------------------------------------------

# 🎯 Objective

-   Generate realistic e-commerce datasets with intentional
    inconsistencies.
-   Clean and validate data using Pandas.
-   Ensure referential integrity across multiple tables.
-   Load cleaned datasets into SQLite.
-   Perform SQL analytics using Joins, Aggregations, Window Functions,
    CTEs and Cohort Analysis.
-   Build a CLI reporting tool for business insights.
-   Handle edge cases to ensure robustness.

------------------------------------------------------------------------

# ✨ Features

-   Realistic Dataset Generation
-   Intentional Data Inconsistencies
-   Data Cleaning & Validation
-   SQLite Database Integration
-   SQL Analytics
-   Window Functions
-   Common Table Expressions (CTEs)
-   Cohort & Retention Analysis
-   Customer Segmentation
-   RFM Analysis
-   CLI Reporting Tool
-   Edge Case Handling

------------------------------------------------------------------------

# 🛠 Technologies Used

-   Python 3
-   Pandas
-   SQLite
-   SQL
-   Faker
-   Random
-   Tabulate

------------------------------------------------------------------------

# 📋 Requirements

Install the required Python libraries:

``` bash
pip install pandas faker tabulate
```

------------------------------------------------------------------------

# 📂 Project Structure

``` text
Week-8_E-Commerce-Order-Analytics-System/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── products.csv
│   │   ├── orders.csv
│   │   └── order_items.csv
│   │
│   ├── cleaned/
│   │   ├── customers_clean.csv
│   │   ├── products_clean.csv
│   │   ├── orders_clean.csv
│   │   └── order_items_clean.csv
│   │
│   └── ecommerce.db
│
├── scripts/
│   ├── generate_data.py
│   ├── clean_data.py
│   └── report_cli.py
│
├── sql/
│   ├── schema.sql
│   ├── aggregations.sql
│   ├── window_functions.sql
│   └── cohort_analysis.sql
│
├── output/
│   └── sample_reports/
│
└── README.md
```

------------------------------------------------------------------------

# 📊 Dataset Description

The project generates four datasets:

-   **customers.csv** -- Customer details
-   **products.csv** -- Product catalogue
-   **orders.csv** -- Order information
-   **order_items.csv** -- Item-level order details

------------------------------------------------------------------------

# ⚠ Intentional Data Inconsistencies

The generated datasets include:

-   Missing customer IDs
-   Invalid email addresses
-   Duplicate records
-   Wrong date formats
-   Mixed-case product names
-   Extra spaces in product names
-   Negative quantities
-   Missing values
-   Invalid references between tables

------------------------------------------------------------------------

# 🧹 Data Cleaning

Using **Pandas**, the project:

-   Handles missing values
-   Removes duplicates
-   Corrects data types
-   Fixes date formats
-   Normalizes product names
-   Validates email addresses
-   Checks referential integrity
-   Exports cleaned datasets

------------------------------------------------------------------------

# 🗄 SQLite Database

The cleaned datasets are loaded into the SQLite database:

``` text
data/ecommerce.db
```

The database contains:

-   Primary Keys
-   Foreign Keys
-   NOT NULL constraints

It is used for all SQL analytics and CLI reports.

------------------------------------------------------------------------

# 📈 SQL Analytics

The project implements:

### Aggregations

-   Revenue per customer
-   Revenue per category
-   Revenue per month
-   Top products
-   Top customers
-   Average Order Value (AOV)

### Window Functions

-   RANK()
-   DENSE_RANK()
-   LAG()
-   FIRST_VALUE()
-   LAST_VALUE()
-   NTILE()
-   SUM() OVER()
-   AVG() OVER()

### CTEs

-   Monthly revenue
-   Customer categorization
-   Growth analysis

### Cohort Analysis

-   Customer cohorts
-   Monthly retention
-   Churn vs repeat customers

### Customer Segmentation

-   Purchase frequency
-   Spend tier
-   RFM Analysis

------------------------------------------------------------------------

# 📝 SQL Queries Included

The project implements all required SQL queries:

1.  Revenue per Category
2.  Top Customers
3.  Month-wise Order Count
4.  Customers Without Delivered Orders
5.  Products with More Returns than Purchases
6.  Return Rate per Category
7.  Running Totals
8.  DENSE_RANK()
9.  LAG Analysis
10. Multi-Level CTE
11. NTILE Segmentation
12. Year-over-Year Comparison
13. First vs Last Purchase Category
14. Cumulative Revenue Distribution
15. Cohort Analysis
16. Frequently Bought Together Products

------------------------------------------------------------------------

# 💻 Command Line Reporting Tool

Generate reports using:

``` bash
python scripts/report_cli.py --report revenue
python scripts/report_cli.py --report top_customers
python scripts/report_cli.py --report retention
```

Reports are generated from the SQLite database and stored in:

``` text
output/sample_reports/
```

------------------------------------------------------------------------

# 🛡 Edge Case Handling

The project handles:

-   Missing order IDs
-   Invalid customer references
-   Invalid email addresses
-   Quantity = 0
-   Discount \> 100%
-   Future order dates
-   Empty query results
-   Invalid CLI arguments
-   Database connection errors

------------------------------------------------------------------------

# ▶ How to Run

### 1. Clone the repository

``` bash
git clone <repository-url>
```

### 2. Navigate to the project

``` bash
cd Week-8_E-Commerce-Order-Analytics-System
```

### 3. Install dependencies

``` bash
pip install pandas faker tabulate
```

### 4. Generate datasets

``` bash
python scripts/generate_data.py
```

Raw datasets will be created inside:

``` text
data/raw/
```

### 5. Clean datasets and create SQLite database

``` bash
python scripts/clean_data.py
```

Outputs:

``` text
data/cleaned/
data/ecommerce.db
```

### 6. Generate reports

``` bash
python scripts/report_cli.py --report revenue
python scripts/report_cli.py --report top_customers
python scripts/report_cli.py --report retention
```

Reports are saved in:

``` text
output/sample_reports/
```

------------------------------------------------------------------------

# 📚 Skills Demonstrated

-   Python Programming
-   Pandas
-   SQLite
-   SQL
-   Data Cleaning
-   Data Validation
-   Data Engineering
-   Window Functions
-   CTEs
-   Cohort Analysis
-   Customer Segmentation
-   RFM Analysis
-   CLI Development
-   Problem Solving

------------------------------------------------------------------------


