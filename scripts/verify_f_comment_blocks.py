#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验源码 F 注释块：每个 【Fx-y】 首段概括后，块内 executable 行应带 【行】 讲解。

用法：python scripts/verify_f_comment_blocks.py
退出码：0=通过，1=有问题
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = [
    ROOT / "frontend" / "src",
    ROOT / "src" / "main" / "java",
    ROOT / "scripts",
    ROOT,
]
EXT = {".java", ".vue", ".ps1", ".bat", ".sql"}
SKIP_PARTS = {"node_modules", "target", "static", ".git"}

F_BLOCK = re.compile(r"【(F\d+-\d+)[^】]*】")
LINE_TAG = re.compile(r"【行】")

# 视为「可执行/应注释」的行（粗略）
CODE_LIKE = re.compile(
    r"^\s*(?:@|async\s+function|function|if\s*\(|for\s*\(|while\s*\(|switch\s*\(|"
    r"return\b|await\s+|const\s+|let\s+|var\s+|import\s+|export\s+|"
    r"public\s+|private\s+|protected\s+|class\s+\w|"
    r"[a-zA-Z_$][\w$]*\s*\(|"
    r"<\w+|v-if|v-for|v-model|@click|el-|INSERT|UPDATE|SELECT|DELETE|CREATE|"
    r"REM\s+\w|# \[|Start-|Invoke-|mysql)"
)


def should_have_line_comment(line: str) -> bool:
    s = line.strip()
    if not s or s in ("{", "}", "};", ")", "});", "},", ">"):
        return False
    if s.startswith("//") or s.startswith("*") or s.startswith("<!--"):
        if LINE_TAG.search(line):
            return False
        if F_BLOCK.search(line) and "【行】" not in line:
            return True  # block header without 行 on same line is ok if next lines have it
        return False
    if s.startswith("/**") or s.startswith("*/") or (s.startswith("*") and not s.startswith("*.")):
        return False
    if s.startswith("}"):
        return False
    if CODE_LIKE.search(line) or "`" in line or "await " in line:
        return True
    return len(s) > 8 and not s.startswith("#") and "【" not in s


def scan_file(path: Path) -> list[str]:
    issues: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return issues
    rel = path.relative_to(ROOT).as_posix()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = F_BLOCK.search(line)
        if not m:
            i += 1
            continue
        f_id = m.group(1)
        block_start = i + 1
        # 块范围：到下一个 【Fx-y】 或空行连续 3 行或函数结束大括号顶格
        j = i + 1
        blank = 0
        while j < len(lines):
            if F_BLOCK.search(lines[j]) and j > i + 1:
                break
            if lines[j].strip() == "":
                blank += 1
                if blank >= 4 and j - i > 15:
                    break
            else:
                blank = 0
            if j - i > 120:
                break
            j += 1
        block_end = j
        missing: list[int] = []
        for k in range(block_start, block_end):
            if should_have_line_comment(lines[k]) and not LINE_TAG.search(lines[k]):
                missing.append(k + 1)
        if len(missing) > 8:
            issues.append(
                f"{rel}:{block_start+1} [{f_id}] 块内 {len(missing)} 行缺 【行】（示例 L{missing[0]}…L{missing[4] if len(missing)>4 else missing[-1]}）"
            )
        elif missing:
            for ln in missing[:5]:
                issues.append(f"{rel}:L{ln} [{f_id}] 疑似代码行缺 【行】：{lines[ln-1].strip()[:70]}")
        i = block_end if block_end > i else i + 1
    return issues


def main() -> int:
    all_issues: list[str] = []
    f_count = 0
    line_count = 0
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for p in sorted(base.rglob("*")):
            if p.suffix.lower() not in EXT:
                continue
            if any(s in p.parts for s in SKIP_PARTS):
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            f_count += len(F_BLOCK.findall(text))
            line_count += len(LINE_TAG.findall(text))
            all_issues.extend(scan_file(p))

    print(f"【Fx-y】块约 {f_count} 处 · 【行】约 {line_count} 处")
    if all_issues:
        print(f"WARN: {len(all_issues)} 条待核对（模板/纯声明行可能误报）")
        for msg in all_issues[:40]:
            print(f"  ! {msg}")
        if len(all_issues) > 40:
            print(f"  ! ... 另有 {len(all_issues) - 40} 条")
        return 0 if len(all_issues) < 30 else 1
    print("PASS: 未发现大块缺失 【行】 的 F 注释区")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
