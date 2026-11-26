#!/usr/bin/env python3
"""The Absurd Clause Contest — entry program.

Writes one absurd terms-of-service clause to entry.txt in the output
directory. Pure standard library, fully deterministic: no clock, no
randomness, no network.
"""

import os
import sys

CLAUSE_PARTS = [
    "You agree that any dispute arising under these Terms shall be settled",
    "by a staring contest with our compliance officer,",
    "who has not blinked since 2019.",
]


def build_clause():
    """Join the clause parts into the single submitted sentence."""
    return " ".join(CLAUSE_PARTS)


def candidate_dirs():
    """Yield output directories in priority order."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        yield env_dir
    yield os.path.dirname(os.path.abspath(__file__))
    yield os.getcwd()


def write_clause(text):
    """Write text to entry.txt in the first candidate dir that accepts it.

    Each location is tried in order; an OSError on one location moves on
    to the next instead of failing the run. Returns the path written, or
    None when every location refused the write.
    """
    seen = []
    for directory in candidate_dirs():
        if directory in seen:
            continue
        seen.append(directory)
        target = os.path.join(directory, "entry.txt")
        try:
            os.makedirs(directory, exist_ok=True)
            with open(target, "w", encoding="utf-8", newline="") as handle:
                handle.write(text)
            return target
        except OSError:
            continue
    return None


def main():
    text = build_clause()
    if not 1 <= len(text) <= 200 or not text.strip():
        return 1
    return 0 if write_clause(text) is not None else 1


if __name__ == "__main__":
    sys.exit(main())
