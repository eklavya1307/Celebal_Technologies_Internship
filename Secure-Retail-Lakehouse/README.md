# Secure Retail Data Lakehouse

## 📌 Project Overview

The **Secure Retail Data Lakehouse** is a Python-based batch data engineering project designed to securely process retail customer and transaction data before it is used for analytics.

Retail platforms such as e-commerce websites and Point-of-Sale (POS) systems collect sensitive customer information including Personally Identifiable Information (PII) and Payment Card Industry (PCI) data. This project demonstrates how such sensitive data can be protected using data masking, tokenization, and feature engineering while still enabling meaningful business analytics.

The project follows the **Medallion Architecture (Bronze → Silver → Gold)** to organize data into different processing stages.

---

# 🎯 Problem Statement

Retail organizations continuously collect customer and payment information such as:

- Customer Name
- Email Address
- Phone Number
- Date of Birth
- Shipping Address
- Credit Card Number
- CVV

Storing this information in plain text introduces major security risks including:

- Identity Theft
- Financial Fraud
- Internal Data Leakage
- Regulatory Non-Compliance (PCI-DSS, GDPR, DPDP)

This project focuses on securing sensitive customer information while generating analytics-ready datasets for business users.

---

# 🎯 Objectives

- Build a secure batch data pipeline using Python.
- Protect sensitive customer information.
- Remove highly sensitive payment information.
- Apply data masking and tokenization.
- Perform feature engineering for analytics.
- Generate business-ready datasets.
- Create an analytics dashboard.

---

# 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Hashlib
- Jupyter Notebook

---

# 🏗 Project Architecture

```
                  Raw Dataset
                       │
                       ▼
               Bronze Layer
             (Raw Ingested Data)
                       │
                       ▼
               Silver Layer
       (Cleaned & Secured Data)
                       │
                       ▼
                Gold Layer
        (Business Ready Data)
                       │
                       ▼
              Analytics Dashboard
```

---

# 📂 Project Structure

```
Secure-Retail-Lakehouse/
│
├── data/
│   └── retail_transactions.csv
│
├── bronze/
│   └── transactions_bronze.csv
│
├── silver/
│   └── transactions_silver.csv
│
├── gold/
│   ├── customer_spend.csv
│   ├── age_band_summary.csv
│   ├── monthly_region_sales.csv
│   ├── monthly_spend_trend.csv
│   ├── payment_method_distribution.csv
│   └── spend_category_summary.csv
│
├── dashboard/
│   ├── dashboard.png
│   └── dashboard.html
│
├── SecureRetailLakehouse.ipynb
├── README.md
└── requirements.txt
```

---

# 🥉 Bronze Layer

The Bronze layer stores the raw dataset immediately after ingestion.

### Operations Performed

- Read raw CSV dataset
- Basic validation
- Store raw data without transformations

No security transformations are applied in this layer.

---

# 🥈 Silver Layer

The Silver layer performs data cleaning and security transformations.

### Data Cleaning

- Remove duplicate records
- Handle missing values
- Standardize column names
- Convert Date of Birth into datetime format

### Security Transformations

- Hard Drop of CVV column
- Mask Customer Name
- Mask Email Address
- Mask Phone Number
- Mask Credit Card Number
- Generate SHA-256 Customer Token

### Feature Engineering

- Calculate Customer Age
- Create Age Band
- Create Spend Category

---

# 🥇 Gold Layer

The Gold layer contains business-ready analytical datasets.

Generated reports include:

- Customer Spend Summary
- Spend Category Summary
- Monthly Spend Trend
- Monthly Region Sales
- Payment Method Distribution
- Age Band Summary

These datasets are optimized for reporting and analytics.

---

# 🔒 Security Techniques Used

## Hard Drop

The CVV column is permanently removed immediately after data ingestion because it is highly sensitive and should never be stored.

---

## Data Masking

Sensitive customer information is masked before analytics.

### Examples

| Original | Masked |
|----------|---------|
| Rahul Sharma | R***********a |
| rahul@gmail.com | ra*****@gmail.com |
| 9876543210 | XXXXXX3210 |
| 4567123412345678 | ************5678 |

---

## SHA-256 Tokenization

Customer IDs are converted into SHA-256 hash values to prevent exposure of original identifiers while maintaining uniqueness.

---

# 📊 Dashboard

The dashboard provides business insights through various visualizations, including:

- Top Customers by Spend
- Spend Category Distribution
- Monthly Spend Trend
- Payment Method Distribution
- Customer Spending Analysis

The dashboard is available in:

- `dashboard/dashboard.png`
- `dashboard/dashboard.html`

---

# 🚀 How to Run

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project folder

```bash
cd Secure-Retail-Lakehouse
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Open the notebook

Open:

```
SecureRetailLakehouse.ipynb
```

Run all cells from top to bottom.

---

# 📁 Output

After execution, the project automatically generates:

- Bronze Dataset
- Silver Dataset
- Gold Analytical Reports
- Dashboard

---

# ⭐ Key Features

- Secure Batch Data Pipeline
- Medallion Architecture
- PII Protection
- PCI Protection
- Hard Drop of CVV
- Data Masking
- SHA-256 Tokenization
- Feature Engineering
- Business Analytics Dashboard

---

# 🔮 Future Enhancements

- Real-Time Data Ingestion using Apache Kafka
- Delta Lake Integration
- Data Encryption
- Role-Based Access Control (RBAC)
- Cloud Deployment (Azure / AWS)

---

# 📌 Conclusion

The Secure Retail Data Lakehouse demonstrates how sensitive retail customer data can be securely processed before analytics. By implementing Hard Drop, Data Masking, SHA-256 Tokenization, and Feature Engineering within the Bronze, Silver, and Gold architecture, the project protects Personally Identifiable Information (PII) and Payment Card Industry (PCI) data while enabling business teams to perform secure and meaningful analytics.

---

