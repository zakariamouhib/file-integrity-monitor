import argparse
import hashlib
import json
import os

BASELINE_FILE = "baseline.json"


def hash_file(path):
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def scan_directory(directory):
    hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            hashes[path] = hash_file(path)
    return hashes


def create_baseline(directory):
    hashes = scan_directory(directory)
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(hashes, f, indent=2)
    print(f"Baseline created for {len(hashes)} files.")


def check_integrity(directory):
    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            baseline = json.load(f)
    except FileNotFoundError:
        print("Error: no baseline found. Run with 'baseline' first.")
        return

    current = scan_directory(directory)

    modified = [p for p in current if p in baseline and current[p] != baseline[p]]
    deleted = [p for p in baseline if p not in current]
    new = [p for p in current if p not in baseline]

    for p in sorted(modified):
        print(f"[MODIFIED] {p}")
    for p in sorted(deleted):
        print(f"[DELETED]  {p}")
    for p in sorted(new):
        print(f"[NEW]      {p}")

    if not (modified or deleted or new):
        print("OK: no changes detected.")
    else:
        print(f"\nSummary: {len(modified)} modified, "
              f"{len(deleted)} deleted, {len(new)} new.")


def main():
    parser = argparse.ArgumentParser(
        description="Detect file changes using SHA-256 hashes (educational use only)"
    )
    parser.add_argument("mode", choices=["baseline", "check"],
                        help="baseline = save current state, check = compare with baseline")
    parser.add_argument("-d", "--dir", default="test_files",
                        help="Directory to monitor (default: test_files)")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Error: directory '{args.dir}' not found.")
        return

    if args.mode == "baseline":
        create_baseline(args.dir)
    else:
        check_integrity(args.dir)


if __name__ == "__main__":
    main()