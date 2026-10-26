"""Check rules in knowledge/ and skills in skills/ follow the repo conventions.

Usage: python scripts/check_rules.py [--self-test]
Exit code 1 if any error. Stdlib only so it runs anywhere.
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["id", "title", "domain", "requirement", "status", "sources", "evals"]
STATUS = {"draft", "reviewed", "verified", "deprecated"}
REQUIREMENT = {"must", "should", "info"}
STALE_DAYS = 180


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text.replace("\r\n", "\n"), re.S)
    return m.group(1) if m else None


def top_value(fm, key):
    # shortcut: only top-level "key: value" lines, not full YAML; switch to PyYAML if rules need nesting beyond sources/evals
    m = re.search(rf"^{key}:[ \t]*([^#\n]*)", fm, re.M)
    return m.group(1).strip() if m else None


def check_rule(path, fm, today):
    errors, warnings = [], []
    for key in REQUIRED:
        if top_value(fm, key) is None:
            errors.append(f"missing '{key}'")
    rid = top_value(fm, "id")
    if rid and rid != path.stem:
        errors.append(f"id '{rid}' != filename '{path.stem}'")
    if top_value(fm, "status") not in STATUS:
        errors.append(f"status must be one of {sorted(STATUS)}")
    if top_value(fm, "requirement") not in REQUIREMENT:
        errors.append(f"requirement must be one of {sorted(REQUIREMENT)}")
    checked = re.findall(r"checked:\s*(\S+)", fm)
    if not checked:
        errors.append("no source with 'checked:' date")
    for c in checked:
        try:
            age = (today - date.fromisoformat(c)).days
        except ValueError:
            errors.append(f"bad checked date '{c}'")
            continue
        if age > STALE_DAYS:
            warnings.append(f"source checked {age} days ago")
    evals_block = re.search(r"^evals:\n((?:[ \t]+-.*\n?)*)", fm + "\n", re.M)
    eval_paths = re.findall(r"-\s*(\S+)", evals_block.group(1)) if evals_block else []
    for e in eval_paths:
        if not (ROOT / e).exists():
            errors.append(f"eval not found: {e}")
    if top_value(fm, "status") == "verified" and not eval_paths:
        errors.append("verified rule needs at least one eval")
    return errors, warnings


def check_skill(path, fm):
    errors = []
    if top_value(fm, "name") != path.parent.name:
        errors.append(f"name must equal folder '{path.parent.name}'")
    if not top_value(fm, "description"):
        errors.append("missing description")
    for ref in re.findall(r"`(knowledge/[^`]+\.md)`", path.read_text(encoding="utf-8")):
        if not (ROOT / ref).exists():
            errors.append(f"rule not found: {ref}")
    return errors


def main():
    today = date.today()
    failed = False
    for path in sorted((ROOT / "knowledge").rglob("*.md")):
        if path.name.startswith("_"):
            continue
        fm = frontmatter(path.read_text(encoding="utf-8"))
        errors, warnings = (["no frontmatter"], []) if fm is None else check_rule(path, fm, today)
        for w in warnings:
            print(f"WARN  {path.relative_to(ROOT)}: {w}")
        for e in errors:
            print(f"ERROR {path.relative_to(ROOT)}: {e}")
        failed |= bool(errors)
    for path in sorted((ROOT / "skills").glob("*/SKILL.md")):
        fm = frontmatter(path.read_text(encoding="utf-8"))
        errors = ["no frontmatter"] if fm is None else check_skill(path, fm)
        for e in errors:
            print(f"ERROR {path.relative_to(ROOT)}: {e}")
        failed |= bool(errors)
    print("FAIL" if failed else "OK")
    return 1 if failed else 0


def self_test():
    good = "id: X\nstatus: draft\nrequirement: must\nsources:\n  - url: u\n    checked: 2026-01-01\nevals:\n  - README.md\n"
    p = Path("X.md")
    errs, warns = check_rule(p, "title: t\ndomain: d\n" + good, date(2026, 2, 1))
    assert errs == [] and warns == [], (errs, warns)
    errs, warns = check_rule(p, "title: t\ndomain: d\n" + good, date(2027, 1, 1))
    assert warns and not errs, "stale source should warn"
    bad = good.replace("status: draft", "status: done").replace("README.md", "nope.md")
    errs, _ = check_rule(p, "title: t\ndomain: d\n" + bad, date(2026, 2, 1))
    assert any("status" in e for e in errs) and any("nope.md" in e for e in errs), errs
    print("self-test OK")


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        self_test()
    else:
        sys.exit(main())
