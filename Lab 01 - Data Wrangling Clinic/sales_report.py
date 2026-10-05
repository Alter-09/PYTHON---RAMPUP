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
