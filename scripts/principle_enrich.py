#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原理列五段内容的零基础扩写：在 rebuild_principles 生成初稿后，
为 ②～⑤ 段注入层说明、本节全景、IO 提示、读码指引与追加答辩问法。
"""
from __future__ import annotations

import re

INTRA_SEP = "<br>"

LAYER_BEGINNER: dict[str, str] = {
    "表现": "【零基础·你能看到的层】浏览器里的页面、按钮、输入框；只负责「展示 + 收集点击」，不算信用、不写数据库。",
    "Presentation": "【零基础·你能看到的层】浏览器里的页面、按钮、输入框；只负责「展示 + 收集点击」，不算信用、不写数据库。",
    "接口": "【零基础·接待员层】Tomcat 收到 HTTP 请求后，由 Controller 读 JSON/路径参数，转交给 Service，再把结果包装成 `{code,data,message}` 返回。",
    "Controller": "【零基础·接待员层】Tomcat 收到 HTTP 请求后，由 Controller 读 JSON/路径参数，转交给 Service，再把结果包装成 `{code,data,message}` 返回。",
    "业务": "【零基础·规则与数据库层】真正查 MySQL、校验能不能预约/登录、改 status、写 credit_log 的地方；答辩时 SQL 多半在这一层。",
    "Service": "【零基础·规则与数据库层】真正查 MySQL、校验能不能预约/登录、改 status、写 credit_log 的地方；答辩时 SQL 多半在这一层。",
    "配置": "【零基础·全员共用层】JWT 鉴权、跨域、白名单等「每个接口都要用」的能力，抽成 Filter/Config，避免每个 Controller 重复写 if。",
    "Config": "【零基础·全员共用层】JWT 鉴权、跨域、白名单等「每个接口都要用」的能力，抽成 Filter/Config，避免每个 Controller 重复写 if。",
    "数据": "【零基础·表结构层】MySQL 里表、字段、外键的定义；数据持久化靠 schema.sql + database-full.sql 导入。",
    "运维": "【零基础·启动层】bat/ps1 脚本，帮你在答辩机上一键装环境、导库、开 8080；不含预约/登录业务逻辑。",
    "Ops": "【零基础·启动层】bat/ps1 脚本，帮你在答辩机上一键装环境、导库、开 8080；不含预约/登录业务逻辑。",
    "样式": "【零基础·外观层】CSS 控制颜色、宽度、弹层 z-index；不改数据，只改「看起来对不对、会不会挡住」。",
    "Application": "【零基础·程序入口】Java 的 main 方法，相当于按下 Spring Boot 的电源键，启动内嵌 Tomcat。",
}

SECTION_FLOW: dict[str, str] = {
    "f1-1": "克隆仓库 → 双击 start.bat → PowerShell 检 Java/MySQL → 导入 database-full.sql 建库 → mvnw 启动 Spring Boot → 浏览器打开 8080 登录页 → verify 脚本输出 PASS=17 验收。",
    "f1-2": "小明在浏览器点「确认预约」→ Vue 把表单变成 JSON → HTTP POST 到 `/api/reservations` → Controller 转 Service → JDBC 写 MySQL → 返回 `{code:200}` → 页面刷新「我的预约」。",
    "f2-1": "小明输入学号密码 → 前端 POST `/auth/login` → Service 查 user_account 表 BCrypt 比对 → 签发 JWT → 浏览器存 localStorage → 以后每个请求 Header 带 Bearer token → 刷新页面 bootstrap 调 `/auth/me` 恢复会话。",
    "f2-2": "管理员切到管理员登录 → POST `/admin/auth/login` 查 admin_account → JWT role=ADMIN → 侧栏进签到/用户管理等；superadmin 多「设置」「管理员管理」。",
    "f2-3": "小李注册填表+上传证件 → POST `/auth/register` → auditStatus=待审核 → 管理员 F6.3 点通过 → auditStatus=已通过 → 小李才能 F2.1 登录。",
    "f2-4": "小明在「我的」改资料/改密码 → PUT profile 或 POST change-password → Service UPDATE 表 → 改密后前端清 token 强制重新登录。",
    "f3-1": "小明选自习室/日期/时段/座位 → 前端 POST `/reservations` → Service 校验信用/黑名单/时长 → INSERT reservation + reservation_slot 占位 → 返回 16 位预约号 → notifyUser 发站内信。",
    "f3-2": "小明在「我的预约」点取消 → POST `/reservations/{id}/cancel` → 仅 status=待使用可取消 → 扣分写 credit_log → releaseSlots 释放时间片。",
    "f3-3": "小明打开我的预约 → GET `/reservations/my` → 卡片展示 status → 每 2 分钟自动 refresh → 可跳转取消(F3.2)或等签到(F4.1)。",
    "f4-1": "管理员扫 QR/输学号 → POST `/admin/checkin/scan` → 校验预约待使用+学号匹配 → INSERT checkin_record → status=使用中 → 信用 +5。",
    "f4-2": "小明使用中点签退 → POST `/reservations/{id}/checkout` → 写 sign_out_time、status=已完成、算 studyMinutes → 刷新信用与列表。",
    "f4-3": "Spring @Scheduled 每分钟扫库 → 超时未签到变已违约 → 过 end_time 自动签退 → 到期解除黑名单；全程无页面。",
    "f5-1": "小明进学习统计 → 选当期/往期与日报~年报 → buildStudyStatsParams 拼 query → GET `/statistics/my-study-duration` → studyBars 转小时 → bar-chart-lite 画柱图。",
    "f5-2": "管理员发公告 → 学生首页卡片 GET `/announcements`；业务事件 notifyUser → 学生铃铛页 GET `/notifications/my` 个人消息。",
    "f5-3": "小明提交反馈 → INSERT feedback_ticket → 管理员处理改 status → 学生可看处理结果。",
    "f6-1": "管理员进统计页 → GET `/admin/statistics/report` 一次 JDBC 算多图 → ECharts 展示；导出 GET export 共用同一 SQL 出 CSV。",
    "f6-2": "超管进设置 → 读/写 system_config JSON（最长预约时长等）→ 后续 F3.1 预约校验读同一配置。",
    "f6-3": "管理员筛用户 → 审核/禁用/导出 CSV → disable 后该账号无法 F2.1 登录。",
    "f6-4": "管理员 CRUD 自习室与座位 → 布局图 uploads 目录 → 学生 F3.1 选座读 seat 状态。",
    "f6-5": "监管违约列表 → revokeViolation 撤销误违约恢复信用 → 写 operation_log。",
    "f6-6": "管理员签到页底部 live-reservations → 实时看待签到/使用中；学生端轮询同步。",
    "f6-7": "超管管 admin_account → 操作写 operation_log 审计。",
    "f7-1": "业务 SQL 在 AppService 用 JdbcTemplate 拼接；DatabaseInitializer 启动补表；未用 JPA/Hibernate。",
    "f7-2": "status 等字段存中文 VARCHAR（待使用/使用中）；schema CHECK 与 database-full.sql 字典一致；无 temp_leave。",
    "f7-3": "DB 存中文 status → 前端 reservationStatusValue 映射 tag 颜色与筛选 canonical。",
    "f7-4": "16 张业务表 + 外键：学生→预约→座位→自习室；ER 见 schema 文件头注释。",
}


def _condense(text: str, max_len: int = 380) -> str:
    s = re.sub(r"\s+", " ", text).strip(" ；;")
    return s[: max_len - 1] + "…" if len(s) > max_len else s


def layer_beginner_note(layer: str) -> str:
    for key, val in LAYER_BEGINNER.items():
        if key in layer:
            return val
    return ""


def layer_short_name(layer: str) -> str:
    return layer.split("·")[0].strip() or layer


def io_beginner_hint(layer: str, symbol: str, f_code: str, route_hint: dict[str, str]) -> str:
    sym = symbol.lower()
    if "表现" in layer or "Presentation" in layer:
        return (
            "**输入**：用户在页面的点击/表单（ref 里的值）。"
            "**输出**：更新 Vue 的 ref/computed 让页面变样，或发 HTTP 等 JSON 回来。"
            "**失败时**：`notify()`/`ElMessage` 弹中文错误，不崩溃整页。"
        )
    if "Controller" in layer or "接口" in layer:
        route = route_hint.get(symbol, route_hint.get(sym, f"/api/...（见 `{sym}`）"))
        return (
            f"**输入**：HTTP 请求（路径 `{route}`、JSON body、Header 里 Bearer JWT）。"
            "**输出**：`ApiResponse` JSON，前端 `call()` 读 `data` 字段。"
            "**失败时**：Service 抛 BusinessException → 全局处理器转 `{code,message}`，或 Filter 直接 401。"
        )
    if "Service" in layer or "业务" in layer:
        return (
            "**输入**：Controller 传入的 DTO/基本类型（userId、seatId、时间段等）。"
            "**输出**：Map/DTO 或 void；副作用为 UPDATE/INSERT MySQL 表。"
            "**失败时**：`throw new BusinessException(\"中文原因\")`，事务回滚，前端看到 message。"
        )
    if "配置" in layer or "Config" in layer:
        return (
            "**输入**：每个 `/api/**` 请求的 Header 与路径。"
            "**输出**：放行并注入 SecurityContext（userId/role），或 401 JSON 拦截。"
            "**失败时**：token 过期/伪造 → 401，前端 bootstrap 清 localStorage。"
        )
    if "运维" in layer or "Ops" in layer:
        return (
            "**输入**：双击 bat 或命令行参数、环境变量（如 CSRRM_MYSQL_PASSWORD）。"
            "**输出**：MySQL 库就绪、8080 进程、控制台 PASS=17 或错误码。"
            "**失败时**：exit 非 0，窗口保留报错，不启动半残后端。"
        )
    if "样式" in layer:
        return (
            "**输入**：Element Plus 渲染出的 DOM 类名（如 popper-class）。"
            "**输出**：CSS 规则改变宽度/z-index/背景，弹层与柱图对齐。"
            "**失败时**：仅 UI 错位，不影响 API 数据正确性。"
        )
    return (
        f"**输入/输出**：见 `{symbol}` 在 `{f_code.upper()}` 功能链中的前后表行；"
        f"改码后对照 GitHub 行号 `【Fx-y】`+`【行】` 注释逐步跟读。"
    )


def design_alternative(layer: str, symbol: str) -> str:
    if "表现" in layer:
        return f"若在前端 `{symbol}` 里算信用/写 SQL，换浏览器结果可能不一致，且规则易泄露，故必须只展示后端返回值。"
    if "Controller" in layer:
        return f"若在 `{symbol}` 写 JDBC，则定时任务、导出、多处入口要复制 SQL，一改规则漏改一处就出 bug，故只做 HTTP 适配。"
    if "Service" in layer:
        return "若用 JPA 全自动 SQL，动态报表（F6.1）与复杂 WHERE（F5.1 时间窗）难写难讲，故课选用 JdbcTemplate 显式 SQL 便于答辩指行。"
    if "配置" in layer:
        return "若每个 Controller 手写 if(token)，漏写一个接口就裸奔；抽成 Filter 后新增接口默认受保护。"
    if "运维" in layer:
        return "若只给 README 文字步骤，答辩机易漏装 MySQL/忘导库；脚本把多步合成双击，降低人为失误。"
    return f"本行 `{symbol}` 的替代方案见 F1.2 八卡分层：职责错层是答辩常见扣分点。"


def design_layer_why(layer: str) -> str:
    if "表现" in layer:
        return "交互密集、改 UI 频繁，放 Vue 模板/JS 最快；与后端通过 REST 解耦，前端可独立 npm run build。"
    if "Controller" in layer:
        return "HTTP 形态（路径、动词、状态码）集中在一层，Service 可被 Controller、定时任务、脚本测试共用。"
    if "Service" in layer:
        return "业务规则 + SQL 是系统「真相来源」，放一层便于单元测试与答辩时打开 AppService 指 SQL。"
    if "配置" in layer:
        return "鉴权、CORS、JWT 密钥与所有接口相关，放 config 包一处维护。"
    if "运维" in layer:
        return "部署与业务生命周期不同，脚本不进 jar，clone 后不改 Java 也能重建环境。"
    if "样式" in layer:
        return "全局 popper/布局问题用 CSS 统一修，避免在每个 Vue 组件 inline style 重复补丁。"
    return f"{layer_short_name(layer)} 在本节链路中承担上表「所属层」对应职责，与相邻行上下衔接。"


def extra_qa_hints(f_code: str, symbol: str, layer: str) -> str:
    sym = symbol.lower()
    extras: list[str] = []
    if "表现" in layer or "Presentation" in layer:
        extras.append("问：数据存在浏览器吗？答：仅 token 与 UI 状态在 localStorage/ref；预约/信用等权威数据每次从 API 拉。")
    if "Controller" in layer:
        extras.append("问：这行会访问数据库吗？答：Controller 层一般不写 SQL，查表在下一行 Service 同名方法。")
    if "Service" in layer:
        extras.append("问：SQL 在哪看？答：AppService.java 搜方法名，或 GitHub 定位列 L 行 `【行】` 注释旁。")
    if f_code == "f5-1" and ("stat" in sym or "study" in sym):
        extras.append("问：为什么有预约但统计为 0？答：统计只计「已签到且使用中/已完成」的时长，仅「待使用」不算。")
    if f_code == "f2-1":
        extras.append("问：忘记密码怎么办？答：课设演示账号固定；真实系统应做找回流程，本项未实现。")
    if f_code == "f3-1":
        extras.append("问：两人同时抢一座？答：reservation_slot 唯一键 uk_seat_slot，后插入者 API 报错「已被预约」。")
    if f_code == "f4-3":
        extras.append("问：关掉 8080 定时还跑吗？答：不跑，@Scheduled 随 JVM 进程，答辩演示需保持服务在线。")
    return INTRA_SEP.join(extras)


def impl_reading_guide(locate: str, path: str, symbol: str, line_ref_fn) -> str:
    lr = line_ref_fn(locate)
    pf = path or "见定位列路径"
    return (
        f"**怎么读代码（零基础）**：打开 `{pf}`，从 {lr} 找 `【F*】` 首段（整段在讲 `{symbol}` 干什么），"
        f"往下每行带 `【行】` 的中文即逐行讲解；改行号后跑 `sync_github_line_anchors.py`。"
    )


def enrich_detail(
    f_code: str,
    story: str,
    layer: str,
    symbol: str,
    locate: str,
    path: str,
    detail: dict[str, str],
    line_ref_fn,
    route_hint: dict[str, str],
) -> dict[str, str]:
    lb = layer_beginner_note(layer)
    flow = SECTION_FLOW.get(f_code, "")
    flow_note = f"【本节一条龙】{flow}" if flow else (f"【本节实例】{_condense(story, 160)}" if story else "")
    chain_core = detail.get("chain", "")
    chain_parts = [
        p
        for p in [
            lb,
            flow_note,
            f"**本行 `{symbol}` 在链中的位置**：{chain_core}",
            io_beginner_hint(layer, symbol, f_code, route_hint),
        ]
        if p
    ]
    impl_parts = [
        impl_reading_guide(locate, path, symbol, line_ref_fn),
        f"**技术细节**：{detail.get('impl', '')}",
    ]
    design_parts = [
        f"**为何放在{layer_short_name(layer)}**：{design_layer_why(layer)}",
        detail.get("design", ""),
        f"**若不这样做**：{design_alternative(layer, symbol)}",
    ]
    qa_parts = [detail.get("qa", "")]
    extra = extra_qa_hints(f_code, symbol, layer)
    if extra:
        qa_parts.append(extra)
    return {
        "chain": INTRA_SEP.join(chain_parts),
        "impl": INTRA_SEP.join(impl_parts),
        "design": INTRA_SEP.join(d for d in design_parts if d),
        "qa": INTRA_SEP.join(q for q in qa_parts if q),
    }


def enrich_concepts(concepts: str, symbol: str, layer: str) -> str:
    if symbol and symbol not in ("本行", "page", "stats page"):
        sym_note = (
            f"**本行符号 `{symbol}`**：本节功能链里「{layer_short_name(layer)}」侧的关键入口，"
            f"下面 ②～⑤ 按「谁调用谁、怎么读写库、为何这样设计、答辩怎么答」展开。"
        )
        if sym_note not in concepts:
            return concepts + INTRA_SEP + sym_note
    return concepts
