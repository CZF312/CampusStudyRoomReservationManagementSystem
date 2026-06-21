#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据源码中 【Fx-y】 注释与符号名，同步 01/02 文档里 GitHub blob 链接的 Lx-Ly。

策略：
  1. 扫描源码，建立 (文件, 函数名) -> (start,end) 与 【F】注释行 -> 块范围
  2. 解析 md 表格「定位」列中的 `函数名` 与 blob 链接
  3. 若本地能找到更准确行号，更新 [Lx-Ly] 文字与 URL #Lx-Ly

用法：
  python scripts/sync_github_line_anchors.py
  python scripts/sync_github_line_anchors.py --check   # 只报告漂移
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_FILES = [
    ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md",
    ROOT / "docs" / "09-理解与讲解" / "02-答辩讲解手册.md",
]
GITHUB_PREFIX = "https://github.com/CZF312/CampusStudyRoomReservationManagementSystem/blob/master/"
LINK_PAT = re.compile(
    r"\[(L\d+(?:-L\d+)?)\]\(" + re.escape(GITHUB_PREFIX) + r"([^)#]+)#L(\d+)(?:-L(\d+))?\)"
)
SYM_PAT = re.compile(
    r"`([a-zA-Z_][\w.]*)`|·\s*([a-zA-Z_][\w]*)\s*·"
)
F_MARK = re.compile(r"【(F\d+-\d+)·[^】]+】功能链实例：")


def scan_f_blocks() -> dict[tuple[str, str], tuple[int, int]]:
    """(repo_path, symbol_or_Fcode) -> (start_line, end_line)"""
    mapping: dict[tuple[str, str], tuple[int, int]] = {}
    ext = {".java", ".vue", ".js", ".bat", ".ps1", ".sql", ".html"}
    func_pat = re.compile(r"(?:async\s+)?function\s+(\w+)|(?:public|private|protected)\s+[\w<>,\s]+\s+(\w+)\s*\(")
    for p in ROOT.rglob("*"):
        if p.suffix.lower() not in ext:
            continue
        if "node_modules" in p.parts or "target" in p.parts:
            continue
        rel = p.relative_to(ROOT).as_posix()
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            fm = F_MARK.search(line)
            if fm:
                code = fm.group(1)
                end = min(i + 50, len(lines))
                for j in range(i, min(i + 120, len(lines))):
                    if j > i and F_MARK.search(lines[j - 1]):
                        end = j - 1
                        break
                mapping[(rel, code)] = (i, end)
            m = func_pat.search(line)
            if m:
                name = m.group(1) or m.group(2)
                start = i
                if "【行】" in line or F_MARK.search(line):
                    start = i
                elif i > 1 and (F_MARK.search(lines[i - 2]) or "【F" in lines[i - 2]):
                    start = i - 1
                end = start
                depth = 0
                for j in range(i - 1, min(i + 100, len(lines))):
                    depth += lines[j].count("{") - lines[j].count("}")
                    end = j + 1
                    if depth <= 0 and j >= i - 1 and "{" in "".join(lines[i - 1 : j + 1]):
                        break
                mapping[(rel, name)] = (start, end)
    return mapping


def find_range(rel_path: str, row_text: str, blocks: dict) -> tuple[int, int] | None:
    syms = set()
    for m in SYM_PAT.finditer(row_text):
        syms.add(m.group(1) or m.group(2))
    for m in re.finditer(r"【(F\d+-\d+)】", row_text):
        syms.add(m.group(1))
    for sym in syms:
        key = (rel_path, sym)
        if key in blocks:
            return blocks[key]
    return None


def update_doc(path: Path, blocks: dict, check_only: bool) -> int:
    text = path.read_text(encoding="utf-8")
    updates = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal updates
        display = m.group(1)
        rel = m.group(2)
        start = int(m.group(3))
        end = int(m.group(4) or m.group(3))
        row_start = max(0, m.start() - 200)
        row_ctx = text[row_start : m.end() + 50]
        found = find_range(rel, row_ctx, blocks)
        if not found:
            return m.group(0)
        ns, ne = found
        if ns == start and ne == end:
            return m.group(0)
        updates += 1
        new_disp = f"L{ns}" if ns == ne else f"L{ns}-L{ne}"
        if check_only:
            print(f"DRIFT {path.name}: {rel} {display} -> {new_disp} ({row_ctx[:60]}…)")
            return m.group(0)
        return f"[{new_disp}]({GITHUB_PREFIX}{rel}#L{ns}" + (f"-L{ne}" if ne != ns else "") + ")"

    new_text = LINK_PAT.sub(repl, text)
    if updates and not check_only:
        path.write_text(new_text, encoding="utf-8")
    return updates


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    blocks = scan_f_blocks()
    total = 0
    for doc in DOC_FILES:
        if doc.exists():
            total += update_doc(doc, blocks, args.check)
    print(f"{'checked' if args.check else 'updated'}: {total} link(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
