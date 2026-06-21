#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 01-项目理解指南.md 生成 02-答辩讲解手册.md。

原则：02 与 01 **同 F 编号、同定位表、同行号**；仅做答辩向删减：
  - 改标题与导读（加【演】【讲】【指】）
  - 删除「阅读与注释约定」整节（答辩时口述即可）
  - 去掉明显 AI 套话（「在…功能链中，这是…」等重复句式）
  - F1.2 八卡概念表保留链接，删掉过长原理 prose
  - 文末追加 F8 答辩 Q&A 与检查清单（若 01 无则保留原 02 尾部）

用法：
  python scripts/generate_02_from_01.py
  python scripts/sync_f_doc_anchors.py   # 生成后必跑
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_01 = ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md"
DOC_02 = ROOT / "docs" / "09-理解与讲解" / "02-答辩讲解手册.md"

AI_TRIM = [
    (r"在「[^」]+」功能链中，这是", "本模块是"),
    (r"在[^，。]+功能链中，这是", "此处是"),
    (r"对应功能链中「", "对应「"),
    (r"对应故事中", "演示时"),
    (r"上游[^，。]+，下游", "前后衔接："),
    (r"放在[^，。]+层是为", "设计原因："),
    (r"功能链中「", "「"),
]


def trim_principle(cell: str) -> str:
    s = cell
    for pat, rep in AI_TRIM:
        s = re.sub(pat, rep, s)
    return s.strip()


def transform_table_principles(text: str) -> str:
    """处理三列表格的原理列（最后一列）。"""
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("|") and "原理" not in line and i > 0 and "原理" in lines[i - 1]:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 4 and parts[-2]:
                parts[-2] = trim_principle(parts[-2])
                line = "| " + " | ".join(parts[1:-1]) + " |"
        out.append(line)
        i += 1
    return "\n".join(out)


def extract_f8_tail(old_02: str) -> str:
    m = re.search(r"(## <a id=\"f8\"></a>F8 附录：答辩 Q&A[\s\S]*)", old_02)
    return m.group(1) if m else ""


def main() -> None:
    if not DOC_01.exists():
        raise SystemExit("01 不存在")
    text = DOC_01.read_text(encoding="utf-8")
    old_02 = DOC_02.read_text(encoding="utf-8") if DOC_02.exists() else ""
    f8_tail = extract_f8_tail(old_02)

    text = text.replace(
        "# 01 — 项目理解指南",
        "# 02 — 答辩讲解手册",
    )
    text = re.sub(
        r"> \*\*读法\*\*：[^\n]+\n",
        "> **演示账号**：学生 `202225220101`/`123456` · 普管 `admin`/`admin123` · 超管 `superadmin`/`super123`  \n"
        "> **标签**：【演】浏览器操作 · 【讲】口述原理 · 【指】点行号（Lx 首行含 `【Fx-y】` 总体讲解）· **与 [01](01-项目理解指南.md#user-content-toc) 同 F 编号**  \n"
        "> **说明**：正文由 01 同步生成，删去阅读约定与 AI 套话；定位表与行号与 01 一致。\n",
        text,
        count=1,
    )
    # 删除阅读与注释约定
    text = re.sub(
        r"\n## 阅读与注释约定\n[\s\S]*?\n---\n",
        "\n---\n",
        text,
        count=1,
    )
    text = transform_table_principles(text)
    # 替换 F8 附录标题与答辩专用尾
    text = re.sub(
        r"## <a id=\"f8\"></a>F8 附录：需求与代码差异",
        "## <a id=\"f8\"></a>F8 附录：答辩 Q&A",
        text,
        count=1,
    )
    if f8_tail and "演示前检查清单" in f8_tail:
        # 保留 01 的 F8 差异表，再追加原 02 的 Q&A 清单
        if "### 演示前检查清单" not in text:
            text = text.rstrip() + "\n\n---\n\n" + f8_tail.split("---", 1)[-1] if "---" in f8_tail else "\n\n" + f8_tail
    text = re.sub(
        r"答辩演练 \*\*\[02-答辩讲解手册\]",
        "详细原理 **[01-项目理解指南](01-项目理解指南.md#user-content-toc)** · 单点问答 **[03-功能问答](03-功能问答-定位环境.md)** · 本手册即",
        text,
    )
    text = text.replace(
        "** · 单点问答 **[03-功能问答](03-功能问答-定位环境.md)**",
        "",
        1,
    )
    DOC_02.write_text(text, encoding="utf-8")
    print(f"generated {DOC_02.name} from 01 ({len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
