
import time
from datetime import datetime


def start_scheduler(task, interval_minutes):
    if interval_minutes <= 0:
        raise ValueError("Interval must be greater than zero.")

    interval_seconds = interval_minutes * 60

    print("Automatic backup scheduler started.")
    print(f"Backup interval: {interval_minutes} minute(s)")

    while True:
        # Wait before each scheduled backup check
        time.sleep(interval_seconds)

        print(
            f"\nScheduled run: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        try:
            task()
        except Exception as error:
            print(f"Scheduled task failed: {error}")
