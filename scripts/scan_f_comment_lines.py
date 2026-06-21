#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描源码中 【Fx-y】 注释行号，供更新 01 文档链接。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = {".java", ".vue", ".js", ".sql", ".html", ".bat", ".ps1"}

def main() -> None:
    pat = re.compile(r"【(F\d+-\d+)[^】]*】")
    for p in sorted(ROOT.rglob("*")):
        if p.suffix.lower() not in EXT:
            continue
        if "node_modules" in p.parts or "target" in p.parts:
            continue
        try:
            lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        rel = p.relative_to(ROOT).as_posix()
        for i, line in enumerate(lines, 1):
            m = pat.search(line)
            if m:
                print(f"{m.group(1):8}  {rel}:{i}  {line.strip()[:100]}")

if __name__ == "__main__":
    main()
