"""Main entry point for log analysis pipeline."""

from collections import Counter
from pathlib import Path
from log_pipeline import iter_log_lines, parse_logs, timed
from generate_logs import generate_synthetic_logs

@timed
def run_pipeline(log_path: Path) -> None:
    # 1. Pipeline de lectura e interpretación (Lazy)
    raw_lines = iter_log_lines(log_path)
    entries = parse_logs(raw_lines)

    # 2. Expresión generadora para filtrar errores (Lazy)
    error_entries = (entry for entry in entries if entry.level == "ERROR")

    # 3. Conteo de errores comunes
    error_counts = Counter(entry.message for entry in error_entries)

    print("\n========================================")
    print(" LOG PIPELINE ANALYSIS REPORT ")
    print("========================================")
    print(f"Top 5 Most Frequent Error Messages:\n")
    for message, count in error_counts.most_common(5):
        print(f" [{count} occurrences]: {message}")
    print("========================================\n")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    log_file = base_dir / "logs.log"
    
    if not log_file.exists():
        print("Generating synthetic logs...")
        generate_synthetic_logs(log_file, line_count=100_000)
        print("Log file generated successfully.\n")
    
    print(f"Running log analysis pipeline for {log_file}:\n")
    run_pipeline(log_file)