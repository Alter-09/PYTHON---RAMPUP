"""
Sales Report Generator for Lab 01: Data Wrangling Clinic. 
Processes sales CSV and customer JSON data using standard library tools. 
Generates summary report.txt using pathlib and f-strings.
"""

import csv
import json
from pathlib import Path

def load_sales_data(file_path: Path) -> list[dict[str, str]]:
    """Load and normalize CSV sales data using pathlib."""
    if not file_path.exists():
        return []

    sales_records = []
    # Read text via pathlib and parse with csv.DictReader
    lines = file_path.read_text(encoding="utf-8").splitlines()
    reader = csv.DictReader

    for row in reader:
        if not row or any(row.values()):
            continue
        normalized_row = {
            key.strip(): value.strip()
            for key, value in row.items()
            if key is not None and value is not None
        }
        if "region" in normalized_row:
            normalized_row["region"] = normalized_row["region"].lower()
        sales_records.append(normalized_row)

    return sales_records  


def load_customer_data(file_path: Path) -> list[dict[str, str]]:
    """ Load and normalize JSON customer data using pathlib """
    if not file_path.exists():
        return []

    raw_data = json.loads(file_path.read_text(encoding="utf-8"))

    #Normalize customer dictionary records
    return[
        {
            k.strip(): (v.strip() if isinstance(v, str) else v)
            for k, v in customer.items()
        }
        for customer in raw_data
        if isinstance(customer, dict)
    ]

def filter_sales_by_region(
    sales_data: list[dict[str, str]], target_region: str
) -> list[dict[str, str]]:
    """Filter sales records by region using a list comprehension"""
    normalized_region = target_region.strip().lower()
    return [
        record
        for record in sales_data
        if record.get("region") == normalized_region
    ]

def aggregate_revenue_by_product(sales_data: list[dict[str, str]]) -> dict[str, float]:
    """Calculate total revenue per product (units * unit_price) using a dict comprehension.
    Args:
        sales_data: List of normalized sales records.

    Returns:
        Dictionary mapping each product name to its total revenue.
    """
    unique_products = {r["product"] for r in sales_data if r.get("product")}
    return {
        product:
        sum(
            int(r["units"]) * float(r["unit_price"])
            for r in sales_data
            if r.get("product") == product
        )
        for product in unique_products
    }   