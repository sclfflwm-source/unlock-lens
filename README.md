# Unlock Lens

**Turn a token vesting CSV into a clear unlock timeline.** Unlock Lens is an offline, dependency-free Python CLI. It groups scheduled token amounts by date and category for an inclusive window you choose. It uses exact decimal arithmetic and prints JSON for scripts or dashboards.

## Quick start

```sh
python3 unlock_lens.py example_schedule.csv --from 2026-10-01 --days 30
```

Example result:

```json
{
  "from": "2026-10-01",
  "through": "2026-10-30",
  "event_count": 2,
  "total": "150000",
  "by_category": {"community": "100000", "team": "50000"},
  "by_date": {"2026-10-01": "100000", "2026-10-08": "50000"}
}
```

## Input format

The CSV needs `date`, `category`, and `amount` columns:

```csv
date,category,amount
2026-10-01,community,100000
2026-10-08,team,50000
```

Dates use `YYYY-MM-DD`. Amounts are **token quantities**, not prices or dollar values. The `--from` date is included; `--days 30` covers 30 calendar dates, including that first date. No timezone conversion is performed. The default start date is the local machine's current date.

The tool rejects invalid dates, empty categories, and negative or non-finite amounts. Zero is allowed. It exits with code `0` on success and `2` for invalid input.

## Tests

```sh
python3 -m unittest -v
```

The GitHub Actions workflow runs these tests on pushes and pull requests.

## Scope and limits

This is schedule arithmetic only. It does not fetch or verify project schedules, model cliffs or vesting rules from contracts, value tokens in currency, or predict circulating supply. Confirm source data and vesting terms with the project before relying on a result.

## License

MIT; see [LICENSE](LICENSE).
