import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
import datetime
from main import score

AS_OF = datetime.date(2026, 11, 12)

def row(system, tested, encryption, offsite, verified):
    return {"system": system, "last_restore_test": tested,
            "encryption": encryption, "offsite_copy": offsite,
            "backup_verified": verified}

class TestRestoreReadiness(unittest.TestCase):
    def test_full_score_ready(self):
        r = score([row("SYS-1", "2026-11-01", "yes", "yes", "yes")], AS_OF)
        self.assertEqual((r[0][1], r[0][2]), (100, "READY"))

    def test_old_test_loses_points(self):
        r = score([row("SYS-1", "2026-09-01", "yes", "no", "yes")], AS_OF)
        self.assertEqual((r[0][1], r[0][2]), (60, "AT RISK"))

    def test_nothing_done_is_zero(self):
        r = score([row("SYS-1", "2026-03-01", "no", "no", "no")], AS_OF)
        self.assertEqual((r[0][1], r[0][2]), (0, "NOT READY"))

    def test_30_day_boundary_is_40(self):
        r = score([row("SYS-1", "2026-10-13", "no", "no", "no")], AS_OF)
        self.assertEqual(r[0][1], 40)

    def test_90_day_boundary_is_20(self):
        r = score([row("SYS-1", "2026-08-14", "no", "no", "no")], AS_OF)
        self.assertEqual(r[0][1], 20)

    def test_180_day_boundary_is_10(self):
        r = score([row("SYS-1", "2026-05-16", "no", "no", "no")], AS_OF)
        self.assertEqual(r[0][1], 10)

    def test_80_points_is_ready(self):
        r = score([row("SYS-1", "2026-11-01", "yes", "yes", "no")], AS_OF)
        self.assertEqual((r[0][1], r[0][2]), (80, "READY"))

    def test_50_points_is_at_risk(self):
        r = score([row("SYS-1", "2026-11-01", "yes", "no", "no")], AS_OF)
        self.assertEqual((r[0][1], r[0][2]), (60, "AT RISK"))

    def test_highest_first(self):
        r = score([row("SYS-1", "2026-03-01", "no", "no", "no"),
                   row("SYS-2", "2026-11-01", "yes", "yes", "yes")], AS_OF)
        self.assertEqual(r[0][0], "SYS-2")

    def test_empty_input(self):
        self.assertEqual(score([], AS_OF), [])
