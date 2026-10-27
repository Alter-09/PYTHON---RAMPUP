"""Script to generate ralistic synthetic log files"""

import random
from datetime import datetime, timedelta
from pathlib import Path

LOG_LEVELS = ["INFO", "INFO", "INFO", "WARNING", "ERROR"]
ERROR_MESSAGES = [
    "DatabaseConnectionTimeout: Failed to connect to host 10.0.0.5",
    "HTTP500InternalServerError: Service payment-gateway unreachable",
    "MemoryLimitExceeded: Process used 98% of allocated RAM",
    "InvalidAuthToken: Signature verification failed for user_id=402",
    "FileNotFoundError: Missing configuration template at /etc/app.json",
]
INFO_MESSAGES = [
    "User logged in successfully",
    "Background sync completed",
    "Cache purged for session_id=892",
    "Metrics pushed to Prometheus",
]

def generate_synthetic_logs(file_path: Path, line_count: int = 100_000) -> None:
    """Generate a synthetic log file line by line using pathlib."""
    start_time = datetime.now() - timedelta(days=1)
    with file_path.open(mode="w", encoding="utf-8") as file:
        for i in range(line_count):
            timestamp = (start_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")
            level = random.choice(LOG_LEVELS)
            if level == "ERROR":
                msg = random.choice(ERROR_MESSAGES)
            else:
                msg = random.choice(INFO_MESSAGES)
            file.write(f"{timestamp} - {level} - {msg}\n")
            
if __name__ == "__main__":
    output_log = Path("logs.log")
    print(f"Generating 100,000 log entries into '{output_log}'...")
    generate_synthetic_logs(output_log, line_count=100_000)
    print("Done!")