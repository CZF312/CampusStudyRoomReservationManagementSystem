#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将源码 【Fx-y·步骤N】实例： 迁移为 【Fx-y·子项】功能链实例：… 本处职责：…"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_01 = ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md"
EXT = {".java", ".vue", ".js", ".sql", ".html", ".bat", ".ps1"}

# F编号 -> 子项短名（用于注释）
SUB_NAMES = {
    "F1-1": "环境启动",
    "F1-2": "技术概念",
    "F2-1": "学生登录",
    "F2-2": "管理员登录",
    "F2-3": "注册审核",
    "F2-4": "账号资料与安全",
    "F3-1": "查座预约",
    "F3-2": "取消预约",
    "F3-3": "我的预约",
    "F4-1": "签到",
    "F4-2": "签退与信用",
    "F4-3": "定时维护",
    "F5-1": "学习统计",
    "F5-2": "公告与通知",
    "F5-3": "问题反馈",
    "F6-1": "统计与CSV",
    "F6-2": "系统配置",
    "F6-3": "用户管理",
    "F6-4": "自习室与座位",
    "F6-5": "预约监管",
    "F6-6": "运营看板",
    "F6-7": "管理员与日志",
    "F7-1": "DB与Java分工",
    "F7-2": "第三版规范化",
    "F7-3": "前端状态",
    "F7-4": "十六张表",
}

STORY_PAT = re.compile(
    r"### <a id=\"(?P<id>f\d+-\d+)\"></a>F[\d.]+\s+([^\n]+)\n\n\*\*功能链实例[^*]*\*\*\s*\n(.+?)\n\n####",
    re.DOTALL,
)


def load_stories() -> dict[str, str]:
    text = DOC_01.read_text(encoding="utf-8")
    stories: dict[str, str] = {}
    for m in STORY_PAT.finditer(text):
        fid = m.group(1).replace("f", "F").upper().replace("-", "-")
        # f5-1 -> F5-1
        key = "F" + m.group(1)[1:].replace("f", "").upper()
        key = re.sub(r"F(\d+)-(\d+)", lambda x: f"F{x.group(1)}-{x.group(2)}", "F" + m.group(1)[1:])
        body = re.sub(r"\s+", " ", m.group(3).strip())
        if len(body) > 120:
            body = body[:117] + "…"
        stories[key] = body
    # manual keys
    manual = {
        "F5-1": "小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图",
        "F6-1": "管理员打开统计页，切换当期/往期与报表类型，查看图表并导出 CSV",
    }
    stories.update(manual)
    return stories


OLD_PAT = re.compile(
    r"【(?P<code>F\d+-\d+)(?:·[^】]+)?】(?:实例：|步骤\d+[^】]*】实例：)?(?P<duty>[^】\n]+)"
)


def normalize_comment(code: str, duty: str, stories: dict[str, str]) -> str:
    sub = SUB_NAMES.get(code, code)
    story = stories.get(code, "见 01 项目理解指南对应节功能链实例")
    duty = duty.strip().lstrip("实例：").strip()
    if duty.startswith("功能链实例："):
        return f"【{code}·{sub}】{duty}"
    return f"【{code}·{sub}】功能链实例：{story} 本处职责：{duty}"


def migrate_line(line: str, stories: dict[str, str]) -> str:
    if "【F" not in line or "功能链实例：" in line:
        return line

    def repl(m: re.Match[str]) -> str:
        full = m.group(0)
        code = m.group("code")
        # 提取旧 duty：去掉 【F..】 前缀
        duty = full.split("】", 1)[-1]
        for prefix in ("实例：", "步骤", "·模板】实例："):
            if "步骤" in duty and "】" in duty:
                duty = duty.split("】", 1)[-1]
        duty = duty.replace("实例：", "", 1).strip()
        return normalize_comment(code, duty, stories)

    # 【F5-1·步骤0·模板】实例：xxx
    pat2 = re.compile(r"【(?P<code>F\d+-\d+)·[^】]*】实例：(?P<duty>[^\n*<]+)")
    line2, n = pat2.subn(lambda m: normalize_comment(m.group("code"), m.group("duty"), stories), line)
    if n:
        return line2

    pat3 = re.compile(r"【(?P<code>F\d+-\d+)·[^】]*】(?P<rest>[^\n*<]+)")
    if "实例：" in line and "【F" in line:
        m = pat3.search(line)
        if m and "功能链实例" not in line:
            rep = normalize_comment(m.group("code"), m.group("rest").replace("实例：", ""), stories)
            return pat3.sub(rep, line, count=1)
    return line


def main() -> None:
    stories = load_stories()
    changed_files = 0
    changed_lines = 0
    for p in sorted(ROOT.rglob("*")):
        if p.suffix.lower() not in EXT:
            continue
        if any(x in p.parts for x in ("node_modules", "target", ".git")):
            continue
        try:
            lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
        except OSError:
            continue
        new_lines = []
        file_changed = False
        for line in lines:
            nl = migrate_line(line, stories)
            if nl != line:
                file_changed = True
                changed_lines += 1
            new_lines.append(nl)
        if file_changed:
            p.write_text("".join(new_lines), encoding="utf-8")
            changed_files += 1
            print(f"updated {p.relative_to(ROOT)}")
    print(f"done: {changed_files} files, {changed_lines} lines")


if __name__ == "__main__":
    main()
