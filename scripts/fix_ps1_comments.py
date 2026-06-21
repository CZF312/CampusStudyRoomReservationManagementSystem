#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove invalid // 【行】 suffixes from PowerShell scripts (// is not valid in PS)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAT = re.compile(r"\s*// 【行】[^\n\r]*")

for p in ROOT.rglob("*.ps1"):
    if "node_modules" in p.parts:
        continue
    text = p.read_text(encoding="utf-8")
    new = PAT.sub("", text)
    if new != text:
        p.write_text(new, encoding="utf-8")
        print(f"fixed {p.relative_to(ROOT)}")
