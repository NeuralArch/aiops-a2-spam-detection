import os
import csv
import re
import sys

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def is_valid_row(row):
    name = row.get("name", "").strip()
    email = row.get("email", "").strip()
    if not name:
        return False
    if not EMAIL_REGEX.match(email):
        return False
    return True

def main():
    index = os.environ.get("JOB_COMPLETION_INDEX")
    if index is None:
        print("ERROR: JOB_COMPLETION_INDEX not set", file=sys.stderr)
        sys.exit(1)

    shard_path = f"/data/shard_{index}.csv"
    node_name = os.environ.get("NODE_NAME", "unknown")
    pod_name = os.environ.get("POD_NAME", "unknown")

    total_rows = 0
    invalid_rows = 0

    with open(shard_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            if not is_valid_row(row):
                invalid_rows += 1

    print(f"SHARD_INDEX={index} POD={pod_name} NODE={node_name} "
          f"TOTAL_ROWS={total_rows} INVALID_ROWS={invalid_rows}")

if __name__ == "__main__":
    main()