#!/usr/bin/env python3
"""Compare sets of actually-covered LCOV line/branch/function identifiers.

Unlike summary percentages, this compares exact (source file, record id) tuples.
"""
import argparse
from pathlib import Path


def covered_identifiers(path):
    covered = {'lines': set(), 'branches': set(), 'functions': set()}
    source = None
    for lineno, raw in enumerate(Path(path).read_text(encoding='utf-8').splitlines(), 1):
        line = raw.strip()
        if line.startswith('SF:'):
            source = line[3:]
        elif line == 'end_of_record':
            source = None
        elif line.startswith(('DA:', 'BRDA:', 'FNDA:')):
            if source is None:
                raise ValueError(f'{path}:{lineno}: coverage entry without SF:')
            if line.startswith('DA:'):
                parts = line[3:].split(',')
                if int(parts[1]) > 0:
                    covered['lines'].add((source, parts[0]))
            elif line.startswith('BRDA:'):
                parts = line[5:].split(',')
                if parts[3] != '-' and int(parts[3]) > 0:
                    covered['branches'].add((source, tuple(parts[:3])))
            elif line.startswith('FNDA:'):
                parts = line[5:].split(',', 1)
                if int(parts[0]) > 0:
                    covered['functions'].add((source, parts[1]))
    return covered


def compare(first, second):
    a, b = covered_identifiers(first), covered_identifiers(second)
    same = True
    for kind in ('lines', 'branches', 'functions'):
        lost, gained = a[kind] - b[kind], b[kind] - a[kind]
        print(f'{kind:10} original={len(a[kind]):5} minimized={len(b[kind]):5} lost={len(lost)} gained={len(gained)}')
        same &= not lost and not gained
    print('IDENTICAL COVERED IDENTIFIERS:', same)
    return same


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('original')
    p.add_argument('minimized')
    args = p.parse_args()
    raise SystemExit(0 if compare(args.original, args.minimized) else 1)
