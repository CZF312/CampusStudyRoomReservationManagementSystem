#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将 09-理解与讲解 中 file:/// 本地链接转为 GitHub blob 链接（便于组长在线点开代码行）。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_DIR = ROOT / "docs" / "09-理解与讲解"
REPO = "https://github.com/CZF312/CampusStudyRoomReservationManagementSystem/blob/master"
LOCAL_PREFIX = re.compile(
    r"file:///d:/SchoolWorkPlace/Database/CampusStudyRoomReservationManagementSystem-master/",
    re.I,
)


def convert(text: str) -> str:
    return LOCAL_PREFIX.sub(f"{REPO}/", text)


def main() -> None:
    for path in sorted(DOC_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        new = convert(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print(f"converted: {path.name}")


if __name__ == "__main__":
    main()
