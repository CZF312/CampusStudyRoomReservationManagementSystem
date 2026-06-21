#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将实现定位表从 Markdown 等宽三列改为 HTML 表格，按内容比例分配列宽：
  所属层 ~11% · 定位 ~27% · 原理 ~62%（F1.2 四列：12/18/22/48）

用法：python scripts/format_impl_tables.py [01路径] [02路径...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCS = [
    ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md",
    ROOT / "docs" / "09-理解与讲解" / "02-答辩讲解手册.md",
]

THREE_COL_HEADER = "| 所属层 Layer | 定位（函数 · 路径 · 行号） | 原理 Principle |"
FOUR_COL_HEADER = "| 概念 Concept | 实例 | 路径 Path（英 · 中）· 行号 | 原理 Principle |"

THREE_COL_GROUP = """<colgroup>
  <col width="11%" />
  <col width="27%" />
  <col width="62%" />
</colgroup>"""

FOUR_COL_GROUP = """<colgroup>
  <col width="12%" />
  <col width="18%" />
  <col width="22%" />
  <col width="48%" />
</colgroup>"""


def esc_cell(text: str) -> str:
    t = text.strip()
    parts = re.split(r"(<br\s*/?>)", t, flags=re.I)
    out: list[str] = []
    for p in parts:
        if re.fullmatch(r"<br\s*/?>", p, flags=re.I):
            out.append(p)
        else:
            out.append(p.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return "".join(out)


def is_three_col_header(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and "所属层 Layer" in s and "原理 Principle" in s and "定位" in s


def is_four_col_header(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and "概念 Concept" in s and "原理 Principle" in s and "路径 Path" in s


def parse_row(line: str) -> list[str] | None:
    if not line.startswith("|") or "---" in line:
        return None
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 3:
        return None
    cells = parts[1:-1] if parts[-1] == "" else parts[1:]
    if not cells or all(not c for c in cells):
        return None
    if cells[0].startswith("-"):
        return None
    return cells


def rows_to_html(rows: list[list[str]], colgroup: str) -> str:
    lines = [
        '<table class="impl-loc-table">',
        colgroup,
        "  <tbody>",
    ]
    for cells in rows:
        lines.append("    <tr>")
        for c in cells:
            lines.append(f"      <td>{esc_cell(c)}</td>")
        lines.append("    </tr>")
    lines.extend(["  </tbody>", "</table>", ""])
    return "\n".join(lines)


def convert_doc(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    changed = 0
    while i < len(lines):
        line = lines[i]
        if is_three_col_header(line):
            i += 1
            if i < len(lines) and "---" in lines[i]:
                i += 1
            rows: list[list[str]] = []
            while i < len(lines):
                row = parse_row(lines[i])
                if row is None:
                    break
                if len(row) >= 3:
                    rows.append(row[:3])
                i += 1
            if rows:
                out.append(rows_to_html(rows, THREE_COL_GROUP))
                changed += 1
            continue
        if is_four_col_header(line):
            i += 1
            if i < len(lines) and "---" in lines[i]:
                i += 1
            rows = []
            while i < len(lines):
                row = parse_row(lines[i])
                if row is None:
                    break
                if len(row) >= 4:
                    rows.append(row[:4])
                i += 1
            if rows:
                out.append(rows_to_html(rows, FOUR_COL_GROUP))
                changed += 1
            continue
        if line.strip().startswith("<table class=\"impl-loc-table\">"):
            while i < len(lines) and "</table>" not in lines[i]:
                i += 1
            if i < len(lines):
                i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out) + "\n", changed


def main() -> None:
    paths = [Path(p) for p in sys.argv[1:]] if len(sys.argv) > 1 else DEFAULT_DOCS
    total = 0
    for path in paths:
        if not path.is_file():
            print(f"skip missing {path}")
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = convert_doc(text)
        path.write_text(new_text, encoding="utf-8")
        print(f"{path.name}: converted {n} tables")
        total += n
    print(f"done, {total} tables total")


if __name__ == "__main__":
    main()
