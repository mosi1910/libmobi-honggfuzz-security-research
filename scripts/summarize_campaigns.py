#!/usr/bin/env python3
"""Report evidence completeness and recorded crash counts (not unique bugs)."""
import argparse
import csv
from pathlib import Path


def summarize(path):
    with Path(path).open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    complete = [r for r in rows if r['iterations'].strip() not in ('', 'N/A') and r['duration_s'].strip() not in ('', 'N/A')]
    missing = [r['id'] for r in rows if r not in complete]
    print(f'Numbered campaigns: {len(rows)}')
    print(f'Final-summary campaigns: {len(complete)}')
    print(f'Missing/incomplete: {", ".join(missing)}')
    print(f'Recorded crash EVENTS (not unique bugs): {sum(int(r["reported_crashes"] or 0) for r in complete if r["reported_crashes"] not in ("", "N/A"))}')
    print(f'Excluded from controlled comparison: HF-05/HF-06 (persistence), HF-14 (minimization), HF-17 (no coverage)')
    return rows

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('csv_file')
    args=p.parse_args()
    summarize(args.csv_file)
