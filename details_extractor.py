#!/usr/bin/env python3
"""Extract selected fields from JSON records into a readable text report."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

FIELDS = ("nickname", "user_id", "nationality", "head_url")


def find_records(value: Any):
    """Yield dictionaries containing all required fields, including nested records."""
    if isinstance(value, dict):
        if all(field in value for field in FIELDS):
            yield value
        for child in value.values():
            yield from find_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from find_records(child)


def format_records(records: list[dict[str, Any]]) -> str:
    """Format extracted records as a readable text report."""
    sections = []
    for record in records:
        sections.append(
            "\n".join(
                (
                    f"Nickname: {record['nickname']}",
                    f"User ID: {record['user_id']}",
                    f"Nationality: {record['nationality']}",
                    f"Head URL: {record['head_url']}",
                    "-" * 40,
                )
            )
        )
    return "\n".join(sections) + ("\n" if sections else "")


def extract_file(input_path: Path, output_path: Path) -> int:
    """Read JSON, extract complete records, and overwrite the report file."""
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output paths must be different.")

    with input_path.open("r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    records = list(find_records(data))
    output_path.write_text(format_records(records), encoding="utf-8")
    return len(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract nickname, user ID, nationality, and head URL from JSON."
    )
    parser.add_argument("input_file", type=Path, help="Path to the source JSON file")
    parser.add_argument("output_file", type=Path, help="Path for the text report")
    args = parser.parse_args()

    try:
        count = extract_file(args.input_file, args.output_file)
    except FileNotFoundError as error:
        print(f"Error: file not found: {error.filename}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as error:
        print(
            f"Error: invalid JSON at line {error.lineno}, column {error.colno}: "
            f"{error.msg}",
            file=sys.stderr,
        )
        return 1
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Extracted {count} record(s) into {args.output_file}")
    if count == 0:
        print("No complete records containing all required fields were found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
