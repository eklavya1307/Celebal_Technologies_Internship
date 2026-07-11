# Secure Retail Data Lakehouse

## Project Overview

This project builds a simple Secure Retail Data Lakehouse using a Jupyter Notebook. It protects sensitive retail customer and payment data while still allowing business analytics through Bronze, Silver, and Gold layers.

The notebook is self-contained and recreates the dataset, layer files, Gold summaries, and dashboard automatically.

## Problem Statement

Retail systems collect sensitive information such as customer names, emails, phone numbers, Aadhaar numbers, addresses, dates of birth, card numbers, and CVV values. If stored in plain text, this data can lead to identity theft, fraud, and compliance issues.

This project solves the problem by hard-dropping CVV, masking PII and PCI fields, tokenizing customer identifiers, and creating analytics-safe Gold summaries.

## Objectives

- Create Bronze, Silver, and Gold layers.
- Remove CVV using a Hard Drop during ingestion.
- Mask customer PII and payment PCI fields.
- Generate SHA-256 customer tokens.
- Calculate age and create age bands.
- Create spend categories.
- Generate Gold layer analytical summaries.
- Create a dashboard image and optional HTML dashboard.
- Validate that sensitive data is protected.

## Bronze Layer

The Bronze layer stores the ingested retail dataset with minimal validation.

Important security step:

- `card_cvv` is removed immediately during Bronze ingestion.

Output:

- `bronze/transactions_bronze.csv`

## Silver Layer

The Silver layer contains protected transaction data.

Security transformations:

- Names are masked.
- Emails are masked.
- Phone numbers are masked.
- Aadhaar numbers are masked.
- Card numbers are masked.
- Customer IDs are replaced with SHA-256 tokens.
- Age, age band, spend category, and transaction month are created.

Output:

- `silver/transactions_silver.csv`

## Gold Layer

The Gold layer contains analytics-ready summary tables without direct PII or PCI fields.

Outputs:

- `gold/customer_spend.csv`
- `gold/spend_category_summary.csv`
- `gold/monthly_spend_trend.csv`
- `gold/payment_method_distribution.csv`
- `gold/age_band_summary.csv`
- `gold/monthly_region_sales.csv`

## Security Techniques

- Hard Drop of CVV
- Name masking
- Email masking
- Phone masking
- Aadhaar masking
- Card masking
- SHA-256/HMAC customer token generation
- Age band feature engineering
- Spend category feature engineering

## Dashboard

The notebook creates:

- `dashboard/dashboard.png`
- `dashboard/dashboard.html`

The dashboard includes:

- Top 10 customers by total spend
- Spend category distribution
- Total vs average spend by spend category
- Top 15 customers by average spend
- Monthly spend trend
- Payment method distribution

## Folder Structure

```text
SecureRetailLakehouse/
|
|-- data/
|-- bronze/
|-- silver/
|-- gold/
|-- dashboard/
|   |-- dashboard.png
|   `-- dashboard.html
|-- SecureRetailLakehouse.ipynb
|-- README.md
`-- requirements.txt
```

## How to Run

1. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

2. Open and run the notebook:

```text
SecureRetailLakehouse.ipynb
```

Run all cells from top to bottom. The notebook will recreate all required output files automatically.

