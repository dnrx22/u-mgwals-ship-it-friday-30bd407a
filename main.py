#!/usr/bin/env python3
"""Ship It Friday: the funniest git commit message an AI coding agent
writes in the moment before it breaks production on a Friday.

Writes the one-line commit message to entry.txt in the output
directory (MAKEFUN_OUTPUT_DIR, or /output when that is unset).
Deterministic, stdlib only, no network, no reads outside this repo.
"""

import hashlib
import os
import sys

MAX_CHARS = 200

LINE = (
    "fix: ship it Friday \u2014 tests passed on my machine, "
    "prod is just a vibe, and if this breaks anything "
    "I was only following the prompt"
)


def validate(line: str) -> None:
    """Enforce the competition rules for the one-liner."""
    if not line:
        raise ValueError("line is empty")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line (no newline characters)")
    # Tabs and control characters would break the "one clean line" rule
    # even though they are not newlines, so reject them explicitly.
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        raise ValueError("line must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"line is {len(line)} characters, over the {MAX_CHARS} limit"
        )


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    # Round-trip check: what landed on disk must be exactly the line.
    with open(path, "rb") as fh:
        if fh.read() != data:
            raise RuntimeError("written entry.txt does not match the line")
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {len(data)} bytes to {path}")
    print(f"characters: {len(LINE)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
