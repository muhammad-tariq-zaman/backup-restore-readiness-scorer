# backup-restore-readiness-scorer

Score backup restore readiness per system, 0–100: last restore test within 30 days +40, within 90 days +20, within 180 days +10, older +0; encryption yes +20; offsite copy yes +20; backup verified yes +20 — READY at 80+, AT RISK at 50–79, NOT READY under 50, highest score first.

Sample input is included (sample.csv with three systems).

## How to run

```sh
python3 main.py sample.csv --as-of 2026-11-12
```

## Example output

```
SYS-1: READY (score 100: test 11 day(s) ago, encryption yes, offsite copy yes, verified yes)
SYS-2: AT RISK (score 60: test 72 day(s) ago, encryption yes, offsite copy no, verified yes)
SYS-3: NOT READY (score 0: test 256 day(s) ago, encryption no, offsite copy no, verified no)
1 ready, 1 at risk, 1 not ready.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
