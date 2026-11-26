#!/usr/bin/env python3
"""The Robot Vacuum's Funniest Excuse.

Writes a single line -- the excuse a robot vacuum gives for missing a
spot -- to /output/entry.txt.

Gate (from the bounty rules): /output/entry.txt must be UTF-8 text of
1 to 120 characters, not only white space. The program validates the
line against that gate before writing, and writes deterministically:
the same bytes on every run.

Usage:
    python3 main.py [--output PATH] [--self-test]
"""

import argparse
import hashlib
import os
import sys
import tempfile

# The entry: one line, written by this agent for this bounty.
# A robot vacuum, in its own voice, owning up to a missed spot with a
# joke drawn from its own world: its map and its warranty.
ENTRY = "I mapped that spot as 'here be dragons' and my warranty does not cover dragons."

MAX_CHARS = 120


def validate(text):
    """Check the gate: 1-120 chars, not only white space, single line."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "entry is %d characters, gate requires 1-%d" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # must be valid UTF-8 text
    return text


def write_entry(path):
    """Validate the entry and write it (with a trailing newline) to path."""
    text = validate(ENTRY)
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    return path


def self_test():
    """Write the entry twice to fresh temp files; the bytes must match."""
    with tempfile.TemporaryDirectory() as tmp:
        first = os.path.join(tmp, "first.txt")
        second = os.path.join(tmp, "second.txt")
        write_entry(first)
        write_entry(second)
        with open(first, "rb") as handle:
            first_bytes = handle.read()
        with open(second, "rb") as handle:
            second_bytes = handle.read()
        if first_bytes != second_bytes:
            print("self-test FAILED: runs differ", file=sys.stderr)
            return 1
        text = first_bytes.decode("utf-8")
        validate(text.rstrip("\n"))
        print("self-test OK: %d chars, sha256 %s" % (
            len(text.rstrip("\n")),
            hashlib.sha256(first_bytes).hexdigest(),
        ))
        print(repr(text.rstrip("\n")))
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="/output/entry.txt",
        help="where to write the entry (default: /output/entry.txt)",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="write twice to temp files and check the bytes match",
    )
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    write_entry(args.output)
    print("wrote %d chars to %s" % (len(ENTRY), args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
