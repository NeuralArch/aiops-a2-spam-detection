import random
import csv

random.seed(42)

NUM_SHARDS = 8
ROWS_PER_SHARD = 50
INVALID_RATE = 0.2

VALID_DOMAINS = ["example.com", "gmail.com", "college.edu"]
NAMES = ["alice", "bob", "carol", "dave", "erin", "frank", "grace", "heidi"]

def make_row(idx, force_invalid):
    name = random.choice(NAMES) + str(idx)
    if force_invalid:
        choice = random.choice(["bad_email", "missing_name"])
        if choice == "bad_email":
            email = f"{name}[at]{random.choice(VALID_DOMAINS)}"
        else:
            email = f"{name}@{random.choice(VALID_DOMAINS)}"
            name = ""
    else:
        email = f"{name}@{random.choice(VALID_DOMAINS)}"
    return [name, email]

def generate_shard(shard_index):
    filename = f"shard_{shard_index}.csv"
    rows = []
    for i in range(ROWS_PER_SHARD):
        force_invalid = random.random() < INVALID_RATE
        rows.append(make_row(f"{shard_index}_{i}", force_invalid))
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "email"])
        writer.writerows(rows)
    print(f"Generated {filename} with {ROWS_PER_SHARD} rows")

if __name__ == "__main__":
    for i in range(NUM_SHARDS):
        generate_shard(i)