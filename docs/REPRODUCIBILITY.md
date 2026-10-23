# Reproducibility and environment

## What is independently checkable from this public repository?

The coverage-set comparison and campaign summaries execute without the target, fuzzing engine, or private input corpus:

```bash
python3 scripts/compare_lcov.py data/coverage/original.lcov data/coverage/minimized.lcov
python3 scripts/summarize_campaigns.py data/campaigns.csv
python3 -m unittest discover -s tests -v
```

These analyze **archived experimental evidence**. They **do not** independently re-run the 21 experiments, establish mutation-operation counts, or prove that the historical flaw is exploitable beyond the recorded memory-safety fault.

## Original research environment

- Host: VMware virtual machine, Kali Linux 2026.3 (x86-64), 4 vCPUs, approximately 1.9 GiB RAM
- Compiler: Debian Clang 21.1.8 (13), language mode `gnu23`
- Honggfuzz revision: `940b958dfeb6f9131fd846cae31fcc0fe996ae98`
- Target revision: `aac5b1f578b284b2f886d6d25cde22a33d8534f8` (libmobi v0.10)
- Harness: the `mobitool` command-line executable; historical wrapper passed a MOBI input path and used a temporary output directory
- Original configure options: `--disable-shared --enable-static --with-libxml2=no`
- Common compiler flags: `-O1 -g -fno-omit-frame-pointer`
- Sanitized CFLAGS: also `-fsanitize=address`; ASan linker flags `-fsanitize=address`
- Non-ASan build used the Honggfuzz Clang wrapper with no ASan flags
- Some versions required environment-specific compatibility adjustments for Clang 21 and XML header handling; **do not assume a clean unmodified v0.10 checkout builds on every modern distribution without adaptation**.

The complete historical compiler/configuration snapshot is preserved in [`evidence/verified_build_configuration.txt`](../evidence/verified_build_configuration.txt). Machine-specific absolute paths reflect the original Kali setup; scripts in this repository are portable wherever possible.

## Review or locally reproduce the one-byte mutation

You must already possess the **exact permitted original 84,412-byte seed**. The generator confirms its SHA-256 to prevent accidentally modifying another MOBI file.

```bash
python3 scripts/derive_reproducer.py \
  /path/to/sample-obfuscated-fonts.mobi \
  /tmp/one-byte-reproducer.mobi
```

The generator does not run the vulnerable target. To test actual memory-safety behavior, independently obtain libmobi v0.10, prepare an instrumented build and compare behavior under ASan against the upstream-patched versions. For parser runs, `mobitool` expects `-s -o OUTPUT_DIRECTORY INPUT_FILE`; use a throwaway output directory and run only in an isolated testing environment.

For a documented demonstration patch, from the **root of the cloned libmobi v0.10 checkout**:

```bash
# Point to wherever this portfolio repository was unpacked:
PORTFOLIO_DIR="/absolute/path/to/libmobi-honggfuzz-security-research"

git apply --check "$PORTFOLIO_DIR/patches/font_xor_bounds_check.patch"
git apply "$PORTFOLIO_DIR/patches/font_xor_bounds_check.patch"
```

Run `git apply --check` before applying the patch; if it fails, inspect the exact target revision and patch context. Rebuild after applying; do not apply the demonstration patch to later fixed releases.

## Privacy-normalized evidence

For the public LCOV exports only the `SF:` file-path prefix was normalized from a workstation-specific path to `libmobi/…`; counters and covered identifiers were retained. The private original LCOV exports and LLVM `merged.profdata` files were separately inspected during the audit, but the profdata (which may embed paths and build-specific artifacts) is **not published**.

The original nine MOBI seeds, three fuzz-generated crash binaries and minimized derivative are **not redistributed**. The repository provides cryptographic hashes, a deterministic one-byte mutation generator, summarized results, sampled error logs, and the complete methodological PDF. Re-running the full campaign set requires the original corpus and locally built fuzzing binaries, neither of which is supplied here.

## Known limitations

- 4 of 21 experiment records lack parseable final summaries; historical mentions are not substituted as authenticated log-derived metrics.
- Coverage equality is specific to the **archived LLVM LCOV exports**. This does not prove equivalence of internal Honggfuzz coverage signatures or that a fresh run on another environment will be identical.
- Dictionary analysis had only two repetitions per configuration.
- UBSan HF-19 yielded a crash corroborated with ASan; an explicit UBSan-specific diagnostic was not established.
- The reported iteration count is not a separately instrumented mutation count.
