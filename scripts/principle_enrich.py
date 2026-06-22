#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
原理列扩写辅助：链路/输入输出写入「链路中位置与代码地址」列；
实现讲解列保留 ①③④⑤（无重复链路段与「怎么读代码」套话）。
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


def _condense(text: str, max_len: int = 380) -> str:
    s = re.sub(r"\s+", " ", text).strip(" ；;")
    return s[: max_len - 1] + "…" if len(s) > max_len else s


def layer_short_name(layer: str) -> str:
    return layer.split("·")[0].strip() or layer


# 按符号定制输入/输出（避免同层每行重复同一套话）
SYMBOL_IO: dict[str, str] = {
    "start.bat": INTRA_SEP.join([
        "输入：双击 bat 或 cmd 调用。",
        "输出：调用 start-system.ps1，exit code 原样返回。",
        "失败时：无 pom.xml 或 ps1 非 0 → ERROR + pause。",
    ]),
    "start-system.ps1": INTRA_SEP.join([
        "输入：bat 调用；可选环境变量 CSRRM_MYSQL_PASSWORD。",
        "输出：导库 PASS=17、新窗口 mvnw、8080 可访问。",
        "失败时：Java/MySQL/static 缺失或 verify 失败 → exit 1。",
    ]),
    "verify-v3-dictionary.ps1": INTRA_SEP.join([
        "输入：MySQL 已导入 database-full.sql；root 密码。",
        "输出：控制台 PASS=17 / FAIL=n；exit 0 或 1。",
        "失败时：表数/外键/字典不符 → 红色 FAIL，需重跑 setup。",
    ]),
    "DatabaseInitializer.run": INTRA_SEP.join([
        "输入：Spring 容器启动完成（无 HTTP）。",
        "输出：缺表时执行 classpath 补丁 SQL。",
        "失败时：SQL 异常 → Boot 启动失败，8080 不起。",
    ]),
    "runMaintenanceTasks": INTRA_SEP.join([
        "输入：@Scheduled 定时触发，无 HTTP 参数。",
        "输出：依次调用 markNoShow/autoCheckout 等维护方法。",
        "失败时：单任务异常记日志，下次调度继续。",
    ]),
}


def _norm_io_sym(symbol: str) -> str:
    return re.sub(r"[^a-z0-9.]", "", symbol.lower())


def io_beginner_hint(layer: str, symbol: str, f_code: str, route_hint: dict[str, str]) -> str:
    sym = _norm_io_sym(symbol)
    for key, val in SYMBOL_IO.items():
        if _norm_io_sym(key) == sym:
            return val
    if sym.startswith("scheduledprocess"):
        return INTRA_SEP.join([
            "输入：@Scheduled 触发，无 HTTP。",
            "输出：JdbcTemplate UPDATE 预约/信用/黑名单表。",
            "失败时：记录日志，不弹前端（无 UI）。",
        ])
    if "表现" in layer or "Presentation" in layer:
        return INTRA_SEP.join([
            "输入：用户在页面的点击/表单（ref 里的值）。",
            "输出：更新 Vue 的 ref/computed 让页面变样，或发 HTTP 等 JSON 回来。",
            "失败时：notify()/ElMessage 弹中文错误，不崩溃整页。",
        ])
    if "Controller" in layer or "接口" in layer:
        route = route_hint.get(symbol, route_hint.get(sym, f"/api/...（见 `{sym}`）"))
        return INTRA_SEP.join([
            f"输入：HTTP 请求（路径 `{route}`、JSON body、Header 里 Bearer JWT）。",
            "输出：ApiResponse JSON，前端 call() 读 data 字段。",
            "失败时：Service 抛 BusinessException → 全局处理器转 {code,message}，或 Filter 直接 401。",
        ])
    if "Service" in layer or "业务" in layer:
        return INTRA_SEP.join([
            "输入：Controller 传入的 DTO/基本类型（userId、seatId、时间段等）。",
            "输出：Map/DTO 或 void；副作用为 UPDATE/INSERT MySQL 表。",
            "失败时：throw new BusinessException(\"中文原因\")，事务回滚，前端看到 message。",
        ])
    if "配置" in layer or "Config" in layer:
        return INTRA_SEP.join([
            "输入：每个 /api/** 请求的 Header 与路径。",
            "输出：放行并注入 SecurityContext（userId/role），或 401 JSON 拦截。",
            "失败时：token 过期/伪造 → 401，前端 bootstrap 清 localStorage。",
        ])
    if "运维" in layer or "Ops" in layer:
        return INTRA_SEP.join([
            "输入：双击 bat 或命令行参数、环境变量（如 CSRRM_MYSQL_PASSWORD）。",
            "输出：MySQL 库就绪、8080 进程、控制台 PASS=17 或错误码。",
            "失败时：exit 非 0，窗口保留报错，不启动半残后端。",
        ])
    if "样式" in layer:
        return INTRA_SEP.join([
            "输入：Element Plus 渲染出的 DOM 类名（如 popper-class）。",
            "输出：CSS 规则改变宽度/z-index/背景，弹层与柱图对齐。",
            "失败时：仅 UI 错位，不影响 API 数据正确性。",
        ])
    return (
        f"输入/输出：见 `{symbol}` 在 {f_code.upper()} 功能链中的前后表行；"
        "改码后对照 GitHub 行号 【Fx-y】+【行】 注释逐步跟读。"
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
        extras.append("问：SQL 在哪看？答：AppService.java 搜方法名，或 GitHub 定位列 L 行 【行】 注释旁。")
    if f_code == "f5-1" and ("stat" in sym or "study" in sym):
        extras.append("问：为什么有预约但统计为 0？答：统计只计「已签到且使用中/已完成」的时长，仅「待使用」不算。")
    if f_code == "f2-1":
        extras.append("问：忘记密码怎么办？答：课设演示账号固定；真实系统应做找回流程，本项未实现。")
    if f_code == "f3-1":
        extras.append("问：两人同时抢一座？答：reservation_slot 唯一键 uk_seat_slot，后插入者 API 报错「已被预约」。")
    if f_code == "f4-3":
        extras.append("问：关掉 8080 定时还跑吗？答：不跑，@Scheduled 随 JVM 进程，答辩演示需保持服务在线。")
    return INTRA_SEP.join(extras)


def _parse_total_io(layer: str, symbol: str, f_code: str, route_hint: dict[str, str]) -> dict[str, str]:
    """从 SYMBOL_IO / io_beginner_hint 解析总输入输出。"""
    raw = io_beginner_hint(layer, symbol, f_code, route_hint)
    out: dict[str, str] = {}
    for line in re.split(r"<br\s*/?>", raw, flags=re.I):
        line = line.strip()
        for key, prefix in (
            ("input", "输入："),
            ("output", "输出："),
            ("fail", "失败时："),
        ):
            if line.startswith(prefix):
                out[key] = line[len(prefix) :].strip()
    return out


# 符号级分步链路（第二列分点 + 第三列按步对行号）
SYMBOL_CHAIN_STEPS: dict[str, list[dict[str, str]]] = {
    "start.bat": [
        {
            "work": "cd 到 bat 所在项目根，设 UTF-8 与窗口标题",
            "input": "用户双击 start.bat",
            "output": "工作目录=项目根；`CSRRM_SCRIPT_ROOT=%~dp0scripts`",
            "lines": "L1-L9",
            "detail": "@echo off；chcp 65001；`cd /d %~dp0` 固定项目根；首行 REM 含 `【F1-1】` 总体讲解。",
        },
        {
            "work": "校验 pom.xml 存在",
            "input": "当前目录",
            "output": "有 pom.xml 继续；无则 echo ERROR 并 exit /b 1",
            "lines": "L12-L16",
            "detail": "if not exist pom.xml → 错误提示 + pause + exit，防止在错误目录启动。",
        },
        {
            "work": "Bypass 执行策略调用 start-system.ps1",
            "input": "`scripts\\start-system.ps1`",
            "output": "PowerShell 五步链运行；`ERRORLEVEL` 写入 ERR",
            "lines": "L18-L22",
            "detail": "`powershell -ExecutionPolicy Bypass -File ...\\start-system.ps1`；重活交给 ps1。",
        },
        {
            "work": "pause 并透传退出码",
            "input": "ps1 的 `%ERRORLEVEL%`",
            "output": "窗口保留供答辩看 PASS/FAIL；`exit /b %ERR%`",
            "lines": "L24-L32",
            "detail": "根据 ERR 打印 Setup finished 或 ERROR；pause 防窗口闪退。",
        },
    ],
    "start-system.ps1": [
        {
            "work": "检 Java、mysql 客户端与 static/index.html",
            "input": "PATH 中 java/mysql；预构建 `static/index.html`",
            "output": "打印版本与 [OK] Frontend；缺依赖 exit 1",
            "lines": "L85-L99",
            "detail": "Write-Step [1/5]；Require-Command java/mysql；Test-Path staticIndex；JDK 版本提示。",
        },
        {
            "work": "检查并启动 MySQL Windows 服务",
            "input": "本机 MySQL/MariaDB 服务",
            "output": "服务 Status=Running（必要时 Start-Service）",
            "lines": "L109-L129",
            "detail": "Get-Service 匹配 mysql；未 Running 则 Start-Service + Sleep；失败 exit 1。",
        },
        {
            "work": "读/写 application-local.properties 中的 root 密码",
            "input": "可选 `CSRRM_MYSQL_PASSWORD`；或已保存密码；或交互 Read-Host",
            "output": "Test-MysqlLogin 通过；密码可写回 local 配置",
            "lines": "L131-L147",
            "detail": "Get-ConfiguredMysqlPassword → 空密码/已保存/循环 Read-Host 直至 mysql SELECT 1 成功。",
        },
        {
            "work": "调用 setup-after-clone.ps1 导库并验 PASS=17",
            "input": "上步 root 密码",
            "output": "DROP+导入 database-full.sql；verify-v3-dictionary PASS=17",
            "lines": "L149-L152",
            "detail": "调用 setup-after-clone.ps1 -MySqlPassword $password -SkipStart；非 0 则 exit。",
        },
        {
            "work": "新窗口 mvnw spring-boot:run 并轮询 8080",
            "input": "8080 空闲或已有实例返回 200",
            "output": "CSRRMS-Backend 窗口；http://localhost:8080 可访问",
            "lines": "L154-L191",
            "detail": "netstat 查 8080；`Start-Process cmd /k mvnw spring-boot:run`；Invoke-WebRequest 最多 60 秒轮询。",
        },
    ],
    "verify-v3-dictionary.ps1": [
        {
            "work": "连接 MySQL 并读取密码",
            "input": "mysql 在 PATH；database-full.sql 已导入",
            "output": "mysql 客户端就绪；$env:MYSQL_PWD 设置",
            "lines": "L18-L39",
            "detail": "检 mysql 命令；从 application-local.properties 或 Read-Host 取密码。",
        },
        {
            "work": "验库存在、16 表、外键与字典",
            "input": "study_room_reservation 库",
            "output": "information_schema 查询 PASS/FAIL 计数",
            "lines": "L68-L120",
            "detail": "Test-Check 包装：表数、temp_leave 不存在、status 中文字典、外键数等。",
        },
        {
            "work": "抽样演示账号与 uploads 并汇总",
            "input": "上步 SQL 结果",
            "output": "控制台 PASS=n FAIL=m；PASS=17 则 exit 0",
            "lines": "L121-L176",
            "detail": "查演示学号/管理员；验 uploads 文件；打印 PASS=17 或 exit 1。",
        },
    ],
    "DatabaseInitializer.run": [
        {
            "work": "Spring 容器启动后触发 @PostConstruct",
            "input": "Boot 完成组件扫描",
            "output": "进入 run() 方法",
            "lines": "L14-L20",
            "detail": "@PostConstruct 标注；JdbcTemplate 已注入。",
        },
        {
            "work": "检测缺表并执行 classpath 补丁 SQL",
            "input": "当前 MySQL 表结构",
            "output": "缺表时 DDL/DML 补丁；与 ps1 全量导入互补",
            "lines": "L21-L38",
            "detail": "读 resources SQL；JdbcTemplate.execute；失败则 Boot 启动失败。",
        },
    ],
}


def _norm_step_sym(symbol: str) -> str:
    return re.sub(r"[^a-z0-9.]", "", symbol.lower())


def _infer_step_io(
    idx: int,
    total: int,
    work: str,
    layer: str,
) -> tuple[str, str]:
    w = work.lower()
    if idx == 1:
        if "运维" in layer or "Ops" in layer:
            return ("用户双击 bat 或命令行调用", "环境就绪，进入下一步")
        if "表现" in layer or "Presentation" in layer:
            return ("用户点击/表单输入（ref 绑定值）", "触发本层 JS 函数或更新 computed")
        if "Controller" in layer or "接口" in layer:
            return ("HTTP 请求到达 Tomcat（路径/JSON/ Bearer JWT）", "参数绑定完成，可转发 Service")
        if "Service" in layer or "业务" in layer:
            return ("Controller 传入 DTO/基本类型", "业务校验通过，可读写 MySQL")
        return ("功能链起点：用户操作或上游表行输出", "进入本步处理")
    if idx == total:
        if "@click" in work or "调 `" in work or "调用" in work:
            return ("上一步 ref/表单已就绪", "调用本层 JS 函数，进入同链下一表行")
        if "表现" in layer:
            return ("前面 API 返回的 JSON", "页面 ref/computed 更新，用户可见结果")
        if "Controller" in layer:
            return ("Service 返回 DTO/void", "ApiResponse JSON 写回 HTTP 响应")
        if "Service" in layer:
            return ("累积 SQL/校验结果", "返回 DTO 或抛 BusinessException")
        return ("前面各步累积结果", "本符号在本层的最终产出")
    if "post " in w or "get " in w or "put " in w:
        return (f"上一步产出 + HTTP 参数（见本步 `{work[:36]}`）", "请求发出或 JSON 返回给下一步")
    if "service" in w or "controller" in w:
        return ("上一步 HTTP/调用参数", "转发至下一层或返回 DTO")
    return ("上一步输出", f"本步 `{work[:40]}` 处理结果交给下一步")


def _parse_bracket_chain(chain: str) -> list[dict[str, str]]:
    body = re.sub(r"^[^：:]*[：:]\s*", "", (chain or "").strip())
    if "→" not in body and not re.search(r"\[\d+/\d+\]", body):
        return []
    parts = [p.strip() for p in re.split(r"\s*→\s*", body) if p.strip()]
    steps: list[dict[str, str]] = []
    for p in parts:
        m = re.match(r"\[(\d+)/(\d+)\]\s*(.+)", p)
        work = m.group(3).strip() if m else p
        steps.append({"work": work, "input": "", "output": "", "lines": "", "detail": ""})
    return steps


def _parse_arrow_chain(chain: str) -> list[dict[str, str]]:
    if not chain or "→" not in chain:
        return []
    body = re.sub(r"^[^：:]*[：:]\s*", "", chain.strip())
    parts = [p.strip() for p in re.split(r"\s*→\s*", body) if p.strip()]
    if len(parts) < 2:
        return []
    return [{"work": p, "input": "", "output": "", "lines": "", "detail": ""} for p in parts]


def _split_line_range(lo: int, hi: int, n: int, idx: int) -> str:
    if n <= 1:
        return f"L{lo}–L{hi}"
    span = hi - lo + 1
    chunk = max(1, span // n)
    start = lo + idx * chunk
    end = start + chunk - 1 if idx < n - 1 else hi
    return f"L{start}–L{end}"


def resolve_chain_steps(
    symbol: str,
    chain: str,
    layer: str,
    f_code: str,
    route_hint: dict[str, str],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    sym = _norm_step_sym(symbol)
    total_io = _parse_total_io(layer, symbol, f_code, route_hint)

    steps: list[dict[str, str]] = []
    for key, val in SYMBOL_CHAIN_STEPS.items():
        if _norm_step_sym(key) == sym:
            steps = [dict(s) for s in val]
            break
    if not steps:
        steps = _parse_bracket_chain(chain)
    if not steps:
        steps = _parse_arrow_chain(chain)
    if not steps and chain.strip():
        steps = [{"work": chain.strip(), "input": "", "output": "", "lines": "", "detail": ""}]

    n = len(steps)
    for i, st in enumerate(steps):
        inf, outf = _infer_step_io(i + 1, n, st["work"], layer)
        if not (st.get("input") or "").strip():
            st["input"] = inf
        if not (st.get("output") or "").strip():
            st["output"] = outf
    return steps, total_io


def format_chain_steps_column(steps: list[dict[str, str]], total_io: dict[str, str]) -> str:
    sub = "\u00a0" * 3
    lines: list[str] = ["链中位置："]
    for i, st in enumerate(steps, 1):
        lines.append(f"{i}. {st['work']}")
        lines.append(f"{sub}输入：{st.get('input', '—')}")
        lines.append(f"{sub}输出：{st.get('output', '—')}")
    if total_io.get("input"):
        lines.append(f"总输入：{total_io['input']}")
    if total_io.get("output"):
        lines.append(f"总输出：{total_io['output']}")
    if total_io.get("fail"):
        lines.append(f"失败时：{total_io['fail']}")
    return INTRA_SEP.join(lines)


def format_impl_by_steps(
    path: str,
    symbol: str,
    steps: list[dict[str, str]],
    fallback_impl: str,
    locate: str,
) -> str:
    pf = path or symbol
    lo = hi = None
    m = re.search(r"\[L(\d+)-L(\d+)\]", locate or "")
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))

    n = len(steps)
    if n == 0:
        return fallback_impl or "见源码 【Fx-y】与 【行】 注释。"

    parts: list[str] = []
    for i, st in enumerate(steps):
        lines = st.get("lines", "")
        if not lines and lo is not None and hi is not None:
            lines = _split_line_range(lo, hi, n, i)
        detail = st.get("detail") or ""
        if not detail and i == 0 and fallback_impl and n == 1:
            detail = fallback_impl
        elif not detail:
            detail = f"见 `{pf}` {lines or '对应段'} 内 【行】 注释逐步跟读。"
        label = f"{i + 1}（{lines}）：" if lines else f"{i + 1}："
        parts.append(f"{label}{detail}")

    return INTRA_SEP.join(parts)


def build_locate_column(
    locate: str,
    layer: str,
    symbol: str,
    chain: str,
    f_code: str,
    route_hint: dict[str, str],
) -> str:
    """第二列：代码地址 + 分步链中位置 + 总输入输出。"""
    parts: list[str] = [locate.strip()]
    steps, total_io = resolve_chain_steps(symbol, chain, layer, f_code, route_hint)
    if steps:
        parts.append(format_chain_steps_column(steps, total_io))
    elif chain.strip():
        chain_one = re.sub(r"\s+", " ", chain.strip())
        parts.append(f"链中位置：{chain_one}")
        io = io_beginner_hint(layer, symbol, f_code, route_hint)
        if io:
            parts.append(io)
    else:
        io = io_beginner_hint(layer, symbol, f_code, route_hint)
        if io:
            parts.append(io)
    return INTRA_SEP.join(parts)


def expand_impl(
    locate: str,
    path: str,
    symbol: str,
    impl: str,
    chain: str = "",
    layer: str = "",
    f_code: str = "",
    route_hint: dict[str, str] | None = None,
) -> str:
    """③ 段：按链路与源码行号分步展开。"""
    steps, _ = resolve_chain_steps(
        symbol, chain, layer, f_code, route_hint or {}
    )
    if steps:
        body = format_impl_by_steps(path, symbol, steps, (impl or "").strip(), locate)
        return body

    pf = path or symbol
    impl = (impl or "").strip()
    m = re.search(r"\[L(\d+)-L(\d+)\]", locate)
    if m:
        lo, hi = m.group(1), m.group(2)
        header = f"1（L{lo}–L{hi}）："
        if impl:
            return f"{header}{impl}"
        return (
            f"{header}L{lo} 起首行 【Fx-y】 总体讲解；"
            f"L{lo}–L{hi} 内 【行】 为逐行中文注释。"
        )
    if impl:
        return impl
    return (
        f"打开 `{pf}`：首行 【Fx-y】 为总体讲解，块内 【行】 为逐行说明；"
        f"符号 `{symbol}` 的具体 API/SQL/表字段见该行号范围内注释。"
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
    chain_core = detail.get("chain", "")
    design_parts = [
        f"为何放在{layer_short_name(layer)}：{design_layer_why(layer)}",
        detail.get("design", ""),
        f"若不这样做：{design_alternative(layer, symbol)}",
    ]
    qa_parts = [detail.get("qa", "")]
    extra = extra_qa_hints(f_code, symbol, layer)
    if extra:
        qa_parts.append(extra)
    return {
        "chain": chain_core,
        "impl": expand_impl(
            locate,
            path,
            symbol,
            detail.get("impl", ""),
            chain=chain_core,
            layer=layer,
            f_code=f_code,
            route_hint=route_hint,
        ),
        "design": INTRA_SEP.join(d for d in design_parts if d),
        "qa": INTRA_SEP.join(q for q in qa_parts if q),
    }


def enrich_concepts(concepts: str, symbol: str, layer: str) -> str:
    """不再追加「本行符号」套话，避免 ① 段重复。"""
    return concepts
