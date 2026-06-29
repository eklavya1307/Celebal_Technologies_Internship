# Week 06: Spark Architecture and Data Processing

## Overview

This repository contains the **Week 06 Assignment** completed during the **Celebal Technologies Internship Program**.

The objective of this assignment is to understand the architecture of Apache Spark and perform efficient data processing using **PySpark DataFrames**. The assignment demonstrates Spark's execution model, DataFrame transformations, lazy evaluation, schema handling, optimized storage formats, and performance optimization techniques.

---

# Assignment Objectives

* Understand Apache Spark Architecture.
* Learn the roles of Driver, Cluster Manager, and Executors.
* Understand Client Mode and Cluster Mode.
* Learn Lazy Evaluation and Directed Acyclic Graph (DAG).
* Read data from CSV and Parquet files.
* Handle schemas while loading datasets.
* Perform DataFrame filtering and column selection.
* Rename columns and cast data types.
* Add new calculated columns.
* Understand Transformations and Actions.
* Learn Wide Transformations and Shuffle operations.
* Understand Predicate Pushdown optimization.
* Handle missing values efficiently.
* Build a complete Spark ETL Pipeline.
* Save processed data in CSV and Parquet formats.
* Follow Spark best practices for processing large datasets.

---

# Technologies Used

* Python
* Apache Spark (PySpark)
* Jupyter Notebook
* Java
* Hadoop (Windows Configuration)
* Git & GitHub

---

# Project Structure

```text
Week_06_Spark_Architecture_And_Processing/
│
├── README.md
├── Week6_Spark_Assignment.ipynb
│
├── Dataset/
│   └── spark_assignment_dataset.csv
│
├── Output/
│   ├── CSV_Output/
│   ├── Parquet_Output/
│   ├── Final_CSV/
│   └── Final_Parquet/
│
└── Screenshots/
    ├── 01_Project_Setup_And_Spark_Session.png
    ├── 02_CSV_Dataset_Loaded.png
    ├── 03_Dataset_Schema.png
    ├── 04_Dataset_Summary_Statistics.png
    ├── 05_Q5_Electronics_Filter_Output.png
    ├── 06_Q6_DataFrame_Transformation.png
    ├── 07_Q8_Filter_Completed_Orders.png
    ├── 08_Q10_Final_Price_Column.png
    ├── 09_Q12_Parquet_Read_And_Null_Filter.png
    ├── 10_Null_Value_Handling.png
    ├── 11_Wide_Transformation_GroupBy.png
    ├── 12_Shuffle_Execution_Plan.png
    ├── 13_Spark_Data_Pipeline.png
    └── 14_Final_Output_And_Verification.png
```

---

# Dataset

A custom dataset was created specifically for this assignment to include all the fields required to perform the requested Spark operations.

The dataset contains attributes such as:

* Order ID
* User ID
* Product ID
* Product Name
* Category
* Region
* Priority
* Status
* Quantity
* Price
* Base Price
* Amount
* Order Date

---

# Tasks Performed

## Q1

Understanding Spark Architecture

## Q2

Lazy Evaluation in Spark

## Q3

Reading CSV files with schema inference

## Q4

Comparison of CSV and Parquet file formats

## Q5

Filtering and selecting required columns

## Q6

Renaming columns and casting data types

## Q7

Understanding DAG and Fault Tolerance

## Q8

Filtering data using multiple conditions

## Q9

Predicate Pushdown optimization

## Q10

Creating a calculated column (`final_price`)

## Q11

Understanding Transformations and Actions

## Q12

Reading Parquet files and exporting processed CSV files

## Q13

Client Mode vs Cluster Mode

## Q14

Filtering using OR conditions

## Q15

Best practices (`show()` vs `collect()`)

---

# Spark ETL Pipeline

The assignment demonstrates a complete Spark data pipeline following the ETL process.

```
Read Dataset
      │
      ▼
Schema Handling
      │
      ▼
Transform Data
      │
      ▼
Filter Records
      │
      ▼
Handle Null Values
      │
      ▼
Generate New Columns
      │
      ▼
Save as CSV
      │
      ▼
Save as Parquet
```

---

# Spark Concepts Covered

* Spark Architecture
* Driver
* Cluster Manager
* Executors
* Client Mode
* Cluster Mode
* Lazy Evaluation
* DAG (Directed Acyclic Graph)
* DataFrame Operations
* Schema Handling
* Column Selection
* Filtering
* Renaming Columns
* Type Casting
* Transformations
* Actions
* Wide Transformations
* Shuffle
* Predicate Pushdown
* Null Value Handling
* CSV Processing
* Parquet Processing
* ETL Pipeline

---

# Performance Optimizations

The assignment demonstrates several Spark optimization techniques:

* Lazy Evaluation
* Predicate Pushdown
* Column Selection
* Wide Transformations
* Shuffle Operations
* Null Value Handling
* Efficient DataFrame Transformations
* Using `show()` instead of `collect()` for large datasets

---

# Output

The processed dataset is generated in both:

* CSV Format
* Parquet Format

The repository also includes execution screenshots demonstrating the successful completion of each major task.

---

# Learning Outcomes

After completing this assignment, the following concepts were learned:

* Understanding Spark Architecture
* Efficient Data Processing with PySpark
* Working with Spark DataFrames
* Handling Large Datasets
* Building ETL Pipelines
* Optimizing Spark Jobs
* Working with CSV and Parquet Formats
* Managing Missing Data
* Applying Spark Transformations and Actions
* Understanding Spark Execution Plans

---

# Conclusion

This assignment demonstrates the practical implementation of Apache Spark for distributed data processing. It covers Spark architecture, execution model, DataFrame operations, optimization techniques, file handling, and ETL pipeline development. The implementation follows Spark best practices and provides hands-on experience with real-world data engineering workflows.
