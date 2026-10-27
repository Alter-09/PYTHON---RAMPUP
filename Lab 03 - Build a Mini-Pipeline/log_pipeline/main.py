from pathlib import Path
from collections import Counter
from log_pipeline.reader import iter_logs_lines
from log_pipeline.reader import timed

@timed
def process_pipeline(log_path: Path) -> None:
    # 1. Line by line stream
    raw_lines = iter_logs_lines(log_path)

    # 2. Error filtering generator expression (Lazy mode)
    error_mssgs = (
        line.split(" - ", 2)[-1]
        for line in raw_lines
        if "Error" in line
    )

    # 3. Efficient counting of top 5 errors using Counter
    top_errors = Counter(error_mssgs).most_common(5)

    print("\n--- Top 5 Errores ---")
    for msg, count in top_errors:
        print(f"[{count} veces]: {msg}")

if __name__ == "__main__":
    process_pipeline(Path("logs.log"))