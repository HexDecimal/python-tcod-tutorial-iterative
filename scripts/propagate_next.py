"""Propagate current commits to the next part of the tutorial relative to the current branch.

If current branch is 'foo/03' this will switch/merge to 'foo/04'.
"""

from __future__ import annotations

import argparse
from subprocess import PIPE, run

# ruff: noqa: INP001, S607

parser = argparse.ArgumentParser(description=__doc__)


def main() -> None:
    """Switch and merge to the next branch."""
    _args = parser.parse_args()

    current_branch = run(
        ("git", "rev-parse", "--abbrev-ref", "HEAD"), stdout=PIPE, check=True, text=True
    ).stdout.strip()
    year, part = current_branch.split("/")
    next_branch = f"{year}/{int(part) + 1:02d}"
    run(("git", "switch", next_branch), check=True)  # noqa: S603
    run(("git", "merge", current_branch), check=True)  # noqa: S603


if __name__ == "__main__":
    main()
