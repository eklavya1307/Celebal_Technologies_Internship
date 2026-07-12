from __future__ import annotations

import csv
import re
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
CLEAN_DIR = PROJECT_ROOT / "data" / "cleaned"
OUTPUT_DIR = PROJECT_ROOT / "output" / "sample_reports"
DB_PATH = PROJECT_ROOT / "data" / "ecommerce.db"
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def ensure_dirs() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def clean_customers(customers: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    issues: list[str] = []
    before = len(customers)
    customers = customers.drop_duplicates(subset=["customer_id"]).copy()
    issues.append(f"Removed {before - len(customers)} duplicate customers by customer_id.")

    invalid_emails = validate_emails(customers)
    issues.append(f"Found {len(invalid_emails)} invalid customer email addresses: {invalid_emails[:20]}.")

    customers["registration_date"] = pd.to_datetime(customers["registration_date"], errors="coerce")
    invalid_registration = customers["registration_date"].isna()
    issues.append(f"Dropped {int(invalid_registration.sum())} customers with invalid registration_date.")
    customers = customers.loc[~invalid_registration].copy()
    customers["registration_date"] = customers["registration_date"].dt.strftime("%Y-%m-%d")
    customers["customer_id"] = customers["customer_id"].astype(int)

    guest = pd.DataFrame(
        [{
            "customer_id": 0,
            "customer_name": "Guest Customer",
            "email": "guest@example.com",
            "registration_date": "2023-01-01",
            "customer_type": "REGULAR",
        }]
    )
    return pd.concat([guest, customers], ignore_index=True), issues


def validate_emails(customers: pd.DataFrame) -> list[int]:
    invalid = ~customers["email"].astype(str).str.match(EMAIL_RE)
    return customers.loc[invalid, "customer_id"].astype(int).tolist()


def clean_products(products: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    issues: list[str] = []
    before = len(products)
    products = products.drop_duplicates(subset=["product_id"]).copy()
    issues.append(f"Removed {before - len(products)} duplicate products by product_id.")

    normalized_names = products["product_name"].astype(str).str.strip().str.title()
    changed_names = products["product_name"].astype(str).ne(normalized_names)
    products["product_name"] = normalized_names
    issues.append(f"Normalized {int(changed_names.sum())} product names with extra spaces or mixed case.")

    products["cost_price"] = pd.to_numeric(products["cost_price"], errors="coerce")
    invalid_cost = products["cost_price"].isna() | (products["cost_price"] <= 0)
    issues.append(f"Dropped {int(invalid_cost.sum())} products with invalid cost_price.")
    return products.loc[~invalid_cost].copy(), issues


def clean_orders(orders: pd.DataFrame, customers: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    issues: list[str] = []
    before = len(orders)
    orders = orders.drop_duplicates(subset=["order_id"]).copy()
    issues.append(f"Removed {before - len(orders)} duplicate orders by order_id.")

    parsed_dates = pd.to_datetime(orders["order_date"], format="%Y-%m-%d %H:%M:%S", errors="coerce")
    wrong_format = parsed_dates.isna()
    reparsed = pd.to_datetime(orders.loc[wrong_format, "order_date"], format="%d-%m-%Y %H:%M:%S", errors="coerce")
    parsed_dates.loc[wrong_format] = reparsed
    issues.append(f"Fixed {int(reparsed.notna().sum())} DD-MM-YYYY order dates.")

    invalid_dates = parsed_dates.isna()
    future_dates = parsed_dates > pd.Timestamp.now()
    issues.append(f"Dropped {int(invalid_dates.sum())} orders with unparseable dates.")
    issues.append(f"Dropped {int(future_dates.sum())} orders with future order_date.")
    orders = orders.loc[~invalid_dates & ~future_dates].copy()
    parsed_dates = parsed_dates.loc[orders.index]
    orders["order_date"] = parsed_dates.dt.strftime("%Y-%m-%d %H:%M:%S")

    valid_customer_ids = set(customers["customer_id"].astype(int))
    missing_customer = orders["customer_id"].isna() | (orders["customer_id"].astype(str).str.strip().isin(["", "NULL", "None"]))
    orders.loc[missing_customer, "customer_id"] = 0
    issues.append(f"Replaced {int(missing_customer.sum())} missing customer_id values with guest customer_id=0.")

    orders["customer_id"] = pd.to_numeric(orders["customer_id"], errors="coerce").fillna(0).astype(int)
    unknown_customer = ~orders["customer_id"].isin(valid_customer_ids | {0})
    orders.loc[unknown_customer, "customer_id"] = 0
    issues.append(f"Converted {int(unknown_customer.sum())} unknown customer_id values to guest customer_id=0.")

    valid_statuses = {"PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"}
    invalid_status = ~orders["status"].isin(valid_statuses)
    issues.append(f"Dropped {int(invalid_status.sum())} orders with invalid status.")
    return orders.loc[~invalid_status].copy(), issues


def check_referential_integrity(order_items: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    valid_order_ids = set(orders["order_id"].astype(int))
    return order_items.loc[~order_items["order_id"].astype(int).isin(valid_order_ids)].copy()


def clean_order_items(order_items: pd.DataFrame, orders: pd.DataFrame, products: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    issues: list[str] = []
    before = len(order_items)
    order_items = order_items.drop_duplicates(subset=["item_id"]).copy()
    issues.append(f"Removed {before - len(order_items)} duplicate order items by item_id.")

    for column in ["order_id", "product_id", "quantity", "unit_price", "discount_percent"]:
        order_items[column] = pd.to_numeric(order_items[column], errors="coerce")

    invalid_numeric = order_items[["order_id", "product_id", "quantity", "unit_price", "discount_percent"]].isna().any(axis=1)
    issues.append(f"Dropped {int(invalid_numeric.sum())} order_items with invalid numeric values.")
    order_items = order_items.loc[~invalid_numeric].copy()

    orphan_items = check_referential_integrity(order_items, orders)
    valid_product_ids = set(products["product_id"].astype(int))
    unknown_product = ~order_items["product_id"].astype(int).isin(valid_product_ids)
    invalid_discount = (order_items["discount_percent"] < 0) | (order_items["discount_percent"] > 100)
    zero_quantity = order_items["quantity"] == 0
    invalid_price = order_items["unit_price"] <= 0

    issues.append(f"Dropped {len(orphan_items)} order_items referencing non-existent orders.")
    issues.append(f"Dropped {int(unknown_product.sum())} order_items referencing non-existent products.")
    issues.append(f"Dropped {int(invalid_discount.sum())} order_items with discount_percent outside 0-100.")
    issues.append(f"Dropped {int(zero_quantity.sum())} order_items with quantity equal to 0.")
    issues.append(f"Dropped {int(invalid_price.sum())} order_items with non-positive unit_price.")

    valid = (
        order_items["order_id"].astype(int).isin(set(orders["order_id"].astype(int)))
        & order_items["product_id"].astype(int).isin(valid_product_ids)
        & ~invalid_discount
        & ~zero_quantity
        & ~invalid_price
    )
    cleaned = order_items.loc[valid].copy()
    cleaned[["item_id", "order_id", "product_id", "quantity"]] = cleaned[["item_id", "order_id", "product_id", "quantity"]].astype(int)
    return cleaned, issues


def load_csv(connection: sqlite3.Connection, table: str, filename: str) -> int:
    path = CLEAN_DIR / filename
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []
        placeholders = ", ".join("?" for _ in columns)
        rows = [tuple(row[column] for column in columns) for row in reader]
    column_sql = ", ".join(columns)
    connection.executemany(f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})", rows)
    return len(rows)


def load_sqlite_database() -> dict[str, int]:
    if DB_PATH.exists():
        DB_PATH.unlink()
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON;")
    connection.executescript((PROJECT_ROOT / "sql" / "schema.sql").read_text(encoding="utf-8"))
    counts = {
        "customers": load_csv(connection, "customers", "customers_clean.csv"),
        "products": load_csv(connection, "products", "products_clean.csv"),
        "orders": load_csv(connection, "orders", "orders_clean.csv"),
        "order_items": load_csv(connection, "order_items", "order_items_clean.csv"),
    }
    connection.commit()
    connection.close()
    return counts


def verify_database() -> list[str]:
    connection = sqlite3.connect(DB_PATH)
    checks = [
        ("orphan_order_items", "SELECT COUNT(*) FROM order_items oi LEFT JOIN orders o ON oi.order_id = o.order_id WHERE o.order_id IS NULL"),
        ("orphan_orders", "SELECT COUNT(*) FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL"),
        ("invalid_discounts", "SELECT COUNT(*) FROM order_items WHERE discount_percent < 0 OR discount_percent > 100"),
        ("zero_quantity_items", "SELECT COUNT(*) FROM order_items WHERE quantity = 0"),
        ("future_orders", "SELECT COUNT(*) FROM orders WHERE date(order_date) > date('now')"),
    ]
    results = []
    for name, query in checks:
        value = connection.execute(query).fetchone()[0]
        results.append(f"{name}: {value}")
    connection.close()
    return results


def write_reports(section_messages: list[tuple[str, list[str]]], counts: dict[str, int]) -> None:
    report_lines = ["# Data Quality Report", ""]
    for section, messages in section_messages:
        report_lines.append(f"## {section}")
        report_lines.extend(f"- {message}" for message in messages)
        report_lines.append("")
    report_lines.append("## SQLite Load Counts")
    report_lines.extend(f"- {table}: {count} rows" for table, count in counts.items())
    report_lines.append("")
    report_lines.append("## Relationship And Edge-Case Checks")
    report_lines.extend(f"- {result}" for result in verify_database())
    (OUTPUT_DIR / "data_quality_report.txt").write_text("\n".join(report_lines), encoding="utf-8")

    edge_lines = ["Edge Case Verification"]
    edge_lines.extend(verify_database())
    edge_lines.append("empty query results: handled in report_cli.py with a clear message")
    edge_lines.append("invalid CLI arguments: handled by argparse choices and date validation")
    edge_lines.append("invalid database connection: handled in report_cli.py")
    edge_lines.append("zero orders and single customer periods: handled with COALESCE, NULLIF, and empty-table messages")
    (OUTPUT_DIR / "edge_case_report.txt").write_text("\n".join(edge_lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    customers_raw = pd.read_csv(RAW_DIR / "customers.csv")
    products_raw = pd.read_csv(RAW_DIR / "products.csv")
    orders_raw = pd.read_csv(RAW_DIR / "orders.csv")
    order_items_raw = pd.read_csv(RAW_DIR / "order_items.csv")

    customers, customer_issues = clean_customers(customers_raw)
    products, product_issues = clean_products(products_raw)
    orders, order_issues = clean_orders(orders_raw, customers)
    order_items, item_issues = clean_order_items(order_items_raw, orders, products)

    customers.to_csv(CLEAN_DIR / "customers_clean.csv", index=False)
    products.to_csv(CLEAN_DIR / "products_clean.csv", index=False)
    orders.to_csv(CLEAN_DIR / "orders_clean.csv", index=False)
    order_items.to_csv(CLEAN_DIR / "order_items_clean.csv", index=False)

    counts = load_sqlite_database()
    write_reports(
        [
            ("Customers", customer_issues),
            ("Products", product_issues),
            ("Orders", order_issues),
            ("Order Items", item_issues),
        ],
        counts,
    )
    print("Cleaned CSV files written to data/cleaned")
    print(f"SQLite database created at {DB_PATH}")
    print("Reports written to output/sample_reports")


if __name__ == "__main__":
    main()
