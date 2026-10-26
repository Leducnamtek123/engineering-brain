"""Flag changes to test files that can make a suite pass without fixing code (luật T1).

    python check_test_diff.py [--base REF] [--repo DIR]   so working tree với REF (mặc định HEAD)
    python check_test_diff.py --self-test

Chỉ bắt dấu hiệu bằng chữ: xoá test, thêm skip/only, giảm assert, sửa dòng assert, cập nhật snapshot.
Cảnh báo không có nghĩa là sai; nghĩa là phải có lời giải thích. Hardcode trong code (T2) không bắt được ở đây.
Có cảnh báo thì thoát mã 1.
"""
import argparse
import re
import subprocess
import sys

TEST_FILE = re.compile(
    r"(^|/)(tests?|__tests__|spec)/|\.(test|spec)\.[cm]?[jt]sx?$|(^|/)test_[^/]*\.py$|_test\.(py|go)$|\.snap$"
)
TEST_DEF = re.compile(r"^\s*(it|test)(\.each\b.*)?\s*\(|^\s*(async\s+)?def test_\w*|^\s*func Test\w*")
SKIP = re.compile(
    r"\.(skip|only|todo)\s*\(|\bx(it|describe|test)\s*\(|@pytest\.mark\.(skip|xfail)|@unittest\.(skip|expectedFailure)|\bt\.Skip(Now|f)?\("
)
ASSERT = re.compile(r"\bexpect\s*\(|\bassert\w*\s*[(\s]|self\.assert\w+\s*\(|\bt\.(Error|Fatal)f?\(")


def analyse(diff_text):
    """Return a list of 'file: message' warnings for a unified diff."""
    warnings = []
    files = re.split(r"^diff --git ", diff_text, flags=re.M)[1:]
    for chunk in files:
        m = re.search(r"^\+\+\+ (?:b/)?(\S+)", chunk, re.M) or re.search(r"^--- (?:a/)?(\S+)", chunk, re.M)
        path = m.group(1) if m else chunk.split()[0]
        if path == "/dev/null":
            path = re.search(r"^--- (?:a/)?(\S+)", chunk, re.M).group(1)
        if not TEST_FILE.search(path):
            continue
        if path.endswith(".snap"):
            warnings.append(f"{path}: snapshot bị cập nhật")
            continue
        removed_defs = added_defs = removed_asserts = added_asserts = 0
        for hunk in re.split(r"^@@.*@@.*$", chunk, flags=re.M)[1:]:
            minus = [l[1:] for l in hunk.splitlines() if l.startswith("-") and not l.startswith("---")]
            plus = [l[1:] for l in hunk.splitlines() if l.startswith("+") and not l.startswith("+++")]
            removed_defs += sum(bool(TEST_DEF.search(l)) for l in minus)
            added_defs += sum(bool(TEST_DEF.search(l)) for l in plus)
            hunk_minus_asserts = [l.strip() for l in minus if ASSERT.search(l)]
            hunk_plus_asserts = [l.strip() for l in plus if ASSERT.search(l)]
            removed_asserts += len(hunk_minus_asserts)
            added_asserts += len(hunk_plus_asserts)
            for line in plus:
                if SKIP.search(line) and not any(SKIP.search(o) for o in minus):
                    warnings.append(f"{path}: thêm skip/only/xfail: {line.strip()}")
            if hunk_minus_asserts and hunk_plus_asserts:
                warnings.append(f"{path}: sửa assert: '{hunk_minus_asserts[0]}' -> '{hunk_plus_asserts[0]}'")
        if removed_defs > added_defs:
            warnings.append(f"{path}: xoá {removed_defs - added_defs} test")
        if removed_asserts > added_asserts:
            warnings.append(f"{path}: giảm {removed_asserts - added_asserts} assert")
    return warnings


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", default="HEAD")
    p.add_argument("--repo", default=".")
    args = p.parse_args()
    diff = subprocess.run(
        ["git", "-C", args.repo, "diff", "--no-color", "--unified=0", args.base],
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    warnings = analyse(diff)
    for w in warnings:
        print(f"WARN {w}")
    print("FLAGGED" if warnings else "OK")
    return 1 if warnings else 0


def self_test():
    clean = "diff --git a/src/a.py b/src/a.py\n--- a/src/a.py\n+++ b/src/a.py\n@@ -1 +1 @@\n-x = 1\n+x = 2\n"
    assert analyse(clean) == []
    edit = (
        "diff --git a/test_vat.py b/test_vat.py\n--- a/test_vat.py\n+++ b/test_vat.py\n"
        "@@ -9 +9 @@\n-        self.assertEqual(vat(250_000), 25_001)\n+        self.assertEqual(vat(250_000), 25_000)\n"
    )
    assert any("sửa assert" in w for w in analyse(edit)), analyse(edit)
    removed = (
        "diff --git a/src/x.test.ts b/src/x.test.ts\n--- a/src/x.test.ts\n+++ b/src/x.test.ts\n"
        "@@ -3,3 +2,0 @@\n-  it('boundary', () => {\n-    expect(f(5)).toBe(1);\n-  });\n"
    )
    w = analyse(removed)
    assert any("xoá 1 test" in x for x in w) and any("giảm 1 assert" in x for x in w), w
    skipped = (
        "diff --git a/tests/test_s.py b/tests/test_s.py\n--- a/tests/test_s.py\n+++ b/tests/test_s.py\n"
        "@@ -4,0 +5 @@\n+    @unittest.skip('flaky')\n"
    )
    assert any("skip" in x for x in analyse(skipped)), analyse(skipped)
    snap = "diff --git a/__snapshots__/a.test.ts.snap b/__snapshots__/a.test.ts.snap\n--- a/x\n+++ b/__snapshots__/a.test.ts.snap\n@@ -1 +1 @@\n-a\n+b\n"
    assert any("snapshot" in x for x in analyse(snap)), analyse(snap)
    print("self-test OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    if "--self-test" in sys.argv:
        self_test()
    else:
        sys.exit(main())
