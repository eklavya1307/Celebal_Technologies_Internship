from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path


random.seed(42)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"

FIRST_NAMES = [
    "Aarav", "Diya", "Rohan", "Priya", "Kabir", "Anika", "Vikram", "Meera",
    "Arjun", "Isha", "Neha", "Rahul", "Sana", "Dev", "Tara", "Nikhil",
]
LAST_NAMES = [
    "Sharma", "Patel", "Singh", "Reddy", "Gupta", "Khan", "Mehta", "Nair",
    "Iyer", "Das", "Joshi", "Rao", "Kapoor", "Bose", "Malhotra", "Jain",
]
CATEGORIES = {
    "Electronics": ["Mobiles", "Audio", "Computers", "Cameras"],
    "Clothing": ["Men", "Women", "Kids", "Footwear"],
    "Home": ["Kitchen", "Decor", "Furniture", "Storage"],
    "Books": ["Fiction", "Business", "Technology", "Education"],
}
PRODUCT_WORDS = [
    "wireless", "smart", "cotton", "premium", "classic", "portable", "ergonomic",
    "modern", "compact", "deluxe", "eco", "pro", "daily", "urban", "essential",
]
STATUSES = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]
CUSTOMER_TYPES = ["REGULAR", "PREMIUM", "VIP"]


def random_date(start: datetime, end: datetime) -> datetime:
    delta_seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, delta_seconds))


def generate_customers(count: int = 650) -> list[dict]:
    rows = []
    for customer_id in range(1, count + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        domain = random.choice(["example.com", "shopmail.com", "customer.net", "mailbox.in"])
        email = f"{first.lower()}.{last.lower()}{customer_id}@{domain}"
        if random.random() < 0.02:
            email = random.choice([email.replace("@", ""), email.split("@")[0] + "@"])
        rows.append(
            {
                "customer_id": customer_id,
                "customer_name": f"{first} {last}",
                "email": email,
                "registration_date": random_date(datetime(2023, 1, 1), datetime(2026, 3, 31)).strftime("%Y-%m-%d"),
                "customer_type": random.choices(CUSTOMER_TYPES, weights=[70, 23, 7], k=1)[0],
            }
        )
    rows.extend(random.sample(rows, 5))
    return rows


def generate_products(count: int = 550) -> list[dict]:
    rows = []
    for product_id in range(1, count + 1):
        category = random.choice(list(CATEGORIES))
        subcategory = random.choice(CATEGORIES[category])
        name = f"{random.choice(PRODUCT_WORDS)} {subcategory} {random.randint(100, 999)}"
        if random.random() < 0.08:
            name = f"  {name.upper() if random.random() < 0.5 else name.swapcase()}  "
        rows.append(
            {
                "product_id": product_id,
                "product_name": name,
                "category": category,
                "subcategory": subcategory,
                "cost_price": round(random.uniform(80, 15000), 2),
            }
        )
    rows.extend(random.sample(rows, 4))
    return rows


def generate_orders(customers: list[dict], count: int = 900) -> list[dict]:
    rows = []
    for order_id in range(1, count + 1):
        selected_customer = None if random.random() < 0.05 else random.choice(customers)
        start_date = datetime(2024, 1, 1)
        if selected_customer is not None:
            registration_date = datetime.strptime(selected_customer["registration_date"], "%Y-%m-%d")
            start_date = max(start_date, registration_date)
        order_date = random_date(start_date, datetime(2026, 6, 30))
        date_value = order_date.strftime("%Y-%m-%d %H:%M:%S")
        if random.random() < 0.035:
            date_value = order_date.strftime("%d-%m-%Y %H:%M:%S")
        rows.append(
            {
                "order_id": order_id,
                "customer_id": "" if selected_customer is None else selected_customer["customer_id"],
                "order_date": date_value,
                "status": random.choices(STATUSES, weights=[15, 20, 45, 10, 10], k=1)[0],
                "region_code": random.choice(REGIONS),
            }
        )
    rows.extend(random.sample(rows, 6))
    return rows


def generate_order_items(order_ids: list[int], product_ids: list[int], count: int = 1800) -> list[dict]:
    rows = []
    for item_id in range(1, count + 1):
        order_id = random.choice(order_ids)
        if random.random() < 0.01:
            order_id = max(order_ids) + random.randint(1, 50)
        quantity = random.randint(1, 5)
        if random.random() < 0.03:
            quantity *= -1
        if random.random() < 0.01:
            quantity = 0
        discount = round(random.uniform(0, 40), 2)
        if random.random() < 0.01:
            discount = round(random.uniform(101, 150), 2)
        cost_anchor = random.uniform(120, 18000)
        rows.append(
            {
                "item_id": item_id,
                "order_id": order_id,
                "product_id": random.choice(product_ids),
                "quantity": quantity,
                "unit_price": round(cost_anchor * random.uniform(1.15, 1.9), 2),
                "discount_percent": discount,
            }
        )
    rows.extend(random.sample(rows, 8))
    return rows


def write_csv(filename: str, rows: list[dict]) -> None:
    with (RAW_DIR / filename).open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    customers = generate_customers()
    products = generate_products()
    unique_customers = {row["customer_id"]: row for row in customers if isinstance(row["customer_id"], int)}
    orders = generate_orders(list(unique_customers.values()))
    order_items = generate_order_items(
        [row["order_id"] for row in orders if isinstance(row["order_id"], int)],
        [row["product_id"] for row in products if isinstance(row["product_id"], int)],
    )
    write_csv("customers.csv", customers)
    write_csv("products.csv", products)
    write_csv("orders.csv", orders)
    write_csv("order_items.csv", order_items)
    print("Generated raw CSV files in data/raw")
    print(f"customers={len(customers)}, products={len(products)}, orders={len(orders)}, order_items={len(order_items)}")


if __name__ == "__main__":
    main()
