#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为含 【Fx-y】 总体讲解注释的代码块追加逐行中文注释（标记 // 【行】…）。

规则：
  - 总体讲解行：含 【Fx-y·子项】功能链实例：… 本处职责：…
  - 逐行注释：紧跟其后的函数/方法/模板片段，直到下一同级 【Fx-y】块或空段
  - 已有 // 【行】 或 <!-- 【行】 的行跳过

用法：
  python scripts/annotate_f_codeblock.py
  python scripts/annotate_f_codeblock.py --dry-run
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT = {".java", ".vue", ".js", ".bat", ".ps1", ".sql"}
F_HEADER = re.compile(r"【F\d+-\d+·[^】]+】功能链实例：")
LINE_MARK = re.compile(r"【行】")
SKIP_DIRS = {"node_modules", "target", ".git", "static/assets"}


def describe_js_line(stripped: str) -> str | None:
    if not stripped or stripped in ("{", "}", "});", "},", ")", "(", "});"):
        return None
    if stripped.startswith("//") or stripped.startswith("/*") or stripped.startswith("*"):
        return None
    if LINE_MARK.search(stripped):
        return None
    pairs = [
        (r"^const params = ", "初始化 GET 查询参数字典，键名与后端约定一致"),
        (r"^return params", "返回参数字典，供 axios call() 拼接到 URL"),
        (r"^return ", "返回本函数计算结果给调用方"),
        (r"^if \(.*\) return", "条件不满足时提前结束，避免无效请求或错误状态"),
        (r"^if \(", "分支判断：根据当前 UI 状态决定后续逻辑"),
        (r"await loadStudyStats\(\)", "异步拉取学习统计数据并写入 studyStats ref"),
        (r"loadStudyStats\(\)\.then", "拉数完成后刷新柱图展示"),
        (r"drawStudentChart\(\)", "根据最新 studyBars 重绘 ECharts 柱图"),
        (r"studyStatsRangeMode\.value = ", "更新当期/往期 Tab 对应的 rangeMode 状态"),
        (r"studyStatsStartDate\.value", "读写往期统计的开始日期 ref"),
        (r"studyStatsEndDate\.value", "读写往期统计的结束日期 ref"),
        (r"studyStatsRangeTouched\.value = true", "标记用户已手动改过日期，禁止被 API 回写覆盖"),
        (r"studentPage\.value = 'stats'", "切换学生端子页面为学习统计"),
        (r"statPeriod\.value = ", "切换日报/周报/月报/年报周期 Tab"),
        (r"params\.startDate", "往期模式下附加自定义开始日期 query"),
        (r"params\.endDate", "往期模式下附加自定义结束日期 query"),
        (r"const range = ", "从快捷按钮配置函数取出 [起,止] 日期数组"),
        (r"const tmp = ", "临时变量，用于交换起止日期纠正逆序"),
        (r"normalizeStudyStatsDateRange\(\)", "保证开始日期不晚于结束日期"),
        (r"await call\(", "带 JWT 调用后端 REST API"),
        (r"\.value = await call", "把接口 JSON 写入 Vue 响应式 ref"),
        (r"^async function ", None),
        (r"^function ", None),
    ]
    for pat, hint in pairs:
        if hint and re.search(pat, stripped):
            return hint
    if "=" in stripped and not stripped.startswith("case "):
        left = stripped.split("=", 1)[0].strip()
        if left.startswith("const ") or left.startswith("let "):
            var = re.sub(r"^(const|let)\s+", "", left).split("[")[0].strip()
            return f"声明并赋值变量 `{var}`"
    if stripped.endswith("{"):
        return "进入代码块"
    if stripped.endswith("}"):
        return None
    return "执行本行语句，推进功能链中的当前步骤"


def describe_java_line(stripped: str) -> str | None:
    if not stripped or stripped in ("{", "}"):
        return None
    if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("@"):
        return None
    if LINE_MARK.search(stripped):
        return None
    pairs = [
        (r"^return ", "返回 Service 结果给 Controller，最终序列化为 JSON"),
        (r"^if \(", "按业务条件分支处理"),
        (r"^throw new ", "校验失败时抛出业务异常，由全局处理器转为 JSON 错误"),
        (r"jdbcTemplate", "通过 JDBC 执行 SQL 并映射结果"),
        (r"String\.formatted", "拼接动态 SQL 或消息字符串"),
        (r"^Map<String, Object>", "声明返回给前端的键值 DTO"),
    ]
    for pat, hint in pairs:
        if hint and re.search(pat, stripped):
            return hint
    if stripped.endswith("{"):
        return "进入方法体或分支块"
    if ";" in stripped:
        return "执行本行 Java 语句"
    return None


def describe_vue_template_line(stripped: str) -> str | None:
    if not stripped or stripped.startswith("<!--") and "【行】" in stripped:
        return None
    if not stripped.startswith("<") and not stripped.startswith("</"):
        return None
    if LINE_MARK.search(stripped):
        return None
    if "el-date-picker" in stripped:
        return "Element Plus 日期选择器：独立单月历，避免 daterange 双面板重叠"
    if "studyStatsRangeMode" in stripped:
        return "绑定当期/往期 Tab 高亮与点击切换"
    if "studyStatsStartDate" in stripped:
        return "绑定往期统计开始日期，变更时触发 onStudyStatsStartDateChange"
    if "studyStatsEndDate" in stripped:
        return "绑定往期统计结束日期，变更时触发 onStudyStatsEndDateChange"
    if "applyStudyStatsShortcut" in stripped:
        return "快捷区间按钮：一键写入起止日期并拉数"
    if "bar-chart-lite" in stripped or "studyBars" in stripped:
        return "轻量柱图：按 studyBars 计算属性渲染每日/每月学习时长"
    if "statPeriod" in stripped or "changeStatPeriod" in stripped:
        return "日报~年报周期 Tab 切换"
    if stripped.startswith("<template") or stripped.startswith("</template"):
        return None
    if stripped.startswith("<div") or stripped.startswith("<button"):
        return "模板 UI 节点：展示学习统计页对应区域"
    return "模板标记：绑定数据或事件到 Vue 实例"


def append_comment(line: str, hint: str, lang: str) -> str:
    if lang == "bat":
        if LINE_MARK.search(line):
            return line
        return line.rstrip() + f" & REM 【行】{hint}" + ("\n" if line.endswith("\n") else "")
    if lang == "ps1":
        if LINE_MARK.search(line) or line.strip().startswith("#"):
            # 已有 # 注释行：在末尾追加 【行】说明（PowerShell 支持行尾 #）
            if LINE_MARK.search(line):
                return line
            return line.rstrip() + f" # 【行】{hint}" + ("\n" if line.endswith("\n") else "")
        return line.rstrip() + f" # 【行】{hint}" + ("\n" if line.endswith("\n") else "")
    if lang == "vue_template":
        if "-->" in line:
            return line.replace("-->", f" 【行】{hint} -->", 1)
        return line.rstrip() + f" <!-- 【行】{hint} -->" + ("\n" if line.endswith("\n") else "")
    suffix = f" // 【行】{hint}"
    if line.rstrip().endswith(suffix.strip()):
        return line
    return line.rstrip() + suffix + ("\n" if line.endswith("\n") else "")


def find_block_end(lines: list[str], start: int, lang: str) -> int:
    if lang == "java":
        depth = 0
        started = False
        for i in range(start, len(lines)):
            depth += lines[i].count("{") - lines[i].count("}")
            if "{" in lines[i]:
                started = True
            if started and depth <= 0 and i > start:
                return i
        return min(start + 80, len(lines) - 1)
    if lang == "js":
        depth = 0
        started = False
        for i in range(start, len(lines)):
            s = lines[i].strip()
            depth += s.count("{") - s.count("}")
            if "{" in s or s.startswith("function") or s.startswith("async function"):
                started = True
            if started and depth <= 0 and i > start:
                return i
        return min(start + 60, len(lines) - 1)
    # vue template: until next major section comment or blank + non-template
    end = start
    for i in range(start, min(start + 80, len(lines))):
        if i > start and F_HEADER.search(lines[i]) and "【行】" not in lines[i]:
            return i - 1
        end = i
    return end


def process_file(path: Path, dry_run: bool) -> int:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return 0
    lines = raw.splitlines(keepends=True)
    changed = 0
    i = 0
    in_template = False
    while i < len(lines):
        line = lines[i]
        if "<template" in line:
            in_template = True
        if "</template>" in line:
            in_template = False
        if not F_HEADER.search(line):
            i += 1
            continue
        lang = "bat" if path.suffix.lower() == ".bat" else (
            "ps1" if path.suffix.lower() == ".ps1" else (
            "vue_template" if in_template or line.strip().startswith("<!--") else (
            "java" if path.suffix == ".java" else "js"))
        )
        block_start = i + 1
        block_end = find_block_end(lines, block_start, lang if lang != "vue_template" else "js")
        if lang == "vue_template":
            block_end = find_block_end(lines, block_start, "js")
        for j in range(block_start, block_end + 1):
            stripped = lines[j].strip()
            if not stripped:
                continue
            if F_HEADER.search(lines[j]) and j != i:
                break
            if lang == "java":
                hint = describe_java_line(stripped)
            elif lang == "vue_template":
                hint = describe_vue_template_line(stripped)
            else:
                hint = describe_js_line(stripped)
            if not hint:
                continue
            new_line = append_comment(lines[j], hint, lang)
            if new_line != lines[j]:
                lines[j] = new_line
                changed += 1
        i = block_end + 1
    if changed and not dry_run:
        path.write_text("".join(lines), encoding="utf-8")
    if changed:
        print(f"{'[dry] ' if dry_run else ''}{path.relative_to(ROOT)}: +{changed} line comments")
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    total = 0
    for p in sorted(ROOT.rglob("*")):
        if p.suffix.lower() not in EXT:
            continue
        if any(x in p.parts for x in SKIP_DIRS):
            continue
        total += process_file(p, args.dry_run)
    print(f"done: {total} line comments {'(dry-run)' if args.dry_run else 'written'}")


if __name__ == "__main__":
    main()
