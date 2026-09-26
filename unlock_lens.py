#!/usr/bin/env python3
"""Summarize a user-supplied token unlock schedule without network access."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path


def read_schedule(path: Path) -> list[dict[str, object]]:
    try:
        with path.open(newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            required = {"date", "category", "amount"}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError("CSV needs date, category, amount columns")
            events = []
            for line, row in enumerate(reader, start=2):
                try:
                    event_date = date.fromisoformat(row["date"].strip())
                    category = row["category"].strip()
                    amount = Decimal(row["amount"].strip())
                except (ValueError, InvalidOperation, AttributeError) as exc:
                    raise ValueError(f"line {line}: invalid date or amount") from exc
                if not category:
                    raise ValueError(f"line {line}: category is empty")
                if not amount.is_finite() or amount < 0:
                    raise ValueError(f"line {line}: amount must be finite and nonnegative")
                events.append({"date": event_date, "category": category, "amount": amount})
            return events
    except OSError as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc


def summarize(events: list[dict[str, object]], start: date, days: int) -> dict[str, object]:
    if days < 1:
        raise ValueError("days must be positive")
    end = start + timedelta(days=days - 1)
    selected = [event for event in events if start <= event["date"] <= end]
    by_category: dict[str, Decimal] = defaultdict(Decimal)
    by_date: dict[str, Decimal] = defaultdict(Decimal)
    for event in selected:
        by_category[event["category"]] += event["amount"]
        by_date[event["date"].isoformat()] += event["amount"]
    return {
        "from": start.isoformat(),
        "through": end.isoformat(),
        "event_count": len(selected),
        "total": str(sum(by_category.values(), Decimal(0))),
        "by_category": {key: str(by_category[key]) for key in sorted(by_category)},
        "by_date": {key: str(by_date[key]) for key in sorted(by_date)},
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schedule", type=Path, help="CSV with date,category,amount columns")
    parser.add_argument("--from", dest="start", default=date.today().isoformat(),
                        help="first date, YYYY-MM-DD (default: today)")
    parser.add_argument("--days", type=int, default=30, help="inclusive window length")
    args = parser.parse_args(argv)
    try:
        start = date.fromisoformat(args.start)
        result = summarize(read_schedule(args.schedule), start, args.days)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
