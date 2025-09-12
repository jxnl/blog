#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR="docs/systematically-improve-your-rag"

echo "🔍 Checking for disallowed assets in $TARGET_DIR (pdf, txt, *-slides.md) ..."

if [ ! -d "$TARGET_DIR" ]; then
  echo "✅ Target directory not found, skipping."
  exit 0
fi

mapfile -t found < <(find "$TARGET_DIR" -type f \( -name "*.pdf" -o -name "*.txt" -o -name "*-slides.md" \) ) || true

if [ ${#found[@]} -gt 0 ]; then
  echo "❌ Disallowed files detected in $TARGET_DIR:"
  for f in "${found[@]}"; do
    echo " - $f"
  done
  echo "\nPlease remove these files. PDFs, TXTs, and slide markdown are not tracked in this section."
  exit 1
fi

echo "✅ No disallowed assets found."
