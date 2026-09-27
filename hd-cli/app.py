import csv
import math
from pathlib import Path

DATA_DIR = Path("/data")
INPUT_FILE = DATA_DIR / "tasks.csv"
OUTPUT_FILE = DATA_DIR / "summary.txt"
DAILY_TARGET = 3


def main():
    with INPUT_FILE.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != ["task", "status"]:
            raise ValueError("CSV columns must be: task,status")
        tasks = list(reader)

    if not tasks:
        raise ValueError("The CSV file must contain at least one task.")

    for row in tasks:
        if not row["task"].strip() or row["status"].strip().lower() not in {"complete", "pending"}:
            raise ValueError("Each task needs a name and a complete or pending status.")

    total = len(tasks)
    completed = sum(row["status"].strip().lower() == "complete" for row in tasks)
    remaining = total - completed
    percentage = completed / total * 100
    days = math.ceil(remaining / DAILY_TARGET)

    summary = (
        "Milestone Progress Summary\n"
        f"Total tasks: {total}\n"
        f"Completed tasks: {completed}\n"
        f"Remaining tasks: {remaining}\n"
        f"Completion: {percentage:.1f}%\n"
        f"Estimated days at {DAILY_TARGET} tasks per day: {days}\n"
    )

    OUTPUT_FILE.write_text(summary, encoding="utf-8")
    print(f"Processed {INPUT_FILE}")
    print(summary)
    print(f"Saved {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
