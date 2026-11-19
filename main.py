"""Score backup restore readiness per system, 0-100.

Usage: python3 main.py systems.csv [--as-of 2026-11-12]
CSV columns: system,last_restore_test,encryption,offsite_copy,backup_verified.
Points: last restore test within 30 days +40, within 90 days
+20, within 180 days +10, older +0; encryption yes +20;
offsite copy yes +20; backup verified yes +20.
- READY: 80 points or more.
- AT RISK: 50-79 points.
- NOT READY: under 50 points.
Highest score first.
"""
import argparse, csv, sys
from datetime import date

def score(rows, as_of=None):
    as_of = as_of or date.today()
    out = []
    for row in rows:
        tested = date.fromisoformat(row["last_restore_test"].strip())
        days = (as_of - tested).days
        if days <= 30:
            points = 40
        elif days <= 90:
            points = 20
        elif days <= 180:
            points = 10
        else:
            points = 0
        encrypted = row["encryption"].strip().lower() in ("yes", "y", "true", "1")
        offsite = row["offsite_copy"].strip().lower() in ("yes", "y", "true", "1")
        verified = row["backup_verified"].strip().lower() in ("yes", "y", "true", "1")
        points += 20 if encrypted else 0
        points += 20 if offsite else 0
        points += 20 if verified else 0
        if points >= 80:
            band = "READY"
        elif points >= 50:
            band = "AT RISK"
        else:
            band = "NOT READY"
        out.append((row["system"].strip(), points, band, days,
                    "yes" if encrypted else "no",
                    "yes" if offsite else "no",
                    "yes" if verified else "no"))
    return sorted(out, key=lambda r: (-r[1], r[0]))

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--as-of", default=None, help="reference date YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    with open(args.path, newline="", encoding="utf-8") as f:
        results = score(list(csv.DictReader(f)), as_of)
    for system, points, band, days, encrypted, offsite, verified in results:
        print(f"{system}: {band} (score {points}: test {days} day(s) ago, "
              f"encryption {encrypted}, offsite copy {offsite}, verified {verified})")
    print(f"{sum(1 for *_, b, _, _, _, _ in results if b == 'READY')} ready, "
          f"{sum(1 for *_, b, _, _, _, _ in results if b == 'AT RISK')} at risk, "
          f"{sum(1 for *_, b, _, _, _, _ in results if b == 'NOT READY')} not ready.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
