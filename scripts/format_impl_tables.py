#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将实现定位表转为 HTML 表格，固定列宽并写入表头行：
  三列：所属层 8% · 代码位置 22% · 实现讲解 70%
  四列（F1.2）：12% · 18% · 22% · 48%

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

THREE_COL_HEADER_MD = "| 所属层 Layer | 定位（函数 · 路径 · 行号） | 原理 Principle |"
FOUR_COL_HEADER_MD = "| 概念 Concept | 实例 | 路径 Path（英 · 中）· 行号 | 原理 Principle |"

THREE_COL_HEADERS = ["所属层", "链路中位置与代码地址", "实现讲解"]
FOUR_COL_HEADERS = ["概念", "实例", "链路中位置与代码地址", "实现讲解"]

TABLE_STYLE = 'style="table-layout:fixed;width:100%;border-collapse:collapse;"'

THREE_COL_GROUP = """<colgroup>
  <col style="width:18%" />
  <col style="width:28%" />
  <col style="width:54%" />
</colgroup>"""

FOUR_COL_GROUP = """<colgroup>
  <col style="width:14%" />
  <col style="width:12%" />
  <col style="width:26%" />
  <col style="width:48%" />
</colgroup>"""

CELL_LEFT = 'style="vertical-align:top;word-break:break-word;"'
CELL_PRINCIPLE = 'style="vertical-align:top;word-break:break-word;line-height:1.45;"'
TH_STYLE = 'style="text-align:left;vertical-align:bottom;padding:6px 8px;border-bottom:1px solid #ccc;"'


def esc_cell(text: str) -> str:
    t = text.strip()
    parts = re.split(r"(<br\s*/?>)", t, flags=re.I)
    out: list[str] = []
    for p in parts:
        if re.fullmatch(r"<br\s*/?>", p, flags=re.I):
            out.append(p)
        else:
            s = p
            if "&amp;" not in s and "&lt;" not in s and "&gt;" not in s:
                s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            out.append(s)
    return "".join(out)


def is_header_cells(cells: list[str]) -> bool:
    joined = " ".join(cells)
    return any(
        k in joined
        for k in ("所属层", "Layer", "代码位置", "实现讲解", "原理 Principle", "概念 Concept", "路径 Path")
    )


def rows_to_html(rows: list[list[str]], headers: list[str], colgroup: str) -> str:
    n = len(headers)
    lines = [
        f'<table class="impl-loc-table" {TABLE_STYLE}>',
        colgroup,
        "  <thead>",
        "    <tr>",
    ]
    for h in headers:
        lines.append(f'      <th scope="col" {TH_STYLE}>{esc_cell(h)}</th>')
    lines.extend(["    </tr>", "  </thead>", "  <tbody>"])
    for cells in rows:
        padded = (cells + [""] * n)[:n]
        lines.append("    <tr>")
        for i, c in enumerate(padded):
            st = CELL_PRINCIPLE if i == n - 1 else CELL_LEFT
            lines.append(f'      <td {st}>{esc_cell(c)}</td>')
        lines.append("    </tr>")
    lines.extend(["  </tbody>", "</table>", ""])
    return "\n".join(lines)


def parse_md_row(line: str) -> list[str] | None:
    if not line.startswith("|") or "---" in line:
        return None
    parts = [p.strip() for p in line.split("|")]
    cells = parts[1:-1] if parts and parts[-1] == "" else parts[1:]
    if not cells or all(not c for c in cells) or cells[0].startswith("-"):
        return None
    return cells


def is_three_col_header(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and "所属层" in s and "原理" in s and "定位" in s


def is_four_col_header(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and "概念 Concept" in s and "原理 Principle" in s


def extract_html_table_rows(html: str) -> list[list[str]]:
    """从已有 impl-loc-table 提取 tbody 数据行（跳过表头行）。"""
    rows: list[list[str]] = []
    for tr in re.finditer(r"<tr[^>]*>(.*?)</tr>", html, flags=re.I | re.DOTALL):
        inner = tr.group(1)
        if re.search(r"<th[\s>]", inner, flags=re.I):
            continue
        cells = re.findall(r"<td[^>]*>(.*?)</td>", inner, flags=re.I | re.DOTALL)
        if not cells:
            continue
        cells = [re.sub(r"\s+", " ", c.strip()) for c in cells]
        if is_header_cells(cells):
            continue
        rows.append(cells)
    return rows


def rebuild_html_block(html: str) -> str:
    rows = extract_html_table_rows(html)
    if not rows:
        return html
    ncols = max(len(r) for r in rows)
    if ncols >= 4:
        return rows_to_html([r[:4] for r in rows], FOUR_COL_HEADERS, FOUR_COL_GROUP)
    return rows_to_html([r[:3] for r in rows], THREE_COL_HEADERS, THREE_COL_GROUP)


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
                row = parse_md_row(lines[i])
                if row is None:
                    break
                if len(row) >= 3:
                    rows.append(row[:3])
                i += 1
            if rows:
                out.append(rows_to_html(rows, THREE_COL_HEADERS, THREE_COL_GROUP))
                changed += 1
            continue
        if is_four_col_header(line):
            i += 1
            if i < len(lines) and "---" in lines[i]:
                i += 1
            rows = []
            while i < len(lines):
                row = parse_md_row(lines[i])
                if row is None:
                    break
                if len(row) >= 4:
                    rows.append(row[:4])
                i += 1
            if rows:
                out.append(rows_to_html(rows, FOUR_COL_HEADERS, FOUR_COL_GROUP))
                changed += 1
            continue
        if line.strip().startswith('<table class="impl-loc-table"'):
            block = [line]
            i += 1
            while i < len(lines) and "</table>" not in lines[i]:
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append(lines[i])
            out.append(rebuild_html_block("\n".join(block)))
            changed += 1
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
        print(f"{path.name}: formatted {n} tables")
        total += n
    print(f"done, {total} tables total")


if __name__ == "__main__":
    main()
