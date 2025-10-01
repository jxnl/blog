#!/usr/bin/env python3
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
TARGET = BASE / "docs" / "systematically-improve-your-rag"

def fix_file(p: Path) -> bool:
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines()
    changed = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.lstrip().startswith("!!! "):
            j = i + 1
            if j < len(lines):
                nxt = lines[j]
                if nxt.strip() != "" and not nxt.startswith("    "):
                    lines[j] = "    " + nxt
                    changed = True
        i += 1
    if changed:
        p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    if not TARGET.exists():
        print(f"Target directory not found: {TARGET}")
        return 1
    total = 0
    for p in sorted(TARGET.glob("*.md")):
        if p.name.endswith("-slides.md"):
            continue
        if fix_file(p):
            total += 1
    print(f"Admonitions fixed in {total} files")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

