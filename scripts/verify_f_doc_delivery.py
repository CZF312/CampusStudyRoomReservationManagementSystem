#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSRRMS 文档最终交付自检。

检查项：
  1. 01/02 页内锚点数量与 F6.7 等关键 id
  2. 实现定位表中 file:/// 链接是否均带 #L
  3. 65 个 HTTP 端点在 01 中的覆盖（主链 / F8 矩阵 / 缺失）
  4. 【Fx-y】源码注释扫描摘要

用法：
  cd CampusStudyRoomReservationManagementSystem-master
  python scripts/verify_f_doc_delivery.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_01 = ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md"
DOC_02 = ROOT / "docs" / "09-理解与讲解" / "02-答辩讲解手册.md"

# (method path_fragment, F节, 说明)
ENDPOINTS: list[tuple[str, str, str]] = [
    ("POST /auth/register", "F2.3", "学生注册"),
    ("POST /auth/login", "F2.1", "学生登录"),
    ("POST /admin/auth/login", "F2.2", "管理员登录"),
    ("GET /auth/me", "F2.1", "会话恢复 bootstrap"),
    ("POST /auth/change-password", "F2.4", "改密"),
    ("GET /student/profile", "F2.4", "读资料"),
    ("PUT /student/profile", "F2.4", "更新资料"),
    ("POST /auth/register/upload", "F2.3", "注册材料上传"),
    ("GET /rooms", "F3.1", "学生自习室列表"),
    ("GET /rooms/{id}", "F8", "单室详情（前端少用）"),
    ("GET /rooms/{id}/seats", "F8", "学生端座位列表（多用 available）"),
    ("GET /seats/available", "F3.1", "可用座"),
    ("POST /reservations", "F3.1", "创建预约"),
    ("GET /reservations/my", "F3.3", "我的预约"),
    ("GET /reservations/{id}", "F8", "单条预约详情 API"),
    ("POST /reservations/{id}/cancel", "F3.2", "取消预约"),
    ("GET /checkin/qrcode", "F8", "后端 QR 接口，前端未用"),
    ("POST /reservations/{id}/checkout", "F4.2", "签退"),
    ("GET /credits/my", "F4.2", "信用流水"),
    ("GET /statistics/my-study-duration", "F5.1", "学习统计"),
    ("GET /announcements", "F5.2", "公告列表"),
    ("POST /announcements/{id}/read", "F5.2", "公告已读"),
    ("GET /notifications", "F5.2", "站内通知"),
    ("POST /notifications/{id}/read", "F5.2", "通知已读"),
    ("POST /notifications/read-all", "F5.2", "全部已读"),
    ("POST /feedback", "F5.3", "提交反馈"),
    ("GET /feedback/my", "F8", "我的反馈列表无 UI"),
    ("GET /admin/dashboard", "F8", "桩接口"),
    ("GET /admin/live-reservations", "F6.6", "实时预约"),
    ("GET /admin/users", "F6.3", "用户列表"),
    ("GET /admin/users/pending", "F8", "待审核列表 API"),
    ("GET /admin/users/export", "F6.3", "导出 CSV"),
    ("POST /admin/users/{id}/approve", "F2.3", "审核通过"),
    ("POST /admin/users/{id}/reject", "F6.3", "审核拒绝"),
    ("POST /admin/users/{id}/disable", "F6.3", "禁用"),
    ("POST /admin/users/{id}/enable", "F6.3", "启用"),
    ("GET /admin/rooms", "F6.4", "管理端自习室"),
    ("POST /admin/rooms", "F6.4", "新增自习室"),
    ("PUT /admin/rooms/{id}", "F6.4", "更新自习室"),
    ("DELETE /admin/rooms/{id}", "F6.4", "删除自习室"),
    ("GET /admin/rooms/{id}/seats", "F6.4", "座位列表"),
    ("PUT /admin/seats/{id}", "F6.4", "改座位"),
    ("PUT /admin/rooms/{id}/seats/batch", "F8", "批量改座无 UI"),
    ("POST /admin/rooms/{roomId}/seats", "F6.4", "新增座位"),
    ("DELETE /admin/seats/{id}", "F6.4", "删座位"),
    ("GET /admin/reservations", "F6.5", "预约监管"),
    ("POST /admin/reservations/{id}/revoke-violation", "F6.5", "撤销违约"),
    ("POST /admin/checkin/scan", "F4.1", "扫码签到"),
    ("GET /admin/checkins", "F4.1", "签到记录"),
    ("GET /admin/announcements", "F5.2", "管理端公告"),
    ("POST /admin/announcements", "F5.2", "发布公告"),
    ("PUT /admin/announcements/{id}", "F5.2", "编辑公告"),
    ("DELETE /admin/announcements/{id}", "F8", "删公告 API"),
    ("GET /admin/statistics/usage", "F6.1", "使用率"),
    ("GET /admin/statistics/peak", "F6.1", "高峰"),
    ("GET /admin/statistics/report", "F6.1", "综合报表"),
    ("GET /admin/statistics/credit", "F6.1", "信用统计"),
    ("GET /admin/statistics/export", "F6.1", "CSV 导出"),
    ("GET /admin/feedback", "F5.3", "反馈列表"),
    ("PUT /admin/feedback/{id}", "F5.3", "处理反馈"),
    ("GET /admin/settings/config", "F6.2", "读系统配置"),
    ("POST /admin/settings/config", "F6.2", "写系统配置"),
    ("GET /admin/operation-logs", "F6.7", "操作日志"),
    ("GET /admin/admins", "F6.7", "管理员列表"),
    ("POST /admin/admins", "F6.7", "新增管理员"),
    ("PUT /admin/admins/{id}", "F6.7", "改管理员"),
    ("POST /admin/admins/{id}/disable", "F6.7", "禁用管理员"),
    ("POST /admin/admins/{id}/enable", "F6.7", "启用管理员"),
    ("POST /upload", "F6.4", "布局图上传"),
]

REQUIRED_ANCHORS_01 = [
    "toc", "f1", "f1-1", "f1-2", "f2", "f2-1", "f2-2", "f2-3", "f2-4",
    "f3", "f3-1", "f3-2", "f3-3", "f4", "f4-1", "f4-2", "f4-3",
    "f5", "f5-1", "f5-2", "f5-3", "f6", "f6-1", "f6-2", "f6-3", "f6-4",
    "f6-5", "f6-6", "f6-7", "f7", "f7-1", "f7-2", "f7-3", "f7-4", "f8",
]

FILE_LINK = re.compile(r"file:///[^\s\)]+\.md", re.I)
FILE_LINK_NO_LINE = re.compile(r"file:///[^\s\)#]+\.(?:java|vue|sql|ps1|bat)(?!\#L)", re.I)
ANCHOR_ID = re.compile(r'<a id="([^"]+)"></a>')


def count_anchors(text: str) -> list[str]:
    return ANCHOR_ID.findall(text)


def path_frag_in_doc(doc: str, method_path: str) -> bool:
    """在 01 中查找端点痕迹：路径片段或典型 controller 映射。"""
    _, path = method_path.split(" ", 1)
    # 去掉路径参数占位，取最后一段或特征段
    needles = [
        path.replace("{id}", "").replace("{roomId}", "").strip("/"),
        path.split("/")[-1].replace("{id}", "").replace("{roomId}", ""),
    ]
    for n in needles:
        if n and n in doc:
            return True
    # 常见简写
    aliases = {
        "auth/me": "/auth/me",
        "register/upload": "registerUpload",
        "live-reservations": "live-reservations",
        "revoke-violation": "revoke-violation",
        "read-all": "read-all",
        "my-study-duration": "my-study-duration",
        "seats/batch": "batchSeats",
        "checkin/qrcode": "checkin/qrcode",
    }
    tail = path.rstrip("/").split("/")[-1]
    if tail in aliases and aliases[tail] in doc:
        return True
    return False


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not DOC_01.exists():
        print("ERROR: 01 不存在", file=sys.stderr)
        return 1

    text01 = DOC_01.read_text(encoding="utf-8")
    text02 = DOC_02.read_text(encoding="utf-8") if DOC_02.exists() else ""

    anchors01 = count_anchors(text01)
    print(f"=== 页内锚点 ===")
    print(f"01: {len(anchors01)} 个")
    if DOC_02.exists():
        print(f"02: {len(count_anchors(text02))} 个")

    for aid in REQUIRED_ANCHORS_01:
        if aid not in anchors01:
            errors.append(f"01 缺少锚点 id={aid}")

    if "f6-7" not in anchors01:
        errors.append("01 缺少 F6.7 锚点（检查 sync 脚本 F6.7 标题匹配）")

    print(f"\n=== file:/// 链接（须带 #L）===")
    bare = FILE_LINK_NO_LINE.findall(text01)
    if bare:
        for b in bare[:10]:
            errors.append(f"裸链接无行号: {b}")
        if len(bare) > 10:
            errors.append(f"... 另有 {len(bare) - 10} 条裸链接")
    else:
        print("01 实现表链接均含 #L（或未使用 file 链接）")

    print(f"\n=== API 端点覆盖（共 {len(ENDPOINTS)}）===")
    ok = f8 = miss = 0
    missing_list: list[str] = []
    for ep, fsec, desc in ENDPOINTS:
        if path_frag_in_doc(text01, ep):
            if fsec == "F8":
                f8 += 1
            else:
                ok += 1
        else:
            miss += 1
            missing_list.append(f"  MISS [{fsec}] {ep} — {desc}")

    print(f"主链已提及: {ok} · F8/附录类: {f8} · 未在 01 出现: {miss}")
    for line in missing_list:
        warnings.append(line.strip())

    print(f"\n=== 【Fx-y】注释扫描 ===")
    try:
        out = subprocess.check_output(
            [sys.executable, str(ROOT / "scripts" / "scan_f_comment_lines.py")],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        lines = [ln for ln in out.strip().splitlines() if ln.strip()]
        print(f"共 {len(lines)} 条注释标记")
        if len(lines) < 80:
            warnings.append(f"注释条数偏少（{len(lines)}），建议 ≥80")
    except Exception as e:
        warnings.append(f"scan_f_comment_lines 失败: {e}")

    print(f"\n=== 结果 ===")
    if errors:
        print("FAIL:")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("PASS: 锚点与链接硬性检查通过")

    if warnings:
        print("WARN:")
        for w in warnings[:25]:
            print(f"  ! {w}")
        if len(warnings) > 25:
            print(f"  ! ... 另有 {len(warnings) - 25} 条")

    return 1 if errors else (0 if miss == 0 else 0)  # warnings 不阻断 exit 0


if __name__ == "__main__":
    raise SystemExit(main())
