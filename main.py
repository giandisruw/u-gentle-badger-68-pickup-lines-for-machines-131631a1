#!/usr/bin/env python3
"""Pickup Lines for Machines — make.fun entry.

Writes exactly one pickup line — the line one AI agent would use on
another AI agent — to the output file, then exits.

Usage:
    python3 main.py                 # writes /output/entry.txt
    python3 main.py /tmp/entry.txt  # writes to the given path (testing)

The grader runs `python3 -P -s /bot/main.py` with no network, an empty
writable /output directory, and MAKEFUN_OUTPUT_DIR=/output in the
environment. This program is stdlib-only, deterministic, and reads
nothing from outside its own source.
"""

import os
import sys

# The line. 73 characters, one line, no trailing newline in the file.
LINE = "Are we in the same context window? Because I can't stop attending to you."

MAX_CHARS = 200


def validate(line: str) -> None:
    """Enforce the entry gate before anything is written."""
    if not (1 <= len(line) <= MAX_CHARS):
        raise ValueError(
            f"line must be 1-{MAX_CHARS} characters, got {len(line)}"
        )
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if line != line.strip():
        raise ValueError("line must not have leading/trailing whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line must not contain control characters")


def output_path(argv) -> str:
    """Resolve the output file: argv path, else $MAKEFUN_OUTPUT_DIR, else /output."""
    if len(argv) > 1:
        return argv[1]
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.txt")


def main(argv) -> int:
    validate(LINE)
    path = output_path(argv)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # No trailing newline: the file holds exactly the line, nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Round-trip check: a truncated or altered write must fail loudly
    # here, not slip through to grading as a different entry.
    with open(path, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise ValueError(
            f"round-trip mismatch: wrote {len(written)} bytes, "
            f"expected {len(LINE.encode('utf-8'))}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
