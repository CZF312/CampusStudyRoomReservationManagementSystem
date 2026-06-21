#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 01/02 理解讲解 md 注入页内锚点，并把页内链接改为 GitHub 可跳转格式。

GitHub 渲染会把 HTML id="f1-2" 变成 id="user-content-f1-2"，
因此目录链接须写 #user-content-f1-2（Cursor/VS Code 预览同样可用）。

标题行内嵌：
  ## <a id="f1"></a>F1 入门基础

发布前必跑（改 md 后）：
  python scripts/sync_f_doc_anchors.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_DIR = ROOT / "docs" / "09-理解与讲解"

ANCHOR_RULES = [
    (r"^## 功能架构目录（根）", "toc"),
    (r"^## 模块总览", "module-overview"),
    (r"^## F1 入门基础", "f1"),
    (r"^### F1\.1 环境启动", "f1-1"),
    (r"^### F1\.2 技术概念", "f1-2"),
    (r"^## F2 认证与账号", "f2"),
    (r"^### F2\.1 学生登录", "f2-1"),
    (r"^### F2\.2 管理员登录", "f2-2"),
    (r"^### F2\.3 注册审核", "f2-3"),
    (r"^### F2\.4 账号资料与安全", "f2-4"),
    (r"^## F3 自习室与预约", "f3"),
    (r"^### F3\.1 查座预约", "f3-1"),
    (r"^### F3\.2 取消预约", "f3-2"),
    (r"^### F3\.3 我的预约", "f3-3"),
    (r"^## F4 签到签退与信用", "f4"),
    (r"^### F4\.1 签到", "f4-1"),
    (r"^### F4\.2 签退与信用", "f4-2"),
    (r"^### F4\.3 定时维护", "f4-3"),
    (r"^## F5 学生端辅助", "f5"),
    (r"^### F5\.1 学习统计", "f5-1"),
    (r"^### F5\.2 公告", "f5-2"),
    (r"^### F5\.3 问题反馈", "f5-3"),
    (r"^## F6 管理端", "f6"),
    (r"^### F6\.1 统计", "f6-1"),
    (r"^### F6\.2 系统配置", "f6-2"),
    (r"^### F6\.3 用户管理", "f6-3"),
    (r"^### F6\.4 自习室与座位", "f6-4"),
    (r"^### F6\.5 预约监管", "f6-5"),
    (r"^### F6\.6 运营看板", "f6-6"),
    (r"^### F6\.7 管理员", "f6-7"),
    (r"^## F7 第三版与数据", "f7"),
    (r"^### F7\.1 数据库与 Java 分工", "f7-1"),
    (r"^### F7\.2 第三版规范化", "f7-2"),
    (r"^### F7\.3 前端状态 canonical", "f7-3"),
    (r"^### F7\.4 十六张表", "f7-4"),
    (r"^## F8 附录", "f8"),
    (r"^### 常见问题", "f8-qa"),
    (r"^### 演示前检查清单", "f8-checklist"),
]

F_FRAGMENT = re.compile(
    r"^(?:user-content-)?(toc|f\d+(?:-\d+)?|f8-qa|f8-checklist)$"
)
ANCHOR_TAG = re.compile(r'<a id="[^"]+"></a>')
LINK_FRAGMENT = re.compile(r"\]\((#[^)]+)\)")


def gh_fragment(raw: str) -> str:
    """#f1-2 或 #user-content-f1-2 → #user-content-f1-2"""
    frag = raw.lstrip("#")
    m = F_FRAGMENT.match(frag)
    if not m:
        return raw
    return f"#user-content-{m.group(1)}"


def githubify_links(text: str) -> str:
    """同页 #f 链接改为 GitHub 兼容的 #user-content-f。"""

    def repl(m: re.Match[str]) -> str:
        return f"]({gh_fragment(m.group(1))})"

    # 先处理 01-项目理解指南.md#f3-1 形式
    text = re.sub(
        r"\]\(([^)#]+\.md)(#[^)]+)\)",
        lambda m: f"]({m.group(1)}{gh_fragment(m.group(2))})",
        text,
    )
    return LINK_FRAGMENT.sub(repl, text)


def inject_inline_anchors(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    count = 0
    for line in lines:
        stripped = ANCHOR_TAG.sub("", line).strip()
        matched = False
        for pattern, aid in ANCHOR_RULES:
            if re.match(pattern, stripped):
                title = ANCHOR_TAG.sub("", line).lstrip()
                if not title.startswith("#"):
                    title = stripped
                out.append(re.sub(r"^(#+\s*)", rf'\1<a id="{aid}"></a>', title, count=1))
                count += 1
                matched = True
                break
        if not matched:
            out.append(ANCHOR_TAG.sub("", line))
    return "\n".join(out) + ("\n" if text.endswith("\n") else ""), count


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text, n = inject_inline_anchors(text)
    text = githubify_links(text)
    path.write_text(text, encoding="utf-8")
    print(f"{path.name}: {n} heading anchors, links githubified")


def main() -> None:
    for name in (
        "00-文档导航.md",
        "01-项目理解指南.md",
        "02-答辩讲解手册.md",
    ):
        p = DOC_DIR / name
        if p.exists():
            process(p)


if __name__ == "__main__":
    main()
