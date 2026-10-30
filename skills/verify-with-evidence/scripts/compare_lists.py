#!/usr/bin/env python3
"""Read-only comparison of manually observed visible IDs and exported CSV IDs."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
import sys


def duplicates(values: list[str]) -> list[str]:
    return sorted(value for value, count in Counter(values).items() if count > 1)


def compare(visible_path: Path, csv_path: Path, id_column: str) -> dict:
    visible = json.loads(visible_path.read_text(encoding="utf-8-sig"))
    if not isinstance(visible, list) or any(
        not isinstance(value, str) or not value.strip() for value in visible
    ):
        raise ValueError("visible IDs must be a JSON array of nonempty strings")

    with csv_path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames or []
        if len(fields) != len(set(fields)):
            raise ValueError("CSV has duplicate column names")
        if id_column not in fields:
            raise ValueError("CSV is missing the requested ID column")
        exported = []
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("CSV row width does not match its header")
            value = row[id_column]
            if not value or not value.strip():
                raise ValueError("CSV has an empty ID")
            exported.append(value)

    missing = sorted(set(visible) - set(exported))
    unexpected = sorted(set(exported) - set(visible))
    visible_duplicates = duplicates(visible)
    csv_duplicates = duplicates(exported)
    same_order = visible == exported
    passed = (
        same_order and not visible_duplicates and not csv_duplicates
    )
    return {
        "result": "PASS" if passed else "MISMATCH",
        "visible_count": len(visible),
        "csv_count": len(exported),
        "missing_in_csv": missing,
        "unexpected_in_csv": unexpected,
        "duplicate_visible_ids": visible_duplicates,
        "duplicate_csv_ids": csv_duplicates,
        "same_order": same_order,
        "scope": "IDs, row count, duplicates and ordering only",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--visible-ids", type=Path, required=True)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--id-column", required=True)
    args = parser.parse_args()
    try:
        report = compare(args.visible_ids, args.csv, args.id_column)
    except (OSError, ValueError, csv.Error, UnicodeError) as exc:
        print(json.dumps({"result": "INPUT_ERROR", "error": str(exc)}, ensure_ascii=True))
        return 2
    print(json.dumps(report, ensure_ascii=True, indent=2))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
