#!/bin/sh
set -eu

: "${MOBI_FUZZ_ROOT:?Project path is missing}"
: "${HF01_DIR:?Experiment path is missing}"

date -Is > "$HF01_DIR/start-time.txt"

"$MOBI_FUZZ_ROOT/honggfuzz/honggfuzz" \
  -i "$MOBI_FUZZ_ROOT/seeds-original" \
  --output "$HF01_DIR/corpus" \
  -W "$HF01_DIR/work" \
  -l "$HF01_DIR/honggfuzz.log" \
  --statsfile "$HF01_DIR/stats.txt" \
  -n 1 \
  -t 10 \
  -F 4194304 \
  --run_time 3600 \
  -- "$MOBI_FUZZ_ROOT/run-mobitool-noasan.sh" \
  -s -o "$HF01_DIR/extracted" ___FILE___

