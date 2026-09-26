import tempfile
import unittest
from datetime import date
from decimal import Decimal
from pathlib import Path

from unlock_lens import read_schedule, summarize


class UnlockLensTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "schedule.csv"

    def test_window_is_inclusive_and_aggregates_categories(self):
        self.path.write_text(
            "date,category,amount\n"
            "2026-10-01,team,1.25\n"
            "2026-10-02,team,2.75\n"
            "2026-10-02,community,3\n"
            "2026-10-03,team,100\n", encoding="utf-8"
        )
        result = summarize(read_schedule(self.path), date(2026, 10, 1), 2)
        self.assertEqual(result["event_count"], 3)
        self.assertEqual(Decimal(result["total"]), Decimal("7"))
        self.assertEqual(result["by_category"], {"community": "3", "team": "4.00"})
        self.assertEqual(result["by_date"], {"2026-10-01": "1.25", "2026-10-02": "5.75"})

    def test_rejects_nonfinite_and_negative_amounts(self):
        for amount in ("NaN", "Infinity", "-1"):
            with self.subTest(amount=amount):
                self.path.write_text(f"date,category,amount\n2026-10-01,team,{amount}\n")
                with self.assertRaisesRegex(ValueError, "finite and nonnegative"):
                    read_schedule(self.path)

    def test_rejects_missing_columns(self):
        self.path.write_text("date,amount\n2026-10-01,1\n")
        with self.assertRaisesRegex(ValueError, "needs date, category, amount"):
            read_schedule(self.path)


if __name__ == "__main__":
    unittest.main()
