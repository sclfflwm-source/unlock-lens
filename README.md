# Unlock Lens

Unlock Lens is a small, offline CLI for checking a token unlock schedule you supply. It reads a CSV and reports the token amount scheduled for an inclusive date window, grouped by date and category. It does not fetch or verify project schedules.

## Run

```sh
python3 unlock_lens.py example_schedule.csv --from 2026-10-01 --days 30
```

The input needs `date`, `category`, and `amount` columns. Dates use `YYYY-MM-DD`. Amounts are token quantities, not prices or dollar values. All dates are treated as calendar dates; there is no timezone conversion. The output is JSON, suitable for other scripts.

The tool uses Python's `Decimal` for exact decimal arithmetic. It rejects negative or non-finite amounts and exits with code 2 for invalid input. Zero is allowed. A successful run exits with code 0.

## Tests

```sh
python3 -m unittest -v
```

This is schedule arithmetic only. Confirm source data and vesting terms with the project before using the results in any financial decision.

## License

MIT; see [LICENSE](LICENSE).
