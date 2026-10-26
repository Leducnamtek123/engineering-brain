"""Flag risky statements in SQL migrations (Postgres) — luật M1–M3.

    python check_migration.py <file.sql | thư mục>...   mặc định: prisma/migrations
    python check_migration.py --self-test

Bắt bằng regex trên từng câu lệnh, không phải SQL parser: đủ cho migration Prisma sinh ra.
Cần soát kỹ hơn thì dùng Squawk (squawkhq.com). Có cảnh báo thì thoát mã 1.
"""
import re
import sys
from pathlib import Path

CHECKS = [
    ("M1", re.compile(r"\bRENAME\s+(COLUMN\b|TO\b)", re.I), "đổi tên: bản app cũ sẽ lỗi khi rolling deploy, dùng expand-contract"),
    ("M1", re.compile(r"\bDROP\s+(COLUMN|TABLE)\b", re.I), "xoá cột/bảng: mất dữ liệu, chỉ làm ở bước contract khi không còn code dùng"),
    ("M1", re.compile(r"\bALTER\s+COLUMN\s+\S+\s+(SET\s+DATA\s+)?TYPE\b", re.I), "đổi kiểu cột: ghi lại bảng và có thể vỡ code cũ"),
    ("M2", re.compile(r"\bSET\s+NOT\s+NULL\b", re.I), "SET NOT NULL: quét toàn bảng, lỗi nếu còn NULL; backfill + CHECK NOT VALID trước"),
    ("M3", re.compile(r"\bCREATE\s+(UNIQUE\s+)?INDEX\b(?!\s+CONCURRENTLY)", re.I), "CREATE INDEX không CONCURRENTLY: khoá ghi tới khi xong"),
    ("M4", re.compile(r"\bTRUNCATE\b|\bDELETE\s+FROM\s+\S+\s*$", re.I), "xoá dữ liệu hàng loạt trong migration"),
]
ADD_NOT_NULL = re.compile(r"\bADD\s+(COLUMN\s+)?\S+\s+[^,]*\bNOT\s+NULL\b", re.I)
VOLATILE_DEFAULT = re.compile(r"\bDEFAULT\s+(clock_timestamp|random|gen_random_uuid|uuid_generate_v4|timeofday)\s*\(", re.I)
CREATE_TABLE = re.compile(r'\bCREATE\s+TABLE\s+(IF\s+NOT\s+EXISTS\s+)?("?[\w.]+"?)', re.I)
INDEX_ON = re.compile(r'\bON\s+("?[\w.]+"?)', re.I)


def statements(sql):
    sql = re.sub(r"--[^\n]*", "", sql)
    return [s.strip() for s in sql.split(";") if s.strip()]


def check_sql(sql):
    """Return (rule, message, statement) for each risky statement."""
    found = []
    stmts = statements(sql)
    new_tables = {m.group(2).strip('"').lower() for s in stmts for m in [CREATE_TABLE.search(s)] if m}
    for s in stmts:
        flat = " ".join(s.split())
        for rule, pattern, message in CHECKS:
            if not pattern.search(flat):
                continue
            if rule == "M3":
                target = INDEX_ON.search(flat)
                if target and target.group(1).strip('"').lower() in new_tables:
                    continue  # bảng vừa tạo trong cùng migration, chưa có dữ liệu
            found.append((rule, message, flat))
        if ADD_NOT_NULL.search(flat) and ("DEFAULT" not in flat.upper() or VOLATILE_DEFAULT.search(flat)):
            if not CREATE_TABLE.search(flat):
                found.append(("M2", "thêm cột NOT NULL không có default hằng số: lỗi khi bảng có dữ liệu hoặc ghi lại bảng", flat))
    return found


def main(args):
    targets = [Path(a) for a in args] or [Path("prisma/migrations")]
    files = [f for t in targets for f in ([t] if t.is_file() else sorted(t.rglob("*.sql")))]
    total = 0
    for f in files:
        for rule, message, stmt in check_sql(f.read_text(encoding="utf-8")):
            total += 1
            print(f"WARN {f} [{rule}] {message}\n     {stmt[:160]}")
    print(f"{len(files)} file, {total} cảnh báo")
    return 1 if total else 0


def self_test():
    assert check_sql('CREATE TABLE "Tag" ("id" TEXT NOT NULL); CREATE INDEX "Tag_i" ON "Tag"("id");') == []
    assert check_sql('ALTER TABLE "User" ADD COLUMN "nick" TEXT;') == []
    assert check_sql("ALTER TABLE \"Order\" ADD COLUMN \"channel\" TEXT NOT NULL DEFAULT 'web';") == []
    rules = lambda sql: [r for r, _, _ in check_sql(sql)]
    assert rules('ALTER TABLE "User" RENAME COLUMN "fullName" TO "name";') == ["M1"]
    assert rules('ALTER TABLE "User" DROP COLUMN "fullName";') == ["M1"]
    assert rules('CREATE INDEX "Order_c_idx" ON "Order"("customerId");') == ["M3"]
    assert rules('CREATE INDEX CONCURRENTLY "Order_c_idx" ON "Order"("customerId");') == []
    assert rules('ALTER TABLE "User" ADD COLUMN "phone" TEXT NOT NULL;') == ["M2"]
    assert rules('ALTER TABLE "User" ALTER COLUMN "phone" SET NOT NULL;') == ["M2"]
    assert rules('ALTER TABLE "E" ADD COLUMN "at" TIMESTAMP NOT NULL DEFAULT clock_timestamp();') == ["M2"]
    assert rules('ALTER TABLE "User" ALTER COLUMN "age" SET DATA TYPE BIGINT;') == ["M1"]
    print("self-test OK")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # console Windows mặc định cp1252
    if "--self-test" in sys.argv:
        self_test()
    else:
        sys.exit(main(sys.argv[1:]))
