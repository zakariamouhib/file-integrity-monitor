# File Integrity Monitor

Python tool that detects file changes using SHA-256 hashes.

> **Disclaimer:** Educational purposes only. The tool only reads and hashes
> files in the directory you choose. The files in `test_files/` are fake.

## Features

- Computes SHA-256 hashes for every file in a directory (recursively)
- Saves a baseline of the trusted state
- Detects MODIFIED, DELETED and NEW files
- Reads files in chunks (works with large files)
- No external dependencies (standard library only)

## Requirements

- Python 3.8+

## Usage

Create the baseline (trusted state):

    python fim.py baseline

Check for changes:

    python fim.py check

Monitor another directory:

    python fim.py baseline -d my_folder
    python fim.py check -d my_folder

## Options

| Option | Description | Default |
|--------|-------------|---------|
| baseline | Save the current state of the directory | - |
| check | Compare the directory with the baseline | - |
| -d, --dir | Directory to monitor | test_files |

## Example output

    [MODIFIED] test_files\config.txt
    [DELETED]  test_files\notes.txt
    [NEW]      test_files\malware.txt

    Summary: 1 modified, 1 deleted, 1 new.

## How it works

1. `baseline` hashes every file and saves the result in `baseline.json`
2. `check` hashes the files again and compares with the baseline
3. A different hash means the file was modified
4. A path only in the baseline means deleted, only in the scan means new

## What I learned

- Cryptographic hashing with `hashlib` (SHA-256)
- Reading files in chunks and walking directories with `os.walk`
- Storing data as JSON
- Building a CLI with `argparse` and positional arguments
- How tools like Tripwire and AIDE detect tampering

## Limitations

- The baseline is stored locally, so an attacker with access could edit it
- No real-time monitoring: you must run `check` manually
- Only detects content changes, not permissions or timestamps

## Roadmap

- [ ] Ignore list for files and extensions
- [ ] Export the report as JSON or CSV
- [ ] Real-time monitoring
- [ ] Protect the baseline with its own hash

## License

MIT
