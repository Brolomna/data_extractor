#!/usr/bin/env python3
"""Extract selected fields from JSON records into a text, CSV, or JSON report."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Iterable

FIELDS = ("nickname", "user_id", "nationality", "head_url")
LABELS = {
    "nickname": "Nickname",
    "user_id": "User ID",
    "nationality": "Nationality",
    "head_url": "Head URL",
}


def find_records(value: Any) -> Iterable[dict[str, Any]]:
    """Yield dictionaries containing all required fields, including nested records."""
    if isinstance(value, dict):
        if all(field in value for field in FIELDS):
            yield value
        for child in value.values():
            yield from find_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from find_records(child)


def format_text(records: list[dict[str, Any]]) -> str:
    """Format records as a readable plain-text report."""
    sections = []
    for record in records:
        sections.append(
            "\\n".join(
                f"{LABELS[field]}: {record[field]}" for field in FIELDS
            )
            + "\\n" + "-" * 40
        )
    return "\\n".join(sections) + ("\\n" if sections else "")


def write_report(records: list[dict[str, Any]], output_path: Path, output_format: str) -> None:
    """Write extracted records in the requested format."""
    if output_format == "json":
        output_path.write_text(
            json.dumps([{field: record[field] for field in FIELDS} for record in records],
                       ensure_ascii=False, indent=2) + "\\n",
            encoding="utf-8",
        )
    elif output_format == "csv":
        with output_path.open("w", encoding="utf-8", newline="") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows({field: record[field] for field in FIELDS} for record in records)
    else:
        output_path.write_text(format_text(records), encoding="utf-8")


def extract_file(input_path: Path, output_path: Path, output_format: str = "txt") -> int:
    """Read JSON, extract complete records, and overwrite the report file."""
    if input_path.resolve() == output_path.resolve():
        raise ValueError("Input and output paths must be different.")

    with input_path.open("r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    records = list(find_records(data))
    write_report(records, output_path, output_format)
    return len(records)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract nickname, user ID, nationality, and head URL from JSON."
    )
    parser.add_argument("input_file", type=Path, help="Path to the source JSON file")
    parser.add_argument("output_file", type=Path, help="Path for the report")
    parser.add_argument(
        "--format", choices=("txt", "csv", "json"), default="txt",
        help="Output format (default: txt)",
    )
    args = parser.parse_args()

    try:
        count = extract_file(args.input_file, args.output_file, args.format)
    except FileNotFoundError as error:
        print(f"Error: file not found: {error.filename}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as error:
        print(
            f"Error: invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}",
            file=sys.stderr,
        )
        return 1
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(f"Extracted {count} record(s) into {args.output_file} ({args.format})")
    if count == 0:
        print("No complete records containing all required fields were found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
