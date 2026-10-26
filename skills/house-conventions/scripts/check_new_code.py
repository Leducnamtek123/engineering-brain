"""Ratchet: chỉ soát các dòng MỚI thêm so với REF theo luật trong file cấu hình của dự án (luật H3).

    python check_new_code.py --config conventions.json [--repo DIR] [--base REF]
    python check_new_code.py --config conventions.json --blocks    in danh sách building block (luật H2)
    python check_new_code.py --self-test

Code cũ vi phạm thì để yên; chỉ chặn vi phạm mới. Tính cả file mới chưa được git add.
Cấu hình: {"building_blocks": [{"path", "note"}], "rules": [{"id", "paths", "pattern", "unless"?, "message"}],
"i18n"?: {"paths", "locales": [thư mục mỗi ngôn ngữ chứa <namespace>.json], "default_ns"}}.
Có "i18n" thì mọi key t('...') trong dòng mới phải có trong MỌI thư mục locale (luật I18N-KEY): regex không
thấy được key thiếu, nên chặn được kiểu "xóa chuỗi hardcode nhưng quên thêm key".
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


T_CALL = re.compile(r"\bt\(\s*['\"]([^'\"`$]+)['\"]")
USE_NS = re.compile(r"useTranslation\(\s*\[?\s*['\"]([\w.-]+)['\"]")
PLURALS = ("_one", "_other", "_zero", "_few", "_many", "_two")


def has_key(data, key):
    if key in data:  # key phẳng có dấu chấm
        return True
    for part in key.split("."):
        if not isinstance(data, dict) or part not in data:
            return False
        data = data[part]
    return True


def check_i18n(lines, cfg, repo):
    """Key t('...') trong dòng mới phải có ở mọi locale. Trả cùng dạng với check()."""
    paths = [glob_to_regex(g) for g in cfg["paths"]]
    cache, ns_of, found = {}, {}, []

    def load(locale, ns):
        f = Path(repo) / locale / f"{ns}.json"
        if (locale, ns) not in cache:
            try:
                cache[locale, ns] = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                cache[locale, ns] = None
        return cache[locale, ns]

    for path, line_no, text in lines:
        if not any(p.match(path) for p in paths):
            continue
        if path not in ns_of:
            try:
                m = USE_NS.search((Path(repo) / path).read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError):
                m = None
            ns_of[path] = m.group(1) if m else cfg.get("default_ns", "translation")
        for key in T_CALL.findall(text):
            ns, _, k = key.rpartition(":") if ":" in key else (ns_of[path], "", key)
            missing = [loc for loc in cfg["locales"]
                       if not any(has_key(load(loc, ns) or {}, k + s) for s in ("",) + PLURALS)]
            if missing:
                found.append((path, line_no, "I18N-KEY", f"key '{key}' (namespace {ns}) chưa có trong: "
                              + ", ".join(missing), text.strip()))
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
    lines = collect(args.repo, args.base)
    found = check(lines, compile_rules(config))
    if config.get("i18n"):
        found += check_i18n(lines, config["i18n"], args.repo)
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
    import tempfile
    with tempfile.TemporaryDirectory() as repo:
        for loc, data in (("vi", {"a": {"b": "x"}, "n_one": "1"}), ("en", {"a": {"b": "x"}})):
            (Path(repo) / "loc" / loc).mkdir(parents=True)
            (Path(repo) / "loc" / loc / "emp.json").write_text(json.dumps({**data, "n_other": "x"}), encoding="utf-8")
        (Path(repo) / "src").mkdir()
        (Path(repo) / "src" / "P.tsx").write_text("const { t } = useTranslation('emp');\n", encoding="utf-8")
        lines = [("src/P.tsx", 2, "{t('a.b')} {t('n')} {t(`x.${y}`)}"), ("src/P.tsx", 3, "{t('a.c', 'mặc định')}"),
                 ("src/P.tsx", 4, "{t('emp:a.b')} {t('other:a.b')}")]
        got = check_i18n(lines, {"paths": ["src/**/*.tsx"], "locales": ["loc/vi", "loc/en"]}, repo)
        assert [(f[1], f[2]) for f in got] == [(3, "I18N-KEY"), (4, "I18N-KEY")], got
        assert "loc/vi, loc/en" in got[0][3] and "other" in got[1][3], got
    assert glob_to_regex("src/**/*.tsx").match("src/B.tsx") and not glob_to_regex("src/**/*.tsx").match("lib/B.tsx")
    print("self-test OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    if "--self-test" in sys.argv:
        self_test()
    else:
        sys.exit(main())
