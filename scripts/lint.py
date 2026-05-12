#!/usr/bin/env python3
"""
Anthology DLC linter.
Validates DLC files across all types: books, includes, overlays, companions.

Usage:
    python3 scripts/lint.py                        # lint all DLCs in vault
    python3 scripts/lint.py books/farsi-workplace/dlc.md  # lint one file
    python3 scripts/lint.py books/                 # lint all books
"""

import sys
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).parent.parent

# --- Type detection ---

def detect_type(path: Path) -> str:
    parts = path.parts
    if "books" in parts:
        return "book"
    if "includes" in parts:
        return "include"
    if "overlays" in parts:
        return "overlay"
    if "companions" in parts:
        return "companion"
    return "unknown"

# --- Field checkers ---

def has(content: str, pattern: str) -> bool:
    return bool(re.search(pattern, content, re.IGNORECASE | re.MULTILINE))

def check_universal(content: str, path: Path) -> list[str]:
    errors = []
    if not has(content, r"^(DLC|Include|Overlay) Name:"):
        errors.append("Missing Name field (DLC Name / Include Name / Overlay Name)")
    if not has(content, r"^(DLC|Include|Overlay) ID:"):
        errors.append("Missing ID field (DLC ID / Include ID / Overlay ID)")
    if not has(content, r"^(DLC|Include|Overlay) Desc:"):
        errors.append("Missing Desc field")
    if not has(content, r"On Load"):
        errors.append("Missing On Load message")
    if not has(content, r"On Error"):
        errors.append("Missing On Error message")
    return errors

def check_book(content: str) -> list[str]:
    errors = []
    if not has(content, r"RUNTIME CONFIG"):
        errors.append("Missing RUNTIME CONFIG section")
    else:
        if not has(content, r"^language:"):
            errors.append("Runtime Config missing: language")
        if not has(content, r"^city:"):
            errors.append("Runtime Config missing: city")
        if not has(content, r"^narrative_register:"):
            errors.append("Runtime Config missing: narrative_register")
    if not has(content, r"CURRICULUM SEEDS"):
        errors.append("Missing CURRICULUM SEEDS section")
    else:
        for stage in ["Intro", "Midgame", "Endgame"]:
            if not has(content, rf"### {stage}"):
                errors.append(f"Curriculum Seeds missing stage: {stage}")
            else:
                section = extract_section(content, f"### {stage}")
                if not has(section, r"- situation:"):
                    errors.append(f"{stage}: no situation seeds")
                if not has(section, r"- vocab:"):
                    errors.append(f"{stage}: no vocab seeds")
                if not has(section, r"- cultural:"):
                    errors.append(f"{stage}: no cultural seeds")
    if not has(content, r"Game Master Instructions"):
        errors.append("Missing Game Master Instructions section")
    return errors

def check_include(content: str) -> list[str]:
    errors = []
    if not has(content, r"## Learning Goals"):
        errors.append("Missing Learning Goals section")
    if not has(content, r"### Hand \d+"):
        errors.append("Missing at least one Hand (### Hand 1)")
    if not has(content, r"## Completion Criteria"):
        errors.append("Missing Completion Criteria section")
    if not has(content, r"## Return"):
        errors.append("Missing Return section")
    return errors

def check_overlay(content: str) -> list[str]:
    errors = []
    if not has(content, r"^Rule:"):
        errors.append("Missing at least one Rule")
    if not has(content, r"[Dd]eactivat"):
        errors.append("Missing deactivation conditions")
    return errors

def check_companion(content: str) -> list[str]:
    errors = []
    if not has(content, r"Requires:"):
        errors.append("Missing Requires field (companion mechanics dependency)")
    if not has(content, r"## Companion Definition"):
        errors.append("Missing Companion Definition section")
    else:
        section = extract_section(content, "## Companion Definition")
        if not has(section, r"Name:"):
            errors.append("Companion Definition missing: Name")
        if not has(section, r"Short Description:"):
            errors.append("Companion Definition missing: Short Description")
    if not has(content, r"## Personality"):
        errors.append("Missing Personality section")
    if not has(content, r"## Role"):
        errors.append("Missing Role section")
    return errors

def extract_section(content: str, heading: str) -> str:
    pattern = rf"{re.escape(heading)}(.*?)(?=\n##|\Z)"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1) if match else ""

# --- Lint a single file ---

def lint_file(path: Path) -> tuple[int, int]:
    dlc_type = detect_type(path)
    if dlc_type == "unknown":
        print(f"⚠  SKIP  {path} (unknown type)")
        return 0, 0

    content = path.read_text()
    errors = check_universal(content, path)

    if dlc_type == "book":
        errors += check_book(content)
    elif dlc_type == "include":
        errors += check_include(content)
    elif dlc_type == "overlay":
        errors += check_overlay(content)
    elif dlc_type == "companion":
        errors += check_companion(content)

    rel = path.relative_to(VAULT_ROOT)
    if errors:
        print(f"✗  FAIL  {rel}  [{dlc_type}]")
        for e in errors:
            print(f"         • {e}")
        return 0, 1
    else:
        print(f"✓  PASS  {rel}  [{dlc_type}]")
        return 1, 0

# --- Collect files ---

def collect_files(target: Path) -> list[Path]:
    if target.is_file():
        return [target]
    patterns = {
        "books": "*/dlc.md",
        "includes": "*/include.md",
        "overlays": "*/overlay.md",
        "assets/companions": "*/dlc.md",
    }
    files = []
    for folder, pattern in patterns.items():
        folder_path = VAULT_ROOT / folder
        if folder_path.exists():
            if target == VAULT_ROOT or target == folder_path or folder_path.is_relative_to(target):
                files += sorted(folder_path.glob(pattern))
    return files

# --- Main ---

def main():
    target = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else VAULT_ROOT
    files = collect_files(target)

    if not files:
        print("No DLC files found.")
        sys.exit(0)

    passed = failed = 0
    for f in files:
        p, fa = lint_file(f)
        passed += p
        failed += fa

    print(f"\n{passed + failed} checked — {passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
