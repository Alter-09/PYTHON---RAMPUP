@timer
def run_cli_pipeline(log_path: Path) -> int:
    """Función de demostración CLI del paquete log_pipeline_revamp."""
    lines = stream_log_lines(log_path)
    entries = parse_log_entries(lines)
    errors = filter_by_level(entries, "ERROR")

    count = 0
    for err in errors:
        count += 1
        print(f"  X [{err.timestamp}] [{err.service}] -> {err.message}")

    return count

