"""Ratchet: chỉ soát các dòng MỚI thêm so với REF theo luật trong file cấu hình của dự án (luật H3).

    python check_new_code.py --config conventions.json [--repo DIR] [--base REF]
    python check_new_code.py --config conventions.json --blocks    in danh sách building block (luật H2)
    python check_new_code.py --self-test

Code cũ vi phạm thì để yên; chỉ chặn vi phạm mới. Tính cả file mới chưa được git add.
Cấu hình: {"building_blocks": [{"path", "note"}], "rules": [{"id", "paths", "pattern", "unless"?, "message"}]}.
Có vi phạm thì thoát mã 1.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def glob_to_regex(glob):
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif glob.startswith("**", i):
            out, i = out + ".*", i + 2
        elif glob[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif glob[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(glob[i]), i + 1
    return re.compile(out + "$")


def compile_rules(config):
    rules = []
    for r in config["rules"]:
        rules.append({
            "id": r["id"],
            "paths": [glob_to_regex(g) for g in r["paths"]],
            "pattern": re.compile(r["pattern"]),
            "unless": re.compile(r["unless"]) if r.get("unless") else None,
            "message": r["message"],
        })
    return rules


def added_lines(diff_text):
    """Yield (path, line_no, text) for every '+' line of a unified=0 diff."""
    path, line_no = None, 0
    for raw in diff_text.splitlines():
        if raw.startswith("+++ "):
            path = None if raw[4:] == "/dev/null" else re.sub(r"^b/", "", raw[4:])
        elif raw.startswith("@@"):
            line_no = int(re.search(r"\+(\d+)", raw).group(1))
        elif raw.startswith("+") and path:
            yield path, line_no, raw[1:]
            line_no += 1


def check(lines, rules):
    found = []
    for path, line_no, text in lines:
        for r in rules:
            if not any(p.match(path) for p in r["paths"]):
                continue
            if r["pattern"].search(text) and not (r["unless"] and r["unless"].search(text)):
                found.append((path, line_no, r["id"], r["message"], text.strip()))
    return found


def collect(repo, base):
    git = ["git", "-C", repo]
    diff = subprocess.run(git + ["diff", "--no-color", "--unified=0", base], capture_output=True,
                          text=True, encoding="utf-8", check=True).stdout
    lines = list(added_lines(diff))
    untracked = subprocess.run(git + ["ls-files", "--others", "--exclude-standard"], capture_output=True,
                               text=True, encoding="utf-8", check=True).stdout.split()
    for rel in untracked:
        try:
            content = (Path(repo) / rel).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        lines += [(rel, i, t) for i, t in enumerate(content.splitlines(), 1)]
    return lines


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    p.add_argument("--repo", default=".")
    p.add_argument("--base", default="HEAD")
    p.add_argument("--blocks", action="store_true")
    args = p.parse_args()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    if args.blocks:
        for b in config.get("building_blocks", []):
            print(f"{b['path']}: {b['note']}")
        return 0
    found = check(collect(args.repo, args.base), compile_rules(config))
    for path, line_no, rule_id, message, text in found:
        print(f"WARN {path}:{line_no} [{rule_id}] {message}\n     {text[:160]}")
    print(f"{len(found)} vi phạm trong dòng mới")
    return 1 if found else 0


def self_test():
    config = {"rules": [
        {"id": "NO-MUI", "paths": ["src/**/*.tsx"], "pattern": "from ['\"]@mui/|\\bsx=\\{", "message": "mui"},
        {"id": "ON-COMMIT", "paths": ["api/**/*.py"], "pattern": "\\.delay\\(", "unless": "on_commit", "message": "oc"},
    ]}
    rules = compile_rules(config)
    diff = (
        "diff --git a/src/a/B.tsx b/src/a/B.tsx\n--- a/src/a/B.tsx\n+++ b/src/a/B.tsx\n"
        "@@ -3,0 +4,2 @@\n+import Button from '@mui/material/Button';\n+<Box className=\"p-2\" />\n"
        "diff --git a/api/x/views.py b/api/x/views.py\n--- a/api/x/views.py\n+++ b/api/x/views.py\n"
        "@@ -10,0 +11,2 @@\n+    notify.delay(job.id)\n+    transaction.on_commit(lambda: notify.delay(job.id))\n"
    )
    found = check(list(added_lines(diff)), rules)
    assert [(f[0], f[1], f[2]) for f in found] == [("src/a/B.tsx", 4, "NO-MUI"), ("api/x/views.py", 11, "ON-COMMIT")], found
    assert glob_to_regex("src/**/*.tsx").match("src/B.tsx") and not glob_to_regex("src/**/*.tsx").match("lib/B.tsx")
    print("self-test OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    if "--self-test" in sys.argv:
        self_test()
    else:
        sys.exit(main())
