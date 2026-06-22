#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将实现定位表转为 HTML 表格，固定列宽、表内语义高亮并写入表头行。

表内高亮（GitHub 可用 inline style）：
  - 所属层名 / 相关概念 / 链中位置 / 总IO / ③④⑤ / 步骤号 / 问·答
  - 反引号代码 → 灰底 code；Markdown 链接 → 蓝色 a

用法：python scripts/format_impl_tables.py [01路径] [02路径...]
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DOCS = [
    ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md",
    ROOT / "docs" / "09-理解与讲解" / "02-答辩讲解手册.md",
]

THREE_COL_HEADERS = ["所属层", "链路中位置与代码地址", "实现讲解"]
FOUR_COL_HEADERS = ["概念", "实例", "链路中位置与代码地址", "实现讲解"]

TABLE_STYLE = (
    'class="impl-loc-table" '
    'style="table-layout:fixed;width:100%;border-collapse:collapse;border:1px solid #d0d7de;"'
)

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

TH_STYLE = (
    'style="text-align:left;vertical-align:bottom;padding:8px 10px;'
    'border:1px solid #d0d7de;background:#f6f8fa;font-weight:700;"'
)

TD_BASE = "vertical-align:top;word-break:break-word;padding:10px 12px;border:1px solid #d0d7de;line-height:1.65;"
TD_PRINCIPLE = TD_BASE.replace("line-height:1.65;", "line-height:1.72;")

BR2 = "<br><br>"

# 语义色（浅底 + 深字，GitHub 亮色系可读）
S = {
    "layer": "color:#6639ba;font-weight:700;",
    "label": "color:#0969da;font-weight:700;",
    "io": "color:#953800;font-weight:600;",
    "total": "color:#bc4c00;font-weight:700;",
    "step": "color:#1a7f37;font-weight:700;background:#ddf4ff;padding:1px 6px;border-radius:4px;",
    "sec3": "color:#0550ae;font-weight:700;background:#dbeafe;padding:2px 8px;border-radius:4px;",
    "sec4": "color:#7c3aed;font-weight:700;background:#ede9fe;padding:2px 8px;border-radius:4px;",
    "sec5": "color:#b45309;font-weight:700;background:#ffedd5;padding:2px 8px;border-radius:4px;",
    "ask": "color:#cf222e;font-weight:700;",
    "ans": "color:#0969da;font-weight:600;",
    "link": "color:#0969da;text-decoration:none;",
    "code_bg": "background:#eff1f3;padding:1px 5px;border-radius:4px;font-size:92%;",
}


def _span(style_key: str, text: str) -> str:
    return f'<span style="{S[style_key]}">{text}</span>'


def ensure_structure_breaks(text: str) -> str:
    """扁平 Markdown 表单元格补回 <br> 结构。"""
    if re.search(r"<br\s*/?>", text, flags=re.I):
        return text
    t = text.strip()
    t = re.sub(r"\s+(相关概念：)", r"<br>\1", t, count=1)
    t = re.sub(r"\s+(链中位置：)", r"<br>\1", t, count=1)
    t = re.sub(r"\s+(总输入：)", r"<br>\1", t)
    t = re.sub(r"\s+(总输出：)", r"<br>\1", t)
    t = re.sub(r"\s+(失败时：)", r"<br>\1", t)
    t = re.sub(r"\s+(③\s*底层实现：)", r"<br><br>\1", t)
    t = re.sub(r"\s+(④\s*设计取舍：)", r"<br><br>\1", t)
    t = re.sub(r"\s+(⑤\s*答辩要点：)", r"<br><br>\1", t)
    t = re.sub(r"(?<![\d/L])(?<!\d)\s+(\d+\.\s)", r"<br>\1", t)
    t = re.sub(
        r"((?:\d+\.\s[^<]+?))\s+(输入：)",
        lambda m: f"{m.group(1)}<br>&nbsp;&nbsp;&nbsp;{m.group(2)}",
        t,
    )
    t = re.sub(
        r"(&nbsp;&nbsp;&nbsp;输入：[^<]+?)\s+(输出：)",
        lambda m: f"{m.group(1)}<br>&nbsp;&nbsp;&nbsp;{m.group(2)}",
        t,
    )
    t = re.sub(r"(?<=[。；])\s+(\d+（L\d+)", r"<br>\1", t)
    t = re.sub(r"(\S)\s+(\d+（L\d+)", r"\1<br>\2", t)
    return t


def relax_cell_spacing(text: str, col_idx: int, n_cols: int) -> str:
    """表内增加换行与段间距，减轻拥挤感。"""
    t = text
    if col_idx == 0:
        t = re.sub(r"；(?=`)", "<br>", t)
        t = re.sub(r"；(?=[^`<])", "<br>", t)
    if col_idx == 1:
        t = re.sub(r"(输出：[^<]+)<br>(?=\d+\.)", rf"\1{BR2}", t)
        t = re.sub(r"(输出：[^<]+)<br>(?=总输入：)", rf"\1{BR2}", t)
    if col_idx == n_cols - 1:
        t = re.sub(r"(③ 底层实现：)\s*(\d+（L|\d+：)", r"\1<br>\2", t)
        t = re.sub(r"(?<!<br>)(?<!<br><br>)问：", f"{BR2}问：", t)
        t = re.sub(r"。<br>若不这样做：", f"。{BR2}若不这样做：", t)
    t = re.sub(r"(<br\s*/?>){3,}", BR2, t, flags=re.I)
    return t


def _md_links_and_code(segment: str) -> str:
    """转义纯文本，保留已生成 span/a/code。"""

    def link_repl(m: re.Match[str]) -> str:
        label, url = m.group(1), m.group(2)
        lab = html.escape(label, quote=True)
        u = html.escape(url, quote=True)
        return f'<a href="{u}" style="{S["link"]}">{lab}</a>'

    def code_repl(m: re.Match[str]) -> str:
        inner = html.escape(m.group(1), quote=False)
        return f'<code style="{S["code_bg"]}">{inner}</code>'

    # 先占位已有 HTML 标签
    placeholders: list[str] = []

    def stash(m: re.Match[str]) -> str:
        placeholders.append(m.group(0))
        return f"\x00H{len(placeholders) - 1}\x00"

    seg = re.sub(r"<(?:span|a|code|br)[^>]*>.*?</(?:span|a|code)>|<br\s*/?>", stash, segment, flags=re.I)
    seg = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, seg)
    seg = re.sub(r"`([^`]+)`", code_repl, seg)
    seg = html.escape(seg, quote=False)
    seg = seg.replace("&lt;br&gt;", "<br>").replace("&lt;br/&gt;", "<br/>").replace("&lt;br /&gt;", "<br />")
    for i, ph in enumerate(placeholders):
        seg = seg.replace(f"\x00H{i}\x00", ph)
    return seg


def highlight_segment(segment: str, col_idx: int, n_cols: int) -> str:
    s = segment.strip()
    if not s:
        return s

    # 所属层 · 相关概念（同段）
    if col_idx == 0 and "相关概念：" in s and "<span" not in s:
        layer, rest = s.split("相关概念：", 1)
        layer = layer.strip()
        layer_html = _span("layer", html.escape(layer, quote=False)) if layer else ""
        return (
            layer_html
            + (_md_links_and_code("<br>") if layer_html else "")
            + _span("label", "相关概念：")
            + _md_links_and_code(rest)
        )

    if col_idx == 0 and s.startswith("相关概念："):
        return _span("label", "相关概念：") + _md_links_and_code(s[len("相关概念：") :])

    # 所属层名单独一行
    if col_idx == 0 and "相关概念" not in s and re.match(
        r"^[\w\u4e00-\u9fff\s·/]+$", s
    ):
        return _span("layer", html.escape(s, quote=False))

    # 链中位置 / 总 IO
    for prefix, key in (
        ("链中位置：", "label"),
        ("总输入：", "total"),
        ("总输出：", "total"),
        ("失败时：", "total"),
    ):
        if s.startswith(prefix):
            body = s[len(prefix) :]
            return _span(key, prefix) + _md_links_and_code(body)

    # 步骤 输入 / 输出（缩进）
    if s.startswith("输入："):
        return _span("io", "输入：") + _md_links_and_code(s[3:])
    if s.startswith("输出："):
        return _span("io", "输出：") + _md_links_and_code(s[3:])

    # 步骤行 1. xxx
    m = re.match(r"^(\d+\.\s)(.+)$", s)
    if m and col_idx == 1:
        return _span("step", m.group(1)) + _md_links_and_code(m.group(2))

    # ③④⑤ 段标题（③ 后可能紧跟 1（Lx））
    if s.startswith("③ 底层实现："):
        rest = s[len("③ 底层实现：") :]
        m = re.match(r"^(\d+（L\d+[–\-—]L?\d*）：)(.*)$", rest, re.S)
        if m:
            return (
                _span("sec3", "③ 底层实现：")
                + _span("step", m.group(1))
                + _md_links_and_code(m.group(2))
            )
        return _span("sec3", "③ 底层实现：") + _md_links_and_code(rest)
    for prefix, key in (
        ("④ 设计取舍：", "sec4"),
        ("⑤ 答辩要点：", "sec5"),
    ):
        if s.startswith(prefix):
            body = s[len(prefix) :]
            return _span(key, prefix) + _md_links_and_code(body)

    # 底层实现分步 1（Lx–Ly）：
    m = re.match(r"^(\d+（L\d+[–\-—]L?\d*）：)(.+)$", s)
    if m:
        return _span("step", m.group(1)) + _md_links_and_code(m.group(2))

    # 问 / 答（答辩列）
    if col_idx == n_cols - 1:
        if s.startswith("问："):
            rest = s[2:]
            if "答：" in rest:
                q, a = rest.split("答：", 1)
                return (
                    _span("ask", "问：")
                    + _md_links_and_code(q)
                    + _span("ans", "答：")
                    + _md_links_and_code(a)
                )
            return _span("ask", "问：") + _md_links_and_code(rest)

    return _md_links_and_code(s)


def dedupe_locate_cell(text: str) -> str:
    """去掉「代码头 + 扁平链路 + 结构化链路」中的重复段。"""
    if text.count("链中位置：") <= 1:
        return text
    first = text.find("链中位置：")
    last = text.rfind("链中位置：")
    if first == last:
        return text
    header = text[:first].strip()
    body = text[last:]
    if "<br>" in body.lower() or "<span" in body:
        sep = "<br>" if header and not header.endswith("<br>") else ""
        return f"{header}{sep}{body}"
    return text


def rich_cell(text: str, col_idx: int, n_cols: int) -> str:
    t = text.strip()
    if col_idx == 1:
        t = dedupe_locate_cell(t)
    t = ensure_structure_breaks(t)
    t = relax_cell_spacing(t, col_idx, n_cols)
    parts = re.split(r"(<br\s*/?>)", t, flags=re.I)
    out: list[str] = []
    for p in parts:
        if re.fullmatch(r"<br\s*/?>", p, flags=re.I):
            out.append("<br>")
        else:
            out.append(highlight_segment(p, col_idx, n_cols))
    return "".join(out)


def is_header_cells(cells: list[str]) -> bool:
    joined = " ".join(cells)
    return any(
        k in joined
        for k in ("所属层", "Layer", "代码位置", "实现讲解", "原理 Principle", "概念 Concept", "路径 Path")
    )


def rows_to_html(rows: list[list[str]], headers: list[str], colgroup: str) -> str:
    n = len(headers)
    lines = [f"<table {TABLE_STYLE}>", colgroup, "  <thead>", "    <tr>"]
    for h in headers:
        lines.append(f'      <th scope="col" {TH_STYLE}>{html.escape(h)}</th>')
    lines.extend(["    </tr>", "  </thead>", "  <tbody>"])
    for ri, cells in enumerate(rows):
        padded = (cells + [""] * n)[:n]
        bg = ' style="background:#f6f8fa;"' if ri % 2 == 1 else ""
        lines.append(f"    <tr{bg}>")
        for i, c in enumerate(padded):
            st = TD_PRINCIPLE if i == n - 1 else TD_BASE
            lines.append(f'      <td style="{st}">{rich_cell(c, i, n)}</td>')
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
    if not s.startswith("|") or "所属层" not in s:
        return False
    has_loc = "链路中位置" in s or "定位" in s or "代码地址" in s
    has_prin = "实现讲解" in s or "原理" in s
    return has_loc and has_prin


def is_four_col_header(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and "概念" in s and ("实例" in s or "Concept" in s)


def extract_html_table_rows(html: str) -> list[list[str]]:
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


def strip_html_to_plain(cell: str) -> str:
    """从旧 HTML 单元格还原为可重新高亮的纯文本（保留 <br>）。"""
    c = cell
    c = re.sub(r"<br\s*/?>", "<br>", c, flags=re.I)
    c = re.sub(r"<a[^>]+href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", c, flags=re.I | re.S)
    c = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", c, flags=re.I | re.S)
    c = re.sub(r"<span[^>]*>(.*?)</span>", r"\1", c, flags=re.I | re.S)
    c = html.unescape(c)
    return c.strip()


def rebuild_html_block(html: str) -> str:
    rows = extract_html_table_rows(html)
    if not rows:
        return html
    plain = [[strip_html_to_plain(c) for c in row] for row in rows]
    ncols = max(len(r) for r in plain)
    if ncols >= 4:
        return rows_to_html([r[:4] for r in plain], FOUR_COL_HEADERS, FOUR_COL_GROUP)
    return rows_to_html([r[:3] for r in plain], THREE_COL_HEADERS, THREE_COL_GROUP)


def convert_doc(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    changed = 0
    while i < len(lines):
        line = lines[i]
        if is_three_col_header(line):
            i += 1
            if i < len(lines) and re.match(r"^\|\s*[-:| ]+\|\s*$", lines[i].strip()):
                i += 1
            rows: list[list[str]] = []
            while i < len(lines):
                row = parse_md_row(lines[i])
                if row is None:
                    break
                if len(row) >= 3 and not is_header_cells(row):
                    rows.append(row[:3])
                i += 1
            if rows:
                out.append(rows_to_html(rows, THREE_COL_HEADERS, THREE_COL_GROUP))
                changed += 1
            continue
        if is_four_col_header(line):
            i += 1
            if i < len(lines) and re.match(r"^\|\s*[-:| ]+\|\s*$", lines[i].strip()):
                i += 1
            rows = []
            while i < len(lines):
                row = parse_md_row(lines[i])
                if row is None:
                    break
                if len(row) >= 4 and not is_header_cells(row):
                    rows.append(row[:4])
                i += 1
            if rows:
                out.append(rows_to_html(rows, FOUR_COL_HEADERS, FOUR_COL_GROUP))
                changed += 1
            continue
        if "impl-loc-table" in line and line.strip().startswith("<table"):
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
