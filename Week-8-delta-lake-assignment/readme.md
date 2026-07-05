# Week 7 - Delta Lake MERGE Implementation

## Overview

This project demonstrates data preprocessing using **Pandas** followed by **incremental data processing using Delta Lake MERGE** in **Databricks Free Edition**.

The assignment focuses on cleaning a retail sales dataset, creating a Delta table, generating incremental data, and applying the Delta Lake **MERGE** operation to update existing records and insert new records.

---

## Objectives

### Part A – Pandas Data Processing

- Load a CSV dataset into a Pandas DataFrame.
- Explore the dataset using various Pandas functions.
- Handle missing values.
- Remove duplicate records.
- Perform filtering and column selection.
- Create derived columns.
- Save the cleaned dataset as a new CSV file.

### Part B – Delta Lake MERGE

- Load the cleaned dataset into Spark.
- Rename columns for Delta Lake compatibility.
- Create a Delta table.
- Generate an incremental dataset.
- Perform Delta Lake MERGE.
- Validate the final dataset.
- Display the final results.

---

## Technologies Used

- Python
- Pandas
- PySpark
- Delta Lake
- Apache Spark
- Databricks Free Edition
- GitHub

---

## Dataset

**Dataset:** Sample Superstore Dataset

The dataset contains retail sales information including:

- Orders
- Customers
- Products
- Sales
- Quantity
- Discount
- Profit
- Region
- Category

Original Dataset Size:

- **Rows:** 9,994
- **Columns:** 21

---

## Project Workflow

### Part 1 – Data Cleaning Using Pandas

The following preprocessing steps were performed:

- Loaded the CSV dataset
- Explored the dataset
- Checked dataset shape
- Displayed column names
- Verified data types
- Checked missing values
- Removed duplicate records
- Filtered required records
- Selected required columns
- Created **Price** column
- Created **total_amount** column
- Exported cleaned dataset

Output:

```
cleaned_superstore.csv
```

---

### Part 2 – Delta Lake MERGE

The cleaned dataset was processed using Apache Spark.

The following operations were performed:

- Loaded cleaned CSV into Spark
- Renamed columns using underscores
- Created **customer_master** Delta table
- Created incremental dataset
- Stored incremental dataset as **customer_incremental**
- Applied Delta Lake MERGE operation
- Updated existing records
- Inserted new records
- Validated the final dataset

---

## Validation

The implementation was verified using multiple validation steps.

### Record Count

| Description | Count |
|------------|------:|
| Original Records | 9994 |
| Incremental Records | 10 |
| Final Records | 9999 |

### Duplicate Validation

- Duplicate Row_ID values checked
- No duplicate records found

### Updated Records

Existing records were successfully updated after MERGE.

### Newly Inserted Records

New records were inserted successfully into the master table.

---

## Project Structure

```
Week-8-delta-lake-assignment
│
├── data
│   ├── Sample_Superstore.csv
│   └── cleaned_superstore.csv
│
├── notebooks
│   └── delta_scd_assignment.ipynb
│
├── screenshots
│   ├── 01_dataset_preview.png
│   ├── 02_dataset_info.png
│   ├── 03_missing_values.png
│   ├── 04_duplicate_removal.png
│   ├── 05_derived_columns.png
│   ├── 06_spark_data_loading.png
│   ├── 07_customer_master.png
│   ├── 08_updated_records.png
│   ├── 09_new_records.png
│   ├── 10_incremental_dataset.png
│   ├── 11_customer_incremental.png
│   ├── 12_merge_operation.png
│   ├── 13_final_master_table.png
│   ├── 14_record_count_validation.png
│   ├── 15_duplicate_validation.png
│   ├── 16_summary_statistics.png
│   ├── 17_updated_records_after_merge.png
│   └── 18_newly_inserted_records.png
│
├── report
│   └── assignment_summary.pdf
│
└── README.md
```

---

## Results

The assignment successfully demonstrated:

- Data cleaning using Pandas
- Duplicate removal
- Missing value analysis
- Derived column creation
- Delta table creation
- Incremental data generation
- Delta Lake MERGE
- Data validation
- Incremental data processing

---

## Learning Outcomes

Through this assignment, the following concepts were learned:

- Data preprocessing using Pandas
- Data exploration techniques
- Data cleaning
- Spark DataFrames
- Delta Lake
- Incremental Data Processing
- Delta MERGE
- Databricks
- GitHub project organization

---

## References

- Kaggle – Sample Superstore Dataset

  https://www.kaggle.com/datasets/vivek468/superstore-dataset-final

- Microsoft Learn – Delta Lake MERGE

  https://learn.microsoft.com/en-us/azure/databricks/delta/merge


