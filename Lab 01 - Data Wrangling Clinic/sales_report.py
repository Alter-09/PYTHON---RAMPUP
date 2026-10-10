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
    reader = csv.DictReader(lines)

    for row in reader:
        if not row or not any(v and v.strip() for v in row.values()):
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

def get_top_n_products(
    revenue_map: dict[str, float], n: int = 3
) -> list[tuple[str, float]]:
    """Return the top N products sorted descending by revenue value.
    Args:
        revenue_map: Dictionary mapping product names to their total revenue.
        n: Number of top products to return.

    Returns:
        List of (product, revenue) tuples for the top N products.
    """
    # Fixed sort key to target revenue value (item[4])
    sorted_products = sorted(
        revenue_map.items(),
        key=lambda item: item[1],
        reverse=True
    )
    return sorted_products[:n]


def get_unique_countries(customer_data: list[dict[str, str]]) -> list[str]: 
    """Extract unique countries preserving first-appearance order."""
    seen = set()
    unique_countries = []
    for customer in customer_data:
        country = customer.get("country", "")
        if country and country not in seen:
            seen.add(country)
            unique_countries.append(country)
    return unique_countries


def generate_report(
    output_path: Path,
    region: str,
    top_products: list[tuple[str, float]],
    unique_countries: list[str],
) -> None:
    """Format summary report using f-strings and write via pathlib."""
    
    # Format products list for the report
    formatted_products = "\n".join(
        [f" - {product}: ${revenue:,.2f}" for product, revenue in top_products]
    )
    
    # Format countries list for the report
    formatted_countries = ", ".join(unique_countries)
    
    # Construct the complete report content using raw f-strings (escaped backslashes)
    report_content = (
        f"========================================\n"  # Backslash needs escaping
        f" SALES & CUSTOMER SUMMARY REPORT\n"   # Backslash needs escaping
        f"========================================\n\n"
        f"Target Region Analyzed: {region.title()}\n\n"    # Backslash needs escaping
        f"Top {len(top_products)} Products by Revenue:\n"
        f"{formatted_products}\n\n"
        f"Customer Reach (Countries in Order):\n"
        f" {formatted_countries}\n"
        f"========================================\n"
    )
    
    # Write report to file using pathlib
    output_path.write_text(report_content, encoding="utf-8")


def main() -> None:
    """Execution pipeline utilizing pathlib Path objects."""
    base_dir = Path(__file__).parent if "__file__" in globals() else Path.cwd()
    data_dir = base_dir / "data"
    sales_file = data_dir / "sales.csv"
    customer_file = data_dir / "customers.json"
    report_file = base_dir / "report.txt"
    
    # Pipeline execution
    sales_records = load_sales_data(sales_file)
    customer_records = load_customer_data(customer_file)
    target_region = "north america"
    filtered_sales = filter_sales_by_region(sales_records, target_region)
    revenue_by_product = aggregate_revenue_by_product(filtered_sales)
    top_3_products = get_top_n_products(revenue_by_product, n=3)
    countries = get_unique_countries(customer_records)
    
    generate_report(
        output_path=report_file,
        region=target_region,
        top_products=top_3_products,
        unique_countries=countries,
    )


if __name__ == "__main__":
    main()