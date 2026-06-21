#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 01 实现定位表中「原理 Principle」列统一为结构化详解（若尚未含 **链中位置**）。

用法：python scripts/expand_doc_principles.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md"


def expand_cell(principle: str) -> str:
    p = principle.strip()
    if not p or "**链中位置**" in p:
        return p
    # 按句号拆句
    parts = [s.strip() for s in re.split(r"(?<=[。；])", p) if s.strip()]
    if len(parts) <= 1:
        return (
            f"**链中位置**：{p} "
            f"**注释导读**：跳转首行为 `【Fx-y】` 总体讲解，块内每行带 `【行】` 中文注释。"
        )
    labels = ["**链中位置**", "**输入输出**", "**上下游**", "**设计原因**", "**注释导读**"]
    out = []
    for i, part in enumerate(parts[:5]):
        label = labels[min(i, len(labels) - 1)]
        if i >= len(labels) - 1 and i < len(parts) - 1:
            part = "；".join(parts[i:])
        out.append(f"{label}：{part}")
        if i >= len(labels) - 1:
            break
    if len(parts) > 5:
        out.append(f"**补充**：{'；'.join(parts[5:])}")
    return " ".join(out)


def main() -> None:
    lines = DOC.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    in_table = False
    changed = 0
    for i, line in enumerate(lines):
        if line.startswith("| 所属层") or line.startswith("| 概念 Concept"):
            in_table = True
            out.append(line)
            continue
        if in_table and line.startswith("|") and "---" not in line:
            parts = line.split("|")
            if len(parts) >= 4:
                # 最后一列是原理
                principle_idx = -2
                old = parts[principle_idx].strip()
                new = expand_cell(old)
                if new != old:
                    parts[principle_idx] = f" {new} "
                    changed += 1
                line = "|".join(parts)
            out.append(line)
            continue
        if in_table and not line.startswith("|"):
            in_table = False
        out.append(line)
    DOC.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"expanded {changed} principle cells")


if __name__ == "__main__":
    main()
