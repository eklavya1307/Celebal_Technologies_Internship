from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

try:
    from tabulate import tabulate
except ImportError:
    tabulate = None


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "ecommerce.db"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="E-Commerce Order Analytics CLI")
    parser.add_argument("--report", choices=["revenue", "top_customers", "retention"], required=True)
    parser.add_argument("--start-date", help="Optional start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", help="Optional end date in YYYY-MM-DD format")
    parser.add_argument("--limit", type=int, default=10, help="Number of rows for ranked reports")
    parser.add_argument("--db", default=str(DB_PATH), help="SQLite database path")
    return parser.parse_args()


def parse_date(value: str | None, label: str) -> str | None:
    if value is None:
        return None
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise SystemExit(f"Invalid {label}: {value}. Use YYYY-MM-DD.") from exc
    if parsed.date() > datetime.now().date():
        raise SystemExit(f"Invalid {label}: future dates are not allowed.")
    return value


def connect(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)
    if not path.exists():
        raise SystemExit(f"Database not found: {path}. Run python scripts/clean_data.py first.")
    try:
        connection = sqlite3.connect(path)
        connection.execute("SELECT 1 FROM orders LIMIT 1")
        return connection
    except sqlite3.Error as exc:
        raise SystemExit(f"Could not open a valid SQLite analytics database: {exc}") from exc


def render_table(headers: list[str], rows: list[tuple]) -> str:
    if not rows:
        return "No results found for the selected filters."
    if tabulate is not None:
        return tabulate(rows, headers=headers, tablefmt="grid")

    values = [headers] + [[str(value) for value in row] for row in rows]
    widths = [max(len(row[index]) for row in values) for index in range(len(headers))]
    line = "+-" + "-+-".join("-" * width for width in widths) + "-+"
    output = [line, "| " + " | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))) + " |", line]
    for row in rows:
        output.append("| " + " | ".join(str(row[i]).ljust(widths[i]) for i in range(len(headers))) + " |")
    output.append(line)
    return "\n".join(output)


def date_filter(alias: str, start_date: str | None, end_date: str | None) -> tuple[str, list[str]]:
    filters: list[str] = []
    params: list[str] = []
    if start_date:
        filters.append(f"date({alias}.order_date) >= date(?)")
        params.append(start_date)
    if end_date:
        filters.append(f"date({alias}.order_date) <= date(?)")
        params.append(end_date)
    return (" WHERE " + " AND ".join(filters)) if filters else "", params


def revenue_report(connection: sqlite3.Connection, start_date: str | None, end_date: str | None) -> str:
    where_sql, params = date_filter("o", start_date, end_date)
    query = f"""
        SELECT
            strftime('%Y-%m', o.order_date) AS month,
            COUNT(DISTINCT o.order_id) AS total_orders,
            COUNT(DISTINCT NULLIF(o.customer_id, 0)) AS unique_customers,
            ROUND(COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0), 2) AS revenue,
            ROUND(COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS average_order_value
        FROM orders o
        LEFT JOIN order_items oi ON o.order_id = oi.order_id
        {where_sql}
        GROUP BY strftime('%Y-%m', o.order_date)
        ORDER BY month;
    """
    rows = connection.execute(query, params).fetchall()
    return "Revenue Report\n" + render_table(["Month", "Orders", "Customers", "Revenue", "AOV"], rows)


def top_customers_report(connection: sqlite3.Connection, start_date: str | None, end_date: str | None, limit: int) -> str:
    where_sql, params = date_filter("o", start_date, end_date)
    query = f"""
        SELECT
            c.customer_id,
            c.customer_name,
            c.customer_type,
            COUNT(DISTINCT o.order_id) AS order_count,
            ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS total_revenue
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        {where_sql}
        GROUP BY c.customer_id, c.customer_name, c.customer_type
        ORDER BY total_revenue DESC
        LIMIT ?;
    """
    rows = connection.execute(query, [*params, max(limit, 1)]).fetchall()
    return "Top Customers Report\n" + render_table(["ID", "Customer", "Type", "Orders", "Revenue"], rows)


def retention_report(connection: sqlite3.Connection) -> str:
    query = """
        WITH order_months AS (
            SELECT DISTINCT
                c.customer_id,
                date(c.registration_date, 'start of month') AS cohort_month,
                date(o.order_date, 'start of month') AS activity_month
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            WHERE c.customer_id <> 0
        ),
        cohort_activity AS (
            SELECT
                customer_id,
                strftime('%Y-%m', cohort_month) AS cohort,
                ((CAST(strftime('%Y', activity_month) AS INTEGER) - CAST(strftime('%Y', cohort_month) AS INTEGER)) * 12)
                    + (CAST(strftime('%m', activity_month) AS INTEGER) - CAST(strftime('%m', cohort_month) AS INTEGER)) AS month_number
            FROM order_months
        ),
        retention AS (
            SELECT
                cohort,
                COUNT(DISTINCT CASE WHEN month_number = 0 THEN customer_id END) AS month_0,
                COUNT(DISTINCT CASE WHEN month_number = 1 THEN customer_id END) AS month_1,
                COUNT(DISTINCT CASE WHEN month_number = 2 THEN customer_id END) AS month_2,
                COUNT(DISTINCT CASE WHEN month_number = 3 THEN customer_id END) AS month_3
            FROM cohort_activity
            WHERE month_number BETWEEN 0 AND 3
            GROUP BY cohort
        )
        SELECT
            cohort,
            month_0,
            month_1,
            month_2,
            month_3,
            ROUND(100.0 * month_1 / NULLIF(month_0, 0), 2) AS month_1_retention_percent,
            ROUND(100.0 * month_2 / NULLIF(month_0, 0), 2) AS month_2_retention_percent,
            ROUND(100.0 * month_3 / NULLIF(month_0, 0), 2) AS month_3_retention_percent
        FROM retention
        ORDER BY cohort;
    """
    rows = connection.execute(query).fetchall()
    return "Retention Report\n" + render_table(
        ["Cohort", "M0", "M1", "M2", "M3", "M1 Ret %", "M2 Ret %", "M3 Ret %"],
        rows,
    )


def run_report(report: str, db_path: str, start_date: str | None = None, end_date: str | None = None, limit: int = 10) -> str:
    start_date = parse_date(start_date, "start-date")
    end_date = parse_date(end_date, "end-date")
    if start_date and end_date and start_date > end_date:
        raise SystemExit("start-date must be before or equal to end-date.")

    connection = connect(db_path)
    with connection:
        if report == "revenue":
            return revenue_report(connection, start_date, end_date)
        if report == "top_customers":
            return top_customers_report(connection, start_date, end_date, limit)
        if report == "retention":
            return retention_report(connection)
    raise SystemExit(f"Unsupported report: {report}")


def main() -> None:
    args = parse_args()
    print(run_report(args.report, args.db, args.start_date, args.end_date, args.limit))


if __name__ == "__main__":
    main()
