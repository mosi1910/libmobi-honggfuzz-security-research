#!/usr/bin/env python3
"""Recreate the verified 1-byte mutation only from an exact authorized seed."""
import argparse
import hashlib
from pathlib import Path

SEED_SHA256 = '34fc67043eeeaa6563481d6ea2fea1b5349cb73e459a1f10e3aa09186f56302e'
EXPECTED_OUTPUT_SHA256 = '3153f56016c369e844c91372a1af1b93584318c937e4e46050eec0e0357e0bc3'
OFFSET = 15378


def derive(seed_path, output_path):
    data = Path(seed_path).read_bytes()
    actual_hash = hashlib.sha256(data).hexdigest()
    if actual_hash != SEED_SHA256:
        raise ValueError('Incorrect original seed (SHA-256 mismatch). Refusing modification.')
    if len(data) != 84412 or data[OFFSET] != 0x00:
        raise ValueError('Original bytes do not match the verified reference seed.')
    mutated = bytearray(data)
    mutated[OFFSET] = 0xFF
    digest = hashlib.sha256(mutated).hexdigest()
    if digest != EXPECTED_OUTPUT_SHA256:
        raise AssertionError('Derived input hash mismatch; investigate input and code.')
    destination = Path(output_path)
    if destination.exists():
        raise FileExistsError(f'Refusing overwrite: {destination}')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(mutated)
    print(f'Created {destination} ({len(mutated)} bytes)')
    print(f'SHA256: {digest}')

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_seed', help='Authorized local copy of the EXACT original seed')
    p.add_argument('output_mobi', help='New file; must not already exist')
    args=p.parse_args()
    derive(args.source_seed, args.output_mobi)
