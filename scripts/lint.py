"""Soát cấu trúc repo trước khi commit: version khớp, skill trỏ đúng file, luật đủ mức/trạng thái/nguồn/test.

Máy chỉ soát hình thức, không hiểu nội dung luật đúng hay sai: việc đó cần người duyệt.

    python scripts/lint.py               soát cả repo, có lỗi thì thoát mã 1
    python scripts/lint.py --self-test   tự kiểm hàm soát luật
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEVELS = {"must", "should", "info"}
STATUSES = {"draft", "reviewed", "verified", "deprecated"}
STALE_DAYS = 180
RULE_HEADING = re.compile(r"^## ([A-Z]+\d+)\. ", re.M)


def read(path):
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def frontmatter_value(text, key):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    v = re.search(rf"^{key}:[ \t]*([^#\n]*)", m.group(1), re.M)
    return v.group(1).strip() if v else None


def check_rule(code, body, today):
    """Soát một mục luật. Trả (lỗi, cảnh báo)."""
    errors, warnings = [], []
    level = re.search(r"Mức:\s*(\w+)", body)
    status = re.search(r"Trạng thái:\s*(\w+)", body)
    if not level or level.group(1) not in LEVELS:
        errors.append(f"{code}: 'Mức:' phải là một trong {sorted(LEVELS)}")
    if not status or status.group(1) not in STATUSES:
        errors.append(f"{code}: 'Trạng thái:' phải là một trong {sorted(STATUSES)}")
    checked = re.findall(r"\(kiểm (\S+?)\)", body)
    if not checked:
        errors.append(f"{code}: chưa có nguồn nào ghi '(kiểm YYYY-MM-DD)'")
    for c in checked:
        try:
            age = (today - date.fromisoformat(c)).days
        except ValueError:
            errors.append(f"{code}: ngày kiểm sai định dạng '{c}'")
            continue
        if age > STALE_DAYS:
            warnings.append(f"{code}: nguồn kiểm đã {age} ngày, đọc lại nguồn")
    test_line = re.search(r"^- Test:(.*)$", body, re.M)
    tests = re.findall(r"`([^`]+)`", test_line.group(1)) if test_line else []
    for t in tests:
        if not (ROOT / t).exists():
            errors.append(f"{code}: không thấy test {t}")
    if status and status.group(1) == "verified" and not tests:
        errors.append(f"{code}: luật verified phải có test")
    return errors, warnings


def split_rules(text):
    parts = RULE_HEADING.split(text)
    return list(zip(parts[1::2], parts[2::2]))


def main():
    today = date.today()
    errors, warnings, codes = [], [], set()

    version = json.loads(read(ROOT / ".claude-plugin" / "plugin.json"))["version"]
    for skill in sorted((ROOT / "skills").iterdir()):
        if not skill.is_dir():
            continue
        name = skill.name
        vfile = skill / "VERSION"
        if not vfile.exists() or read(vfile).strip() != version:
            errors.append(f"skills/{name}/VERSION phải là {version} (theo plugin.json)")
        md = skill / "SKILL.md"
        if not md.exists():
            errors.append(f"skills/{name}: thiếu SKILL.md")
            continue
        text = read(md)
        if frontmatter_value(text, "name") != name:
            errors.append(f"skills/{name}/SKILL.md: 'name' phải là '{name}'")
        if not frontmatter_value(text, "description"):
            errors.append(f"skills/{name}/SKILL.md: thiếu 'description'")
        for ref in set(re.findall(r"`(references/[^`\s]+)`", text)):
            if not (skill / ref).exists():
                errors.append(f"skills/{name}/SKILL.md: không thấy {ref}")
        for rules_file in sorted((skill / "references").glob("rules-*.md")):
            for code, body in split_rules(read(rules_file)):
                if code in codes:
                    errors.append(f"{code}: mã luật bị trùng")
                codes.add(code)
                e, w = check_rule(code, body, today)
                errors += [f"{rules_file.relative_to(ROOT)} {x}" for x in e]
                warnings += [f"{rules_file.relative_to(ROOT)} {x}" for x in w]

    for case in sorted((ROOT / "tests").rglob("*.md")):
        text = read(case)
        rel = case.relative_to(ROOT)
        if frontmatter_value(text, "kind") not in {"positive", "negative"}:
            errors.append(f"{rel}: 'kind' phải là positive hoặc negative")
        for code in re.findall(r"[A-Z]+\d+", frontmatter_value(text, "rules") or ""):
            if code not in codes:
                errors.append(f"{rel}: luật {code} không tồn tại")

    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print("FAIL" if errors else "OK")
    return 1 if errors else 0


def self_test():
    good = "\n- Mức: must · Trạng thái: draft\n- Test: `README.md`\n- Nguồn: [x](u) (kiểm 2026-01-01)\n"
    assert check_rule("A1", good, date(2026, 2, 1)) == ([], [])
    e, w = check_rule("A1", good, date(2027, 1, 1))
    assert not e and w, "nguồn cũ phải cảnh báo"
    bad = good.replace("draft", "done").replace("README.md", "nope.md").replace("(kiểm 2026-01-01)", "")
    e, _ = check_rule("A1", bad, date(2026, 2, 1))
    assert len(e) == 3, e
    verified_no_test = good.replace("draft", "verified").replace("- Test: `README.md`\n", "")
    e, _ = check_rule("A1", verified_no_test, date(2026, 2, 1))
    assert any("verified" in x for x in e), e
    assert [c for c, _ in split_rules("x\n## A1. a\nb\n## A2. c\n")] == ["A1", "A2"]
    print("self-test OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252, không in được tiếng Việt
    if "--self-test" in sys.argv:
        self_test()
    else:
        sys.exit(main())
