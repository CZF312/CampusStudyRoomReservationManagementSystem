#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重建 01 实现定位表：
  - 第一列「所属层」：架构层 + 相关概念
  - 第二列「链路中位置与代码地址」：GitHub 行号 + 链中位置 + 输入/输出
  - 第三列「实现讲解」：③ 底层实现 · ④ 设计取舍 · ⑤ 答辩要点

用法：python scripts/rebuild_principles.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from principle_enrich import (  # noqa: E402
    INTRA_SEP,
    build_locate_column,
    enrich_detail as enrich_detail_sections,
    enrich_concepts,
)
DOC = ROOT / "docs" / "09-理解与讲解" / "01-项目理解指南.md"

OLD_LABELS = re.compile(
    r"\*\*(?:链中位置|输入输出|输入|输出|上下游|设计原因|注释导读|补充)\*\*：?"
)

# 每节功能链默认名词池（① 相关概念的基础）
SECTION_GLOSSARY: dict[str, str] = {
    "f1-1": "**start.bat**（Windows 一键入口）、**PowerShell**（跨平台脚本引擎）、**database-full.sql**（DROP 后全量导入的库快照）、**Spring Boot**（内嵌 Tomcat 的 Java 后端框架）、**study_room_reservation**（本系统 MySQL 库名）、**PASS=17**（第三版字典 17 项验收）",
    "f1-2": "**SPA 单页应用**、**REST**（资源风格 URL + HTTP 动词）、**JSON**（键值文本交换格式）、**JWT**（Header 携带的无状态令牌）、**MVC 分层**（表现/接口/业务/数据）",
    "f2-1": "**BCrypt**（不可逆密码哈希）、**JWT Bearer**（`Authorization: Bearer <token>`）、**localStorage**（浏览器持久 KV）、**user_account**（学生账号表）、**auditStatus**（待审核/已通过）、**ApiResponse**（统一 `{code,data,message}`）",
    "f2-2": "**admin_account**（管理员表）、**role**（ADMIN / SUPER_ADMIN）、**独立登录端点**（`/admin/auth/login` 与学生端分离）",
    "f2-3": "**auditStatus 待审核**、**Multipart 上传**、**registerUpload**、**BusinessException 403**（待审核不可登录）",
    "f2-4": "**student_profile**（扩展资料表）、**PUT 更新语义**、**改密强制登出**（防 token 继续可用）",
    "f3-1": "**reservation_slot**（10 分钟时间片占位）、**uk_seat_slot**（同座同片唯一）、**seat 状态**（可用/维修/禁用）、**reservation.status 待使用**",
    "f3-2": "**取消窗口**（system_config）、**credit_cancel_penalty**（默认 -50）、**releaseSlots**（释放时间片）",
    "f3-3": "**GET /reservations/my**、**轮询 refresh**（2 分钟）、**canonical 状态**（前端 PENDING→待使用）",
    "f4-1": "**checkin_record**（签到流水）、**scanCheckin**（学号/QR 解析为 12 位学号）、**status 使用中**、**信用 +5**",
    "f4-2": "**checkout**、**sign_out_time**、**studyMinutes**、**credit_log**（信用流水）、**已完成** 状态",
    "f4-3": "**@Scheduled**（Java 定时，替代 MySQL EVENT）、**已违约**、**noShow grace**、**自动签退**、**黑名单解除**",
    "f5-1": "**rangeMode**（current/past）、**statsDateWhereCondition**（与 F6.1 共用时间窗）、**bar-chart-lite**（CSS 柱图）、**studyBars computed**、**%%Y-%%m SQL 转义**",
    "f5-2": "**announcement**（全员公告）、**notification_message**（个人站内信）、**is_read**、**notifyUser**（业务触发写入）",
    "f5-3": "**feedback_ticket**（工单表）、**status 待处理/已处理**",
    "f6-1": "**JDBC 动态 SQL**（非 SELECT * FROM 视图）、**statisticsReport**、**exportCsv**、**v_room_daily_usage**（仅验收用视图，报表链不引用）",
    "f6-2": "**system_config.json**（超管可改 JSON 配置）、**最长预约时长** 等键值",
    "f6-3": "**CSV 导出**、**disable/enable**、**auditStatus 筛选**",
    "f6-4": "**study_room / seat**、**布局图 uploads**、**batchSeats**（后端有前端无）",
    "f6-5": "**revokeViolation**（撤销违约恢复信用）、**预约监管列表**",
    "f6-6": "**live-reservations**（实时列表）、**使用中/待使用** 混合看板",
    "f6-7": "**operation_log**、**admin_account CRUD**、**superadmin 专属**",
    "f7-1": "**JDBC vs JPA**（本项目选 JDBC 动态 SQL）、**DatabaseInitializer**",
    "f7-2": "**第三版中文枚举**、**无 temp_leave**、**12 位学号**、**facility 字典表**",
    "f7-3": "**reservationStatusValue**（DB 中文↔页面 canonical）、**PENDING/USING 映射**",
    "f7-4": "**16 张业务表**、**24 外键**、**ER：学生→预约→座位**",
}

# 零基础节级概念导读（① 相关概念缺符号专条时作底稿，比 SECTION_GLOSSARY 更白话）
BEGINNER_SECTION: dict[str, str] = {
    "f1-1": "**start.bat**=Windows 双击启动脚本；**PowerShell**=微软脚本语言，负责检 Java/MySQL、导入 SQL、启动 Spring Boot；**database-full.sql**=删库后整库导入的演示数据快照；**8080**=浏览器访问端口；**PASS=17**=第三版字典 17 条自动验收。",
    "f1-2": "**浏览器**=看网页的程序；**Vue**=把数据绑到页面、点按钮不发整页刷新；**HTTP**=浏览器与服务器对话的规则；**JSON**= `{键:值}` 文本格式；**REST**=用 URL 表资源、用 GET/POST 表操作；**JWT**=登录后发的加密通行证；**MySQL**=存数据的库。",
    "f2-1": "**BCrypt**=密码单向加密，库中不存明文；**JWT**=登录成功后的一串 token，以后请求 Header 带上即可证明身份；**localStorage**=浏览器本地小仓库，刷新页面 token 仍在；**user_account**=学生账号表；**auditStatus**=待审核/已通过，待审核不能登录。",
    "f2-2": "**admin_account**=管理员账号表（与学生表分开）；**role**=ADMIN 普管 / SUPER_ADMIN 超管，决定能进哪些菜单；**独立登录接口**=`/admin/auth/login` 与学生 `/auth/login` 分离。",
    "f2-3": "**注册**=INSERT 新账号且 auditStatus=待审核；**Multipart**=表单里夹 PDF 图片上传；**审核通过**=管理员改状态后小李才能 F2.1 登录。",
    "f2-4": "**student_profile**=学号以外的扩展资料表；**改密**=BCrypt 换新哈希且前端清 token 强制重新登录。",
    "f3-1": "**reservation_slot**=每 10 分钟一片的座位占位，防两人同座同时段；**reservation**=预约主表，status 从待使用→使用中→已完成；**reservation_no**=16 位预约号。",
    "f3-2": "**取消**=仅待使用可取消；**credit_cancel_penalty**=取消扣分，默认 -50 可读 system_config；**releaseSlots**=释放时间片给他人预约。",
    "f3-3": "**我的预约**=GET `/reservations/my`；**轮询**=每 2 分钟自动 refresh 列表；**canonical**=前端把中文 status 映射成 tag 颜色。",
    "f4-1": "**签到**=管理员扫 QR/输学号，写 checkin_record，预约变使用中，信用 +5；**QR**=12 位学号编码，非 GPS。",
    "f4-2": "**签退**=写 sign_out_time，status=已完成，算 studyMinutes；**credit_log**=每次加减分的流水表。",
    "f4-3": "**定时任务**=Java @Scheduled 每分钟扫库，自动违约/自动签退/解黑名单，无页面。",
    "f5-1": "**rangeMode**=当期 current（默认时间窗）/ 往期 past（自选起止日）；**studyBars**=把 API 返回 minutes 转小时画柱图；**%%Y-%%m**=Java SQL 里 `%` 要写成 `%%` 防 500。",
    "f5-2": "**announcement**=全员公告，所有人看同一份；**notification_message**=给某个 userId 的站内信，有 is_read。",
    "f5-3": "**feedback_ticket**=学生提交问题，管理员处理改 status。",
    "f6-1": "**statisticsReport**=一次 JDBC 算多图数据；**exportCsv**=与报表同 SQL 导出 CSV，避免数和图不一致。",
    "f6-2": "**system_config**=JSON 键值，如最长预约时长，超管可改。",
    "f6-3": "**用户管理**=审核/禁用/导出 CSV；**disable**=禁后无法登录。",
    "f6-4": "**study_room/seat**=自习室与座位；**uploads**=布局图文件目录。",
    "f6-5": "**revokeViolation**=撤销误违约，恢复信用。",
    "f6-6": "**live-reservations**=管理端实时看使用中/待使用预约。",
    "f6-7": "**operation_log**=管理员操作审计；**admin CRUD**=超管管管理员账号。",
    "f7-1": "**JDBC**=Java 里直接写 SQL 字符串，灵活适合报表；**JPA**=对象映射 ORM，本项目未用。",
    "f7-2": "**第三版字典**=status 等字段存中文 VARCHAR，答辩可直接读 SQL 结果。",
    "f7-3": "**reservationStatusValue**=前端工具函数，DB「待使用」↔ 页面展示文案。",
    "f7-4": "**16 表**=schema.sql 业务表；**外键**=保证 seat 属于 room 等引用完整。",
}

PRINCIPLE_SEP = "<br><br>"

# 符号级名词（① 相关概念，优先于节级 glossary，避免每行重复整节）
SYMBOL_GLOSSARY: dict[str, str] = {
    "openStudyStats": "**studentPage**（字符串路由，如 `'stats'` 表示学习统计子页，不刷新整页）· **loadStudyStats**（发 GET 拉统计数据）· **drawStudentChart**（可选 ECharts 重绘）",
    "buildStudyStatsParams": "**statPeriod**（day/week/month/year 统计粒度）· **rangeMode**（current 当期默认窗 / past 往期自选）· **startDate/endDate**（往期才带的 query 参数）",
    "loadStudyStats": "**call()**（项目统一 HTTP 封装，自动加 JWT）· **studyStats**（ref 对象，存 API 返回的 series 等）· **GET /statistics/my-study-duration**",
    "loginStudent": "**BCrypt**（密码哈希比对，明文不进库）· **JWT**（登录成功后 token 字符串）· **afterLogin**（写 localStorage 并切首页）",
    "checkout": "**签退 API** POST `/reservations/{id}/checkout` · **sign_out_time**（签退时刻）· **studyMinutes**（本次学习分钟，供 F5.1 统计）",
    "studyBars": "**computed**（依赖 studyStats.series）、**buildYearStudyBars**（年报补零月份）、**bar-chart-lite**（CSS 柱高）",
    "drawStudentChart": "**ECharts**（echarts.init）、**studentChart ref**（DOM 容器，课设主展示为 lite 柱图）",
    "stats-date-popper-single": "**teleported popper**（弹层挂 body）、**z-index**（高于柱图）、**el-date-picker type=date**",
    "stats page": "**v-if studentPage==='stats'**、**el-radio-group**（当期/往期）、**双 type=date**（起止分离）",
    "loginStudent": "**BCrypt.matches**、**JwtService.createToken**、**afterLogin**（写 token + 切页）",
    "login": "**POST /api/auth/login**、**LoginRequest DTO**、**ApiResponse.ok(tokenDto)**",
    "checkout": "**POST /reservations/{id}/checkout**、**sign_out_time**、**studyMinutes**、**status 已完成**",
    "credit": "**GET /credit/my**、**credit_score** 字段、**credit_log** 流水表",
    "loadCredit": "**credit ref**、**call('get','/credit/my')**、签退/违约后刷新展示",
    "loadNotifications": "**notification_message** 表、**is_read**、**GET /notifications/my**",
    "notifyUser": "**INSERT notification_message**、业务侧触发（预约成功等）",
    "createReservation": "**reservation_no**（16 位）、**reservation_slot** 占位、**uk_seat_slot** 唯一",
    "cancelReservation": "**credit_cancel_penalty**、**releaseSlots**、**status 已取消**",
    "scanCheckin": "**checkin_record.sign_in_time**、**status 使用中**、**credit +5**",
    "statisticsReport": "**reportType** 六种、**exportCsv** 共用 SQL、**rangeMode** 与 F5.1 对齐",
    "statsDateWhereCondition": "**LocalDate 窗口**、**current/past 分支**、**startDate/endDate 闭区间**",
    "myStudyDuration": "**statsDateWhereCondition**、**TIMESTAMPDIFF 分钟**、**series[]**、**date_format(%%Y-%%m)**",
    "main": "**SpringApplication.run**、**@SpringBootApplication**、内嵌 Tomcat 监听 8080",
    "DatabaseInitializer.run": "**@PostConstruct**、**JdbcTemplate.execute**、classpath schema 补丁",
    "start.bat": "**@echo off**、**%~dp0** 固定项目根、**ERRORLEVEL** 透传 ps1 退出码",
    "start-system.ps1": "**[1/5]–[5/5]** 五步链、**setup-after-clone.ps1** 导库、**8080 轮询**",
    "verify-v3-dictionary.ps1": "**information_schema** 验表/外键、**Test-Check**、**PASS=17**",
    "runMaintenanceTasks": "**@Scheduled** 总入口、串联 markNoShow/autoCheckout 等",
    "scheduledProcessNoShow": "**noShow grace** 宽限、**status 已违约**、**credit 扣分**",
    "scheduledProcessAutoCheckout": "**过 end_time** 自动签退、**status 已完成**",
    "scheduledProcessBlacklistRelease": "**blacklist_record** 到期解除",
    "scheduledProcessInvalidCheckin": "**异常 checkin** 数据纠正",
    "availableSeats": "**seat 状态** 过滤、**reservation_slot** 占用查询",
    "listMyReservations": "**GET /reservations/my**、**按 user_id** 列表",
    "loadMyReservations": "**call GET**、**reservations ref**、**2 分钟 refresh**",
    "loadAvailableSeats": "**GET /seats/available**、**seat 网格 ref**",
    "submitReservation": "**POST /reservations**、**确认弹窗**后提交",
    "bootstrap": "**GET /auth/me**、**localStorage token** 恢复会话",
    "doFilterInternal": "**Authorization Bearer**、**SecurityContext**、**401 JSON**",
}

# 符号级底层详解（优先于泛化模板）
SYMBOL_DETAIL: dict[str, dict[str, str]] = {
    "start.bat": {
        "chain": "用户双击后，bat 只做三件事：`cd` 到项目根、设置 `CSRRM_SCRIPT_ROOT`、以 `-ExecutionPolicy Bypass` 调用 `scripts\\start-system.ps1`，最后把 PowerShell 退出码原样返回。",
        "impl": (
            "L1–L3：@echo off、`cd /d %~dp0` 固定工作目录为 bat 所在项目根；首行 REM 含 `【F1-1】` 总体讲解。"
            "L12–L16：若找不到 `pom.xml` 则 echo 错误并 exit /b 1，防止在错误目录启动。"
            "L21–L25：`powershell -ExecutionPolicy Bypass -File scripts\\start-system.ps1`，把 ps1 退出码 `%ERRORLEVEL%` 原样返回。"
            "L27–L31：pause 保留窗口供答辩查看 PASS/FAIL 输出。"
        ),
        "design": "bat 兼容双击与答辩机无 IDE；重活交给 PowerShell（MySQL 检测、导入 SQL、mvnw）。",
        "qa": "问：为什么不用纯 PowerShell？答：双击 `.bat` 是 Windows 用户零学习成本入口；`.ps1` 默认策略可能拦截。",
    },
    "start-system.ps1": {
        "chain": "承接 bat：[1/5] 检 Java/mysql 与 static/index.html → [2/5] 启 MySQL 服务 → [3/5] 读/写 application-local.properties 密码 → [4/5] 调 setup-after-clone.ps1（DROP+导入 database-full.sql+verify PASS=17）→ [5/5] 新窗口 `mvnw spring-boot:run` 并轮询 8080。",
        "impl": "关键调用：`setup-after-clone.ps1 -SkipStart`；`Start-Process cmd /k mvnw spring-boot:run`；`Invoke-WebRequest http://localhost:8080` 最多 60 秒。环境变量 `CSRRM_MYSQL_PASSWORD` 可跳过交互。",
        "design": "导入与启动解耦：库坏了可只跑 setup；8080 已在线则跳过第二实例。",
        "qa": "问：克隆后没 Node 能跑吗？答：可以，仓库已带 `src/main/resources/static` 预构建前端。",
    },
    "loginStudent": {
        "chain": "小明点登录：模板收集 `studentLogin` → JS `loginStudent()` POST `/api/auth/login` → Controller `login` → Service 查 `user_account`（student_no）→ BCrypt 比对 → JwtService 签发 → `afterLogin` 写 localStorage 与 `studentPage='home'`。",
        "impl": "Service：`SELECT * FROM user_account WHERE student_no=?`；拦截 auditStatus≠已通过、status=禁用、blacklist；密码 `BCrypt.matches`；返回 token 载荷含 userId/role。后续请求：`call()` 自动加 `Authorization: Bearer`。",
        "design": "密码绝不明文存库；待审核在 Service 抛 403 中文 message，前端 toast。",
        "qa": "问：JWT 存在哪？答：localStorage；问：刷新为何不掉线？答：`bootstrap()` 调 GET `/auth/me` 用旧 token 恢复。",
    },
    "myStudyDuration": {
        "chain": "小明打开学习统计：`openStudyStats` → `buildStudyStatsParams`（period+rangeMode+可选起止日）→ GET `/statistics/my-study-duration` → Service 按 `statsDateWhereCondition` 拼 WHERE → JDBC 聚合 `series` → `studyBars` 转小时 → `bar-chart-lite` 渲染。",
        "impl": "统计口径：`reservation.status IN ('使用中','已完成')` 且存在签到；时长=TIMESTAMPDIFF(sign_in, sign_out 或 slot_end)。年报 GROUP BY 须写 `date_format(...,'%%Y-%%m')` 防 Java `formatted()` 把 `%Y` 当占位符（`MyStudyDurationSqlTest`）。往期 `rangeMode=past` 可带 startDate/endDate。",
        "design": "学生端两个 `type=date` + `stats-date-popper-single`，避免 daterange 双面板重叠；与管理端共用日期算法。",
        "qa": "问：有预约但年报全 0？答：查是否仅「待使用」未签到；或接口 500 看 SQL 转义；问：当期和往期区别？答：current 含今日默认窗，past 查历史自选区间。",
    },
    "createReservation": {
        "chain": "小明选座时段确认：前端 POST `/reservations`（seatId+slotStart/End）→ Service 校验信用/黑名单/时长上限 → 写 reservation + 占用 reservation_slot → notifyUser 发通知 → 返回 reservationNo。",
        "impl": "表：`reservation`（reservation_no 16 位、status=待使用）、`reservation_slot`（uk_seat_slot 防双占）；冲突则 BusinessException；读 `system_config` 最长时长与可预约天数。",
        "design": "时间片表实现并发互斥，比仅应用层锁可靠；预约号独立生成规则见 schema 注释。",
        "qa": "问：如何防两人同座同时段？答：插入 reservation_slot 时唯一键冲突即失败。",
    },
    "scanCheckin": {
        "chain": "管理员扫 QR/输学号：POST `/admin/checkin/scan`（reservationId+studentNo）→ 校验预约归属与状态=待使用 → 写 checkin_record → reservation.status=使用中 → credit +5。",
        "impl": "QR 内容为 12 位学号（前端 `createQrSvg` 本地生成，非后端 qrcode 接口）；`checkin_record.sign_in_time=NOW()`；INSERT credit_log reason=签到奖励。",
        "design": "签到仅管理员端操作，防学生远程伪造 GPS；信用即时写入可 F4.2/F5 统计。",
        "qa": "问：为何不用摄像头实时扫？答：课设采用拍照/选图+jsQR，降低浏览器权限复杂度（见 F8）。",
    },
    "statisticsReport": {
        "chain": "管理员统计页：`loadAdminStatistics` GET `/admin/statistics/report` → `statisticsReport` 一次调 usage/peak/trend/credit 四段 JDBC → ECharts 渲染；导出走 `/admin/statistics/export?reportType=` 同一 Service 方法拼 CSV。",
        "impl": "非 `SELECT * FROM v_room_daily_usage`；动态 SQL 按 period、rangeMode、roomId（普管仅本室）拼接；6 种 reportType：usage/peak/reservation/activity/studyDuration/credit。",
        "design": "report 与 export 共用算法，避免「图一套数、CSV 另一套数」；视图仅验收展示今日使用率。",
        "qa": "问：报表从视图来吗？答：不是，AppService JDBC 现算；视图只有 v_room_daily_usage 且管理端报表链未引用。",
    },
    "checkout": {
        "chain": "小明使用中点签退：POST `/reservations/{id}/checkout` → Service 写 sign_out_time、status=已完成、算 studyMinutes → 前端刷新信用与预约列表。",
        "impl": "UPDATE reservation SET status='已完成', sign_out_time=NOW()；TIMESTAMPDIFF 分钟写入返回 DTO；releaseSlots 释放 reservation_slot；可触发 F5.1 可统计时长。",
        "design": "签退才计入学习统计；仅待使用不算时长，答辩常考点。",
        "qa": "问：不签退会怎样？答：F4.3 定时 autoCheckout 过 end_time 自动已完成。",
    },
    "cancelReservation": {
        "chain": "小明取消待使用预约：POST `/reservations/{id}/cancel` → 校验状态与时间窗 → 扣分写 credit_log → releaseSlots。",
        "impl": "status 改已取消；读 system_config 的 credit_cancel_penalty（默认 -50，见 F8 与需求差异）；仅待使用可取消。",
        "design": "取消惩罚在 Service 可读配置，非写死 SQL。",
        "qa": "问：30 分钟内扣 10 分？答：代码默认 50，以 system_config 为准（F8 对照表）。",
    },
    "bootstrap": {
        "chain": "页面 mounted：若 localStorage 有 token 则 GET `/auth/me` 恢复 user，否则回登录页。",
        "impl": "`call('get','/auth/me')`；成功则填充 user/studentPage；401 则 clearToken。",
        "design": "刷新不掉线，演示体验好；token 无效必须清本地缓存。",
        "qa": "问：Session 存在哪？答：无服务端 Session，仅 JWT+localStorage。",
    },
    "doFilterInternal": {
        "chain": "除 login/register 外，每个 `/api/**` 请求先经此过滤器解析 Bearer，再进 Controller。",
        "impl": "读 Header Authorization；JwtService.parse；设 SecurityContext userId/role；失败 401 JSON。",
        "design": "统一鉴权，Controller 用 @AuthenticationPrincipal 取当前用户。",
        "qa": "问：哪些接口免鉴权？答：登录注册与 static 资源，见 SecurityConfig 白名单。",
    },
    "auditUser": {
        "chain": "管理员点通过：POST `/admin/users/{id}/approve` → auditStatus=已通过 → 小李可走 F2.1 登录。",
        "impl": "UPDATE user_account SET audit_status='已通过'；写 operation_log；拒绝/禁用走 reject/disable 分支。",
        "design": "注册与登录解耦，人工审核合规课设流程。",
        "qa": "问：待审核能登录吗？答：不能，loginStudent 抛 403 中文提示。",
    },
    "DatabaseInitializer": {
        "chain": "Spring Boot 启动后 @PostConstruct/run：若表不存在则执行 classpath schema 补丁（与 database-full.sql 导入互补）。",
        "impl": "读 resources 下 SQL；JdbcTemplate 执行 DDL/DML；与 clone 后 ps1 全量导入分工：ps1 负责演示数据，Initializer 负责增量迁移。",
        "design": "Java 侧可版本化补丁，不必每次手动改 SQL 文件。",
        "qa": "问：数据从哪来？答：答辩机以 start.bat 导入 database-full.sql 为主；Initializer 防表缺失。",
    },
    "verify-v3-dictionary.ps1": {
        "chain": "setup-after-clone 导入后自动调用：17 项 CHECK（16 表、无 temp_leave、中文字典、演示账号、uploads 文件等）。",
        "impl": "mysql 客户端执行 information_schema 与抽样 SELECT；输出 PASS/FAIL 计数；失败 exit 1。",
        "design": "答辩前一条命令验第三版规范，不需打开数据库客户端。",
        "qa": "问：PASS=17 是什么？答：第三版字典 17 条验收，见脚本内注释与 F7.2。",
    },
    "loadNotifications": {
        "chain": "小明打开通知：`loadNotifications` GET `/notifications/my` → 写入 notifications ref → 模板 v-for 展示未读角标。",
        "impl": "L2717–2719 `call('get','/notifications/my')`；响应含 id/title/content/isRead/createdAt；首页 L60–68 公告区另走 announcement 接口。",
        "design": "公告（全员）与通知（个人）分表分接口，避免一条 SQL 混读权限。",
        "qa": "问：预约成功怎么收到通知？答：Service createReservation 内调 notifyUser INSERT notification_message。",
    },
    "notifyUser": {
        "chain": "业务事件（预约成功/审核通过等）在 Service 内调用，向指定 userId 写一条站内信。",
        "impl": "INSERT INTO notification_message(user_id,title,content,is_read,created_at) VALUES(...,0,NOW())；无 WebSocket，前端轮询或进入页时 loadNotifications。",
        "design": "同步写入，课设规模够用；未做推送以降低复杂度。",
        "qa": "问：实时吗？答：非实时；我的预约页 2 分钟 refresh 或手动刷新可见新通知。",
    },
    "loadCredit": {
        "chain": "签退/违约/取消后前端刷新：GET `/credit/my` → credit ref → 首页/我的页展示分数。",
        "impl": "L2698–2700；SELECT credit_score FROM user_account WHERE id=?；与 credit_log 流水展示可分开接口。",
        "design": "信用权威在后端 user_account.credit_score，前端只展示不计算。",
        "qa": "问：分数怎么变？答：签到+5、取消扣分、违约扣分等见 credit_log reason 字段。",
    },
    "registerStudent": {
        "chain": "小李注册：模板填表 → POST `/auth/register` + Multipart 证件 → auditStatus=待审核 → 不可 F2.1 登录直至 F2.3 审核。",
        "impl": "INSERT user_account + student_profile；BCrypt 哈希密码；registerUpload 存 uploads/；login 时 auditStatus≠已通过抛 403。",
        "design": "注册与登录分离，人工审核符合课设流程。",
        "qa": "问：待审核能登录吗？答：不能，Service 抛 BusinessException 403 中文提示。",
    },
    "statsDateWhereCondition": {
        "chain": "myStudyDuration 与 statisticsReport 共用：按 period+rangeMode(+可选 start/end) 生成 SQL WHERE 片段与 bind 参数列表。",
        "impl": "current：日=今日、周=近7天含今日、月=本月、年=年初至今；past：日=过去7天不含今日、周=上周期、月=近12月、年=闭区间或全部历史；返回 List<Object> params。",
        "design": "一处维护时间窗，F5.1 学生端与 F6.1 管理端数字一致，答辩可对照两节。",
        "qa": "问：为何抽成方法？答：避免四段报表 SQL 各写一套日期逻辑导致口径不一致。",
    },
    "autoCheckout": {
        "chain": "F4.3 定时：@Scheduled 扫描 end_time 已过且仍「使用中」的预约 → 自动签退 → status=已完成。",
        "impl": "ScheduledTaskService；UPDATE reservation SET sign_out_time=end_time, status='已完成' WHERE ...；releaseSlots；不计额外信用。",
        "design": "替代 MySQL EVENT，逻辑在 Java 便于调试与单测。",
        "qa": "问：学生忘记签退？答：定时任务按预约结束时刻补签退，时长仍计入 F5.1。",
    },
    "markNoShow": {
        "chain": "定时：待使用且超过 grace 未签到 → status=已违约 → 扣分 → 可能触发黑名单。",
        "impl": "读 system_config no_show_grace_minutes；UPDATE reservation；INSERT credit_log；notifyUser 可选。",
        "design": "违约与取消不同状态，监管端 F6.5 可 revokeViolation 撤销。",
        "qa": "问：grace 多长？答：system_config 可配，默认见 schema 与 F8 对照。",
    },
    "exportCsv": {
        "chain": "管理端点导出：GET `/admin/statistics/export?reportType=&period=&rangeMode=` → 与 statisticsReport 同 SQL → text/csv 流。",
        "impl": "AppService.exportCsv 调 statisticsReport 同源 JDBC；HttpServletResponse 写 BOM+header；6 种 reportType 与图表一致。",
        "design": "导出与图表共用算法，答辩「数和图对不上」不成立。",
        "qa": "问：CSV 从视图来吗？答：否，与 F6.1 一样现算 JDBC。",
    },
    "revokeViolation": {
        "chain": "超管/普管撤销违约：POST `/admin/reservations/{id}/revoke-violation` → 恢复信用 → status 回待使用或已取消视规则。",
        "impl": "UPDATE reservation + user_account.credit_score + INSERT credit_log reason=撤销违约；写 operation_log。",
        "design": "人工纠错通道，避免误违约永久黑。",
        "qa": "问：谁可操作？答：管理端 F6.5，需 ADMIN JWT。",
    },
    "reservationStatusValue": {
        "chain": "前端 canonical：DB 中文 status ↔ 页面展示/筛选枚举（PENDING→待使用、USING→使用中）。",
        "impl": "App.vue 工具函数 reservationStatusValue/toReservationStatus；F7.3 字典与 schema CHECK 一致。",
        "design": "第三版存中文 VARCHAR，前端映射便于 Element tag 颜色。",
        "qa": "问：为何不全用英文 enum？答：第三版规范要求中文状态便于 SQL 肉读与答辩。",
    },
    "createToken": {
        "chain": "loginStudent 校验通过后：Service 调 JwtService.createToken(userId, role) 生成 HS256 签名字符串。",
        "impl": "claims 含 sub=userId、role=STUDENT；secret 来自 application.properties jwt.secret；exp 默认 24h；返回 compact JWT 字符串给 Controller 包装进 data.token。",
        "design": "签发集中在一处，Filter 与 Service 共用同一 JwtService 解析/验证逻辑。",
        "qa": "问：token 里存密码吗？答：不存，只存 userId 与 role 等非敏感 claims。",
    },
    "afterLogin": {
        "chain": "loginStudent 收到 token 后：写 token/role ref 与 localStorage → toast → bootstrap(false) 拉 /auth/me 补全用户信息 → 切 studentPage。",
        "impl": "L2491–2498：`localStorage.setItem('token',t)`；`await bootstrap(false)` 不再跳登录页；me ref 存昵称/学号等展示字段。",
        "design": "前端会话状态双写 ref+localStorage，刷新时 bootstrap 读 localStorage 恢复。",
        "qa": "问：为何还要 bootstrap？答：token 只含 id/role，展示名等从 /auth/me 拉最新 profile。",
    },
    "me": {
        "chain": "bootstrap 或登录后：GET `/auth/me`（Bearer）→ 本方法取 SecurityContext userId → Service 查 user_account 返回 DTO。",
        "impl": "`@GetMapping(\"/auth/me\")`；需 JWT；return ApiResponse.ok(service.getCurrentUser(userId))；含 studentNo/name/creditScore/auditStatus 等。",
        "design": "「我是谁」只读接口，支撑刷新恢复与 header 展示，不写库。",
        "qa": "问：与 login 区别？答：login 验密签发 token；me 只解析已有 token 返回资料。",
    },
    "ok": {
        "chain": "几乎所有 Controller 成功路径：`return ApiResponse.ok(data)` 统一 `{code:200, message:'ok', data:...}`。",
        "impl": "静态工厂 `ApiResponse.ok(T data)` 设 code=200；Jackson 序列化为 JSON；前端 call() 判断 res.code===200 取 data。",
        "design": "业务错误也常用 200+code≠200 或 BusinessExceptionHandler，login 失败 message 中文可读。",
        "qa": "问：为何不用 HTTP 4xx 表示业务失败？答：课设统一 JSON 包装，前端只解析 body.code/message。",
    },
    "main": {
        "chain": "mvnw spring-boot:run 入口：SpringApplication.run 启动内嵌 Tomcat、扫描 @Component、挂载 static 与 /api。",
        "impl": "CampusStudyRoomReservationManagementSystemApplication.main；@SpringBootApplication 含 @EnableScheduling（F4.3 定时）；默认 port 8080。",
        "design": "标准 Boot 单 jar 部署，答辩机只需 Java+MySQL。",
        "qa": "问：前端怎么访问？答：同端口 8080，/ 返回 index.html，/api 进 Controller。",
    },
    "confirmCheckout": {
        "chain": "小明「使用中」点签退：若无 activeReservation 则 return；否则 openModalConfirm 弹窗，确认后调 doCheckout。",
        "impl": "L2393–2397 `【F4-2】`；genericModal 复用确认框；onConfirm=doCheckout；不直接 POST。",
        "design": "二次确认防误触释放座位；表现层只弹窗+回调，不算时长。",
        "qa": "问：为何分 confirm 与 do？答：UI 确认与 HTTP 提交分离，逻辑清晰可测。",
    },
    "doCheckout": {
        "chain": "确认后 POST `/reservations/${id}/checkout` → 弹 checkoutSummary（分钟数）→ loadReservations + loadCredit 刷新列表与分数。",
        "impl": "L2399–2411；data.actualMinutes 来自 Service TIMESTAMPDIFF；checkoutModalOpen 展示 room/seat；catch 用 notify 显示 message。",
        "design": "签退后立即刷新 F3.3 我的预约与 F4.2 信用，用户可见「已完成」。",
        "qa": "问：creditChange 写死 +5？答：展示文案；实际签到 +5 已在 F4.1 写入 credit_log。",
    },
    "loginAdmin": {
        "chain": "管理员 tab 输入账号密码 → POST `/admin/auth/login` → afterLogin(token,'ADMIN',info) → adminPage 切 dashboard。",
        "impl": "L2474–2489 `【F2-2】`；adminLoginForm ref；与学生 loginStudent 分表单分 endpoint；role 写 ADMIN/SUPER_ADMIN。",
        "design": "学生与管理员 JWT role 不同，后端 Security 可限制 /admin/** 仅 ADMIN。",
        "qa": "问：同一浏览器能同时登学生和管理员吗？答：会覆盖 localStorage token，演示时分开浏览器或先 logout。",
    },
    "adminLogin": {
        "chain": "POST `/admin/auth/login`：查 admin_account 表 BCrypt 比对 → 签发 role=ADMIN 的 JWT。",
        "impl": "`@PostMapping(\"/admin/auth/login\")`；Service.loginAdmin；白名单免 JWT；返回 token+admin 信息。",
        "design": "与学生 user_account 分表，避免学号与工号混用同一 login SQL。",
        "qa": "问：superadmin 怎么区分？答：admin_account.role=SUPER_ADMIN，前端部分菜单 v-if 控制。",
    },
    "readNotification": {
        "chain": "小明点一条通知：PUT `/notifications/{id}/read` → 本地 isRead=true → 角标减一。",
        "impl": "L2725–2728；call('put',...)；UPDATE notification_message SET is_read=1 WHERE id=? AND user_id=?。",
        "design": "已读状态持久化，刷新后仍显示已读样式。",
        "qa": "问：公告需要已读吗？答：announcement 全员公告无 is_read  per user；notification 才 per user。",
    },
    "readAllNotifications": {
        "chain": "通知页点「全部已读」：PUT `/notifications/read-all` → 批量 UPDATE is_read=1 → 刷新列表。",
        "impl": "L2730–2733；一条 SQL WHERE user_id=?；前端 notifications ref 全置 isRead。",
        "design": "批量操作减少逐条点击，课设 UX 基本需求。",
        "qa": "问：未读数怎么算？答：前端 computed 过滤 isRead=false 或接口返回 unreadCount。",
    },
    "saveAnnouncement": {
        "chain": "管理员编辑公告点保存：POST/PUT `/admin/announcements` → INSERT/UPDATE announcement 表 → 学生首页 loadAnnouncements 可见。",
        "impl": "前端 L3266–3272 收集 title/content/priority；Service L1071–1085 JDBC 写 announcement(published_at, author_id)；status=已发布。",
        "design": "公告写 admin 端、读 student 端 GET `/announcements` 公开列表，无 JWT 或学生 JWT 均可读。",
        "qa": "问：会推送到 notification 吗？答：本课设公告与站内信分表，发布公告不自动 notifyUser 全员。",
    },
    "loadAnnouncements": {
        "chain": "学生首页 mounted：GET `/announcements` → announcements ref → L60–68 卡片 v-for 展示标题与摘要。",
        "impl": "SELECT * FROM announcement WHERE status='已发布' ORDER BY published_at DESC LIMIT N；无 userId 过滤。",
        "design": "全员可见，与 notification_message 个人消息分离。",
        "qa": "问：过期公告？答：schema 可含 expire_at，Service 可加 WHERE 过滤（见实现行号）。",
    },
    "register": {
        "chain": "小李填表+上传 PDF → POST `/auth/register` Multipart → auditStatus=待审核 → 尝试 login 得 403 待审核提示。",
        "impl": "前端 L2501+ 校验 12 位学号；FormData 含 registerUpload；Service INSERT user_account+profile；密码 BCrypt 哈希。",
        "design": "注册成功不等于可登录，须 F2.3 管理员 approve。",
        "qa": "问：PDF 存哪？答：UploadController 存 uploads/ 目录，路径写 student_profile 字段。",
    },
    "loadMyReservations": {
        "chain": "小明进「我的预约」：GET `/reservations/my` → reservations ref → 卡片展示 status canonical 颜色。",
        "impl": "call 带 JWT；Service SELECT reservation JOIN seat/room WHERE user_id=? ORDER BY start_time DESC；2 分钟 setInterval refresh（F3.3）。",
        "design": "轮询简单可靠，课设未上 WebSocket。",
        "qa": "问：状态中文还是英文？答：DB 中文，前端 reservationStatusValue 映射 tag 类型。",
    },
    "releaseSlots": {
        "chain": "取消/签退/违约后：DELETE 或 UPDATE reservation_slot 释放座位时间片，供他人预约。",
        "impl": "AppService 内部方法；DELETE FROM reservation_slot WHERE reservation_id=?；与 uk_seat_slot 配合防脏占。",
        "design": "时间片与 reservation 生命周期绑定，状态终态必须释放。",
        "qa": "问：不释放会怎样？答：座位仍显示被占，其他人无法预约该时段。",
    },
    "ScheduledTaskService": {
        "chain": "Spring @Scheduled 定时（如每分钟）：依次 markNoShow、autoCheckout、解除过期黑名单等 F4.3 维护。",
        "impl": "ScheduledTaskService 类；cron/fixedRate 见注解；每项调 AppService  package-private 方法；无 UI。",
        "design": "用 Java 定时替代 MySQL EVENT，逻辑可调试、与业务 Service 复用 SQL。",
        "qa": "问：服务停掉定时还跑吗？答：不跑，必须 Boot 进程在线；答辩说明演示机需保持 8080 运行。",
    },
}

# F1.2 八卡概念专用（零基础详尽五段；段间 <br><br>，段内 <br> 分条）
CONCEPT_CARDS: dict[str, str] = {
    "Browser 浏览器": (
        "**① 相关概念**：**浏览器**=Chrome/Edge 等看网页的程序；**HTTP**=浏览器向服务器「要页面/要数据」的协议；**localhost:8080**=本机 Spring Boot 地址。<br>"
        "**本行符号**：浏览器是整个系统的「入口」，用户所有操作从这里开始。<br><br>"
        "**② 链路与职责**：【本节一条龙】小明点确认预约 → 浏览器发 HTTP → 后端写库 → 浏览器显示结果。<br>"
        "【零基础·你能看到的层】双击 start.bat 后访问 `http://localhost:8080`，Tomcat 返回 `index.html`，再加载 JS，Vue 画出登录页。<br>"
        "**本行在链中的位置**：没有浏览器就没有「用户」；F1.2 八卡第一环。<br>"
        "**输入**：用户打开 URL。**输出**：渲染页面。**失败时**：8080 未启动则无法访问。<br><br>"
        "**③ 底层实现**：**怎么读代码**：静态资源在 `src/main/resources/static/`；`/` 映射到 index.html。<br>"
        "**技术细节**：Vite 打包的 `assets/index-*.js` 含整个 Vue；与 `/api` 同源无需 CORS。<br><br>"
        "**④ 设计取舍**：**为何同端口 8080**：答辩只开一个端口；clone 后无需 Node 也能跑预构建 static。<br>"
        "**若不这样做**：前后端 dev 需 5173+8080 两端口，答辩易忘开前端。<br><br>"
        "**⑤ 答辩要点**：问：怎么访问？答：浏览器打开 8080。<br>"
        "问：为什么要浏览器？答：Web 系统，所有交互经 HTTP，浏览器是客户端。"
    ),
    "Vue 单页框架": (
        "**① 相关概念**：**Vue**=数据 ref 变则页面自动变；**SPA**=切换子页不整页刷新；**ref/computed**=响应式变量。<br>"
        "**本行符号**：Vue 管「页面长什么样、点按钮调哪个函数」。<br><br>"
        "**② 链路与职责**：点确认预约 → Vue 收集 form → call() POST → 改列表展示。<br>"
        "【零基础·表现层】`studentPage='reservation'` 显示选座；`'home'` 显示首页，URL 仍是 `/`。<br>"
        "**输入**：点击与表单。**输出**：改 ref 或发 HTTP。**失败时**：ElMessage 提示。<br><br>"
        "**③ 底层实现**：读 `frontend/src/App.vue`；搜 studentPage 看子页切换；Element Plus 组件库。<br>"
        "**技术细节**：Vue3 Composition API；课设用字符串路由未上 Vue Router。<br><br>"
        "**④ 设计取舍**：**为何单文件 App.vue**：子页有限，答辩找代码快；字符串路由比 Router 配置直观。<br>"
        "**若不这样做**：多文件跳转讲解预约链路过散。<br><br>"
        "**⑤ 答辩要点**：问：为何叫单页？答：只加载一次 HTML，之后 Vue 改 DOM。<br>"
        "问：Vue 与后端分工？答：Vue 管界面；算信用写库在后端。"
    ),
    "HTTP 请求": (
        "**① 相关概念**：**GET**=取数据；**POST**=提交；**Header**=如 Authorization Bearer token；**axios**=发 HTTP 的库。<br>"
        "**本行符号**：HTTP 是浏览器与 Spring Boot 的对话语言。<br><br>"
        "**② 链路与职责**：call('post','/reservations') → Tomcat → Controller → Service → JSON 响应。<br>"
        "【零基础·表现层】Network 面板可见 `/api/...`；body.code=200 为业务成功。<br>"
        "**输入**：method、path、body、JWT。**输出**：JSON。**失败时**：401/403 或 message 中文错误。<br><br>"
        "**③ 底层实现**：App.vue 搜 function call；baseURL `/api`；自动加 Bearer。<br>"
        "**技术细节**：Content-Type application/json；Spring @RequestBody 转 DTO。<br><br>"
        "**④ 设计取舍**：**为何封装 call()**：统一 token、统一解析 code、统一 toast。<br>"
        "**若不这样做**：漏 JWT 会已登录仍 401。<br><br>"
        "**⑤ 答辩要点**：问：API 前缀？答 `/api`，例 `http://localhost:8080/api/auth/login`。<br>"
        "问：GET vs POST？答：GET 查，POST 改状态/创建。"
    ),
    "JSON 数据格式": (
        "**① 相关概念**：**JSON**=`{\"键\":值}` 文本；**DTO**=传输结构；**Jackson**=Java 自动转 JSON。<br>"
        "**本行符号**：前后端只通过 JSON 交换数据。<br><br>"
        "**② 链路与职责**：登录 body 含 studentId/password → 响应 `{code:200,data:{token}}`。<br>"
        "【零基础·表现层】前端 res.data 即 ApiResponse 的 data 字段。<br>"
        "**输入**：JS 对象。**输出**：JSON 字符串。**失败时**：message 中文（如待审核）。<br><br>"
        "**③ 底层实现**：Java `ApiResponse.java`；Controller return ApiResponse.ok(...)。<br>"
        "**技术细节**：camelCase 字段名；中文 status 为字符串。<br><br>"
        "**④ 设计取舍**：**为何统一包装**：前端只判 code===200；message 人类可读。<br>"
        "**若不这样做**：各接口返回形态不一，前端难维护。<br><br>"
        "**⑤ 答辩要点**：问：成功标志？答：JSON 的 code=200，非仅 HTTP 200。<br>"
        "问：密码会回传吗？答：不会，仅 token 与摘要。"
    ),
    "REST API": (
        "**① 相关概念**：**REST**=URL 表资源、HTTP 动词表操作；如 POST /reservations 创建。<br>"
        "**本行符号**：REST 是本系统 URL 设计原则。<br><br>"
        "**② 链路与职责**：GET 查、POST 建/改状态；管理员路径带 /admin/。<br>"
        "【零基础·接口层】AppController `@RequestMapping(\"/api\")` + 方法级 @PostMapping。<br>"
        "**输入**：路径/query/body。**输出**：ApiResponse JSON。<br><br>"
        "**③ 底层实现**：AppController.java 搜 @PostMapping；方法常一行 return service.xxx()。<br>"
        "**技术细节**：/auth/login 白名单免 JWT。<br><br>"
        "**④ 设计取舍**：**Controller 极薄**：证明有接口；规则在 Service。<br>"
        "**若不这样做**：Controller 写 SQL 定时任务无法复用。<br><br>"
        "**⑤ 答辩要点**：问：是 REST 吗？答：资源风格 URL+动词，课设级足够。<br>"
        "问：取消为何 POST 非 DELETE？答：课设统一 POST 改状态，与 call 封装一致。"
    ),
    "Service 业务层": (
        "**① 相关概念**：**Service**=业务规则；**JdbcTemplate**=执行 SQL；**BusinessException**=业务失败中文提示。<br>"
        "**本行符号**：Service 决定「能不能预约、扣多少分」。<br><br>"
        "**② 链路与职责**：Controller 调 service.createReservation → 校验 → INSERT 表 → notifyUser。<br>"
        "【零基础·业务层】「能不能做」必须在这里，不在 Vue。<br>"
        "**输入**：userId、seatId 等。**输出**：DTO/void + 库变更。**失败时**：throw BusinessException。<br><br>"
        "**③ 底层实现**：AppService.java 按方法名搜；SQL 用 ? 占位防注入。<br>"
        "**技术细节**：credit_log 流水；中文 status。<br><br>"
        "**④ 设计取舍**：**为何 JDBC 非 JPA**：动态报表 SQL 多，答辩可指字符串（F7.1）。<br>"
        "**若不这样做**：复杂统计难讲清 SQL。<br><br>"
        "**⑤ 答辩要点**：问：SQL 在哪？答：AppService 对应方法或 GitHub【行】注释旁。<br>"
        "问：定时任务也用 Service？答：是，F4.3 与 Controller 共用规则。"
    ),
    "MySQL 数据库": (
        "**① 相关概念**：**表**=数据集合；**行**=一条记录；**外键**=引用完整性；**InnoDB**=事务引擎。<br>"
        "**本行符号**：MySQL 持久化全部业务数据。<br><br>"
        "**② 链路与职责**：Service 执行 SQL → MySQL 存取 → 映射 Java 对象。<br>"
        "【零基础·数据层】start.bat 导入 database-full.sql，库名 study_room_reservation。<br>"
        "**输入**：SQL+参数。**输出**：结果集/影响行数。**失败时**：唯一键冲突等转 BusinessException。<br><br>"
        "**③ 底层实现**：schema.sql 看 DDL；database-full.sql 看演示数据。<br>"
        "**技术细节**：16 表；reservation+reservation_slot 防双占。<br><br>"
        "**④ 设计取舍**：**中文 status**：SQL 结果答辩可直接读（F7.2）。<br>"
        "**若不这样做**：英文 ENUM 答辩易口误。<br><br>"
        "**⑤ 答辩要点**：问：几表？答：16 业务表 + 1 验收视图。<br>"
        "问：数据从哪来？答：start.bat 导入 + DatabaseInitializer 补丁。"
    ),
    "JWT 令牌": (
        "**① 相关概念**：**JWT**=三段 Base64；**Bearer**=Authorization Header；**无 Session**=服务端不存会话表。<br>"
        "**本行符号**：JWT 是登录后的通行证。<br><br>"
        "**② 链路与职责**：login → createToken → localStorage → 每请求 Bearer → Filter 解析 userId。<br>"
        "【零基础·配置层】除登录外 `/api/**` 先过 JwtAuthFilter。<br>"
        "**输入**：userId/role。**输出**：token 串。**失败时**：401 清 token 回登录。<br><br>"
        "**③ 底层实现**：JwtService 签发/解析；JwtAuthFilter；jwt.secret 在 properties。<br>"
        "**技术细节**：HS256；payload 无密码；默认 24h 过期。<br><br>"
        "**④ 设计取舍**：**JWT 非 Session**：SPA 友好、Tomcat 无状态。<br>"
        "**若不这样做**：Session 需 sticky/Redis，答辩配置重。<br><br>"
        "**⑤ 答辩要点**：问：token 存哪？答：localStorage。<br>"
        "问：logout？答：前端删 token；无黑名单则到期前仍有效。"
    ),
}


def normalize_concepts(text: str) -> str:
    """相关概念列：去掉所有 ** 加粗，保留反引号代码。"""
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", text.strip())
    if "<br" not in s.lower():
        s = re.sub(r"\s+", " ", s).strip(" ；;")
    return s


def strip_old_principle(text: str) -> str:
    m = re.search(r"\*\*② 链路与职责\*\*：(.+?)(?:\*\*③|$)", text, re.S)
    if m:
        text = m.group(1)
    s = OLD_LABELS.sub(" ", text)
    s = re.sub(r"\*\*[①②③④⑤][^*]*\*\*：?", " ", s)
    s = re.sub(r"链中位置：|输入：|输出：|失败时：", " ", s)
    s = re.sub(r"\s+", " ", s).strip(" ;；")
    return s


def extract_symbol(locate: str) -> str:
    """优先取定位列中第一对反引号内的函数/模块/脚本名。"""
    ticks = [m.group(1).strip() for m in re.finditer(r"`([^`]+)`", locate)]
    for inner in ticks:
        if re.search(r"\.(vue|java|sql|css|html|js)$", inner, re.I):
            continue
        if "/" in inner:
            inner = inner.split("/")[-1]
        if inner.lower() not in ("vue", "java", "js", "css"):
            return inner
    if ticks:
        return ticks[0].split("/")[-1]
    parts = [p.strip() for p in locate.split("·")]
    for p in parts:
        if "`" in p or "[" in p or "http" in p or not p:
            continue
        if "frontend/" in p or "controller/" in p or "service/" in p:
            continue
        return p.strip()[:36]
    return "本行"


def extract_path(locate: str) -> str:
    for p in ("App.vue", "AppService.java", "AppController.java", "start.bat", "schema.sql", "styles.css"):
        if p in locate:
            return p
    m = re.search(r"`([^`]+\.(?:java|vue|ps1|bat|sql|css|html))`", locate)
    return m.group(1) if m else ""


def condense_chain_text(old: str, max_len: int = 380) -> str:
    s = re.sub(r"\s+", " ", old).strip(" ；;")
    if len(s) > max_len:
        return s[: max_len - 1] + "…"
    return s


def lookup_detail(symbol: str, layer: str, locate: str) -> dict[str, str] | None:
    sym = symbol.lower().replace(" ", "")
    # 模板/页面行（无独立函数名或含「模板区」）
    if "模板" in locate or re.search(r"\bpage\b", locate, re.I) or " cards" in locate.lower() or "公告区" in locate:
        if "stats" in locate.lower() or "统计" in locate:
            return {
                "chain": "小明 `studentPage='stats'` 时渲染的唯一页面：当期/往期 Tab、往期双单日历与快捷按钮、日报～年报 Tab、汇总三卡与 bar-chart-lite。",
                "impl": "模板 L266–330：`v-if=\"studentPage==='stats'\"`；绑定 studyStatsRangeMode/statPeriod/studyStats；`@change` 触发 loadStudyStats；L267 `【F5-1】` 总体讲解。",
                "design": "弃用 daterange，两个 type=date + stats-date-popper-single，从 UI 层消除图层重叠。",
                "qa": "问：为何柱图不用 ECharts 为主？答：lite 柱图 CSS 足够答辩；drawStudentChart 保留扩展。",
            }
        if "login" in locate.lower() or "登录" in locate:
            return {
                "chain": "小明输入学号密码点登录：模板 v-model 绑定 studentLogin → @click 调 loginStudent()。",
                "impl": "el-form + el-input；L2457–2472 `【F2-1】`；不含 BCrypt，仅收集 studentId/password 字段。",
                "design": "表现层零业务：密码强度/审核状态全在后端 Service。",
                "qa": "问：前端校验什么？答：非空与格式；密码对错由 BCrypt 在后端比对。",
            }
        if "通知" in locate:
            return {
                "chain": "小明 `studentPage='notifications'`：v-for 渲染 notifications ref，点击单条调 readNotification，顶部按钮 readAllNotifications。",
                "impl": "模板 L321–331；mounted 时 loadNotifications；el-badge 未读角标；`【F5-2】` 总体讲解。",
                "design": "列表 UI 与已读逻辑分离到 JS 函数，模板只绑事件。",
                "qa": "问：公告在哪看？答：首页 L60–68 公告卡片，与本通知页不同数据源。",
            }
        if "公告" in locate and "管理" in locate:
            return {
                "chain": "管理员 adminPage 公告管理：表单编辑 title/content → 点保存调 saveAnnouncement → 列表刷新。",
                "impl": "模板 L508–517；v-model announcementForm；表格 v-for adminAnnouncements。",
                "design": "管理端 CRUD UI，与学生端只读公告区分权限。",
                "qa": "问：学生会即时看到吗？答：保存后写 announcement 表，学生 refresh 首页即可。",
            }
        if "公告" in locate:
            return {
                "chain": "学生首页顶部：mounted loadAnnouncements → v-for 展示最新公告卡片，点击可看详情。",
                "impl": "L60–68；announcements ref；GET `/announcements` 无 user 过滤。",
                "design": "全员公告区与 personal notification 分区展示，降低认知负担。",
                "qa": "问：未登录能看公告吗？答：视 Security 白名单，通常首页需登录后进入。",
            }
        if "预约" in locate or "reservation" in locate.lower():
            return {
                "chain": "小明选自习室/时段/座位：`studentPage='reserve'` 模板展示 room 列表、快捷时段按钮、座位网格，@click 触发 loadAvailableSeats / submitReservation。",
                "impl": "L100–161 `【F3-1】`；v-model reservationForm；seat 网格 :class 绑定可用/占用/维修；确认弹窗后 POST /reservations。",
                "design": "预约 UI 与 F3.3 我的预约分离 studentPage，减少单页状态交叉。",
                "qa": "问：灰色座位什么意思？答：维修/禁用或已被 reservation_slot 占用，Service availableSeats 过滤。",
            }
        if "我的预约" in locate or "myres" in locate.lower():
            return {
                "chain": "小明查看预约列表：v-for reservations，按 status 显示签退/取消按钮，使用中显示倒计时。",
                "impl": "L232–237 `【F3-3】`；reservationStatusValue 映射 tag 颜色；2 分钟 refresh 轮询。",
                "design": "列表与 F3.1 预约页分模板，状态驱动按钮显隐。",
                "qa": "问：为何轮询？答：管理员签到后 status 变使用中，学生端需 refresh 见变化。",
            }
    if sym in ("createtoken",):
        return SYMBOL_DETAIL.get("createToken")
    if sym in ("afterlogin",):
        return SYMBOL_DETAIL.get("afterLogin")
    if sym == "me":
        return SYMBOL_DETAIL.get("me")
    if sym == "ok":
        return SYMBOL_DETAIL.get("ok")
    if sym == "main":
        return SYMBOL_DETAIL.get("main")
    if sym in ("confirmcheckout",):
        return SYMBOL_DETAIL.get("confirmCheckout")
    if sym in ("docheckout",):
        return SYMBOL_DETAIL.get("doCheckout")
    if sym in ("loginadmin",):
        return SYMBOL_DETAIL.get("loginAdmin")
    if sym in ("adminlogin",):
        return SYMBOL_DETAIL.get("adminLogin")
    if sym in ("readnotification",):
        return SYMBOL_DETAIL.get("readNotification")
    if sym in ("readallnotifications",):
        return SYMBOL_DETAIL.get("readAllNotifications")
    if sym in ("loadannouncements",):
        return SYMBOL_DETAIL.get("loadAnnouncements")
    if sym in ("loadmyreservations",):
        return SYMBOL_DETAIL.get("loadMyReservations")
    if sym in ("register",) and "Service" not in layer:
        return SYMBOL_DETAIL.get("register")
    if sym == "saveannouncement":
        if "Service" in layer or "业务" in layer:
            d = dict(SYMBOL_DETAIL["saveAnnouncement"])
            d["impl"] = "Service L1071–1085：INSERT/UPDATE announcement(title,content,priority,status,author_id,published_at)；JdbcTemplate；写 operation_log。"
            return d
        return SYMBOL_DETAIL.get("saveAnnouncement")
    if sym == "scancheckin":
        if "Service" in layer or "业务" in layer:
            return {
                "chain": "Controller 转发后：按 reservationId+studentNo 查预约 → 校验 status=待使用、学号匹配、时间窗 → 写 checkin_record → UPDATE 使用中 → credit+5。",
                "impl": "L989–1057 AppService；INSERT checkin_record；UPDATE reservation SET status='使用中'；UPDATE user_account credit_score+=5；INSERT credit_log。",
                "design": "全部业务规则与 SQL 在 Service，管理员 UI 只传 id 与学号。",
                "qa": "问：能替别人签到吗？答：Service 校验 studentNo 与预约 user_id 一致。",
            }
        if "Controller" in layer or "接口" in layer:
            return {
                "chain": "POST `/admin/checkin/scan`：body 含 reservationId+studentNo → 转发 Service.scanCheckin。",
                "impl": "`@PostMapping(\"/admin/checkin/scan\")`；需 ADMIN JWT；return ApiResponse.ok(dto)。",
                "design": "管理端专属路径 /admin/checkin，与学生端隔离。",
                "qa": "问：为何 admin 路径？答：签到由管理员操作，防学生远程伪造。",
            }
        return SYMBOL_DETAIL.get("scanCheckin")
    if sym in ("mystudyduration", "mystudy-duration"):
        if "Controller" in layer or "接口" in layer:
            return {
                "chain": "JWT 鉴权通过后，Controller 将 query 参数 `period`、`rangeMode`、`startDate`、`endDate` 原样传入 Service，返回 `ApiResponse.ok(Map)`。",
                "impl": "`@GetMapping(\"/statistics/my-study-duration\")`；方法签名绑定 CurrentUser + 四个 query；无业务 if，一行 return service.myStudyDuration(...)。",
                "design": "HTTP 适配与业务分离；参数名与前端 buildStudyStatsParams、管理端 F6.1 完全一致。",
                "qa": "问：为何不在 Controller 写 SQL？答：统计口径复杂且 F6.1 复用，必须集中在 AppService.statsDateWhereCondition。",
            }
        return SYMBOL_DETAIL.get("myStudyDuration")
    if sym == "statsdatewherecondition":
        return SYMBOL_DETAIL.get("statsDateWhereCondition")
    if sym in ("loadnotifications",):
        return SYMBOL_DETAIL.get("loadNotifications")
    if sym in ("loadcredit",):
        return SYMBOL_DETAIL.get("loadCredit")
    if sym in ("notifyuser",):
        return SYMBOL_DETAIL.get("notifyUser")
    if sym in ("registerstudent", "register"):
        if "Service" in layer:
            return SYMBOL_DETAIL.get("registerStudent")
    if sym in ("exportcsv",):
        return SYMBOL_DETAIL.get("exportCsv")
    if sym in ("revokeviolation",):
        return SYMBOL_DETAIL.get("revokeViolation")
    if sym in ("autocheckout",):
        return SYMBOL_DETAIL.get("autoCheckout")
    if sym in ("marknoshow", "noshow"):
        return SYMBOL_DETAIL.get("markNoShow")
    if "reservationstatusvalue" in sym:
        return SYMBOL_DETAIL.get("reservationStatusValue")
    if sym in ("statsdatepopper-single", "stats-date-popper-single") or "popper-single" in locate:
        return {
            "chain": "两个 el-date-picker 的 teleported 弹层挂载到 body，本 CSS 类保证只显示单月历且 z-index 高于柱图。",
            "impl": "`.stats-date-popper-single{z-index:5000;background:#fff}`；`.el-date-picker{width:322px}`；与 `.stats-date-popper`（756px daterange）分离。",
            "design": "学生端起止分离选型下的样式配套，避免再出现双面板重叠。",
            "qa": "问：为何不用 Element 默认样式？答：默认 teleported 弹层会与 bar-chart 层叠穿透，需 fixed+白底。",
        }
    if "学习统计页" in locate or sym == "statspage" or symbol == "stats page":
        return {
            "chain": "小明 `studentPage='stats'` 时渲染的唯一页面：当期/往期 Tab、往期双单日历与快捷按钮、日报～年报 Tab、汇总三卡与 bar-chart-lite。",
            "impl": "模板 L266–330：`v-if=\"studentPage==='stats'\"`；绑定 studyStatsRangeMode/statPeriod/studyStats；`@change` 触发 loadStudyStats；L267 `【F5-1】` 总体讲解。",
            "design": "弃用 daterange，两个 type=date + stats-date-popper-single，从 UI 层消除图层重叠。",
            "qa": "问：为何柱图不用 ECharts 为主？答：lite 柱图 CSS 足够答辩；drawStudentChart 保留扩展。",
        }
    if sym == "openstudystats":
        return {
            "chain": "侧栏/我的页点击后：`studentPage='stats'` → await `loadStudyStats()` → `drawStudentChart()`。",
            "impl": "L2743 `【F5-1】`；L2744 改 studentPage；L2745 GET；L2746 重绘。无参，读全局 ref。",
            "design": "每次进入强制拉数，避免签退前旧缓存。",
            "qa": "问：为何不缓存上次统计？答：签退后时长变化，必须重新 GET。",
        }
    if sym == "buildstudystatsparams":
        return {
            "chain": "把 `statPeriod`、`studyStatsRangeMode`、可选起止日期 ref 组装为 axios params。",
            "impl": "返回 `{period, rangeMode}`；往期且两端日期齐全时附加 startDate/endDate；L2144–2149 逐行 `// 【行】`。",
            "design": "参数名与 F6.1、后端 statsDateWhereCondition 一致。",
            "qa": "问：当期为何不带日期？答：后端按默认时间窗计算，无需 query。",
        }
    if sym in ("applystudystatsshortcut", "applystudystatsshortcut/起止日期变更"):
        return {
            "chain": "往期下：快捷按钮或 `onStudyStatsStartDateChange`/`onStudyStatsEndDateChange` 写入 ref → `normalizeStudyStatsDateRange` → `loadStudyStats`。",
            "impl": "`studyStatsRangeTouched=true` 防 sync 覆盖；shortcut.value() 返回 [start,end]；L2158–2182。",
            "design": "起止分离选择器，各弹单月历，配合 normalize 纠正逆序。",
            "qa": "问：为何要 Touched 标记？答：防止 API 回写 startDate 覆盖用户手选区间。",
        }
    if sym == "changestudystatsrangemode":
        return {
            "chain": "Tab 点击切换 current/past：past 可保留日期；切回 current 清空起止日与 Touched。",
            "impl": "L2184 `【F5-1】`；await loadStudyStats + drawStudentChart；mode 写入 studyStatsRangeMode ref。",
            "design": "当期不传 startDate/endDate，后端走默认窗；往期才启用自定义区间。",
            "qa": "问：切当期会丢往期日期吗？答：ref 清空，但可再通过快捷按钮选区间。",
        }
    if sym == "loadstudystats":
        return {
            "chain": "全链数据枢纽：`call('get','/statistics/my-study-duration',{params: buildStudyStatsParams()})` → 写入 studyStats → sync 起止日回显。",
            "impl": "响应字段 series/periodLabel/rangeWindowLabel/studyDayCount/startDate/endDate；L2701–2704。",
            "design": "统一 call() 带 JWT 与全局错误 toast。",
            "qa": "问：统计含哪些预约？答：使用中/已完成且已签到，见 Service SQL 口径。",
        }
    if sym == "studybars" or "buildyearstudybars" in sym:
        return {
            "chain": "computed `studyBars`：把 series.minutes 转小时；年报/往期月报走 buildYearStudyBars 补零月份。",
            "impl": "L1649 computed；L2229 buildYearStudyBars 按 startDate/endDate 或默认年窗循环月份；模板 L317 v-for。",
            "design": "前端补零使柱图连续，SQL 不必 LEFT JOIN 日历表。",
            "qa": "问：为何 API 不补零？答：减少 payload，展示层补全更灵活。",
        }
    if sym == "drawstudentchart":
        return {
            "chain": "可选 ECharts：nextTick 后 init studentChart ref，setOption 用 studyBars 的 label/value。",
            "impl": "L3386–3397；课设主展示为 bar-chart-lite，本函数为扩展预留。",
            "design": "演示以 CSS 柱图为主，降低 ECharts 依赖讲解成本。",
            "qa": "问：页面上看不到 ECharts？答：可能未绑 ref，lite 柱图仍正常显示数据。",
        }
    # checkout：Controller 与 Service 分层描述
    if sym == "checkout":
        if "Controller" in layer or "接口" in layer:
            return {
                "chain": "小明点签退：前端 POST `/api/reservations/{id}/checkout`（JWT）→ 本方法取 path id + CurrentUser → 一行转发 Service.checkout。",
                "impl": "`@PostMapping(\"/reservations/{id}/checkout\")`；参数 reservationId + @AuthenticationPrincipal userId；return ApiResponse.ok(service.checkout(id, userId))；无 SQL。",
                "design": "REST 资源动词 checkout 挂在预约 id 下；鉴权在 Filter，Controller 不重复验归属。",
                "qa": "问：为何 path 带 id？答：REST 风格，一条预约一次签退，Service 内再验 userId 归属。",
            }
        return SYMBOL_DETAIL.get("checkout")
    if sym == "credit":
        if "Controller" in layer or "接口" in layer:
            return {
                "chain": "前端 GET `/credit/my` → 本方法取 CurrentUser → 返回当前 credit_score 与近期流水摘要。",
                "impl": "`@GetMapping(\"/credit/my\")`；return service.getMyCredit(userId)；DTO 含 score 与 logs 列表。",
                "design": "读操作无 side effect，适合 GET；分数变更只在签退/取消/违约等 POST 业务里发生。",
                "qa": "问：信用存在哪张表？答：user_account.credit_score 权威值，credit_log 存每次变动流水。",
            }
    if sym == "login" or sym == "loginstudent":
        if "模板" in locate or "登录页" in locate or "login page" in locate.lower():
            return {
                "chain": "小明输入学号密码点登录：模板 v-model 绑定 studentLogin → @click 调 loginStudent()。",
                "impl": "el-form + el-input；L 行见 GitHub `【F2-1】`；不含 BCrypt，仅收集 JSON 字段 studentId/password。",
                "design": "表现层零业务：密码强度/审核状态全在后端 Service。",
                "qa": "问：前端校验什么？答：非空与格式；密码对错由 BCrypt 在后端比对。",
            }
        if "Controller" in layer or "接口" in layer:
            return {
                "chain": "POST `/api/auth/login`：@RequestBody LoginRequest → service.loginStudent → 返回 token DTO。",
                "impl": "`@PostMapping(\"/auth/login\")`；白名单免 JWT；return ApiResponse.ok(jwtService...)；HTTP 200 即使业务 403 也在 body.code。",
                "design": "登录端点独立白名单；与学生/管理员分路径见 F2.2。",
                "qa": "问：登录失败 HTTP 码？答：多数仍 200，message 中文说明；403 待审核见 Service 抛错。",
            }
        if sym == "loginstudent" or ("Service" in layer and sym == "login"):
            if "Service" in layer or "业务" in layer:
                return {
                    "chain": "Controller 传入 LoginRequest：SELECT user_account BY student_no → 校验 auditStatus=已通过、非禁用、非黑名单 → BCrypt.matches → createToken。",
                    "impl": "L184–207 AppService；失败抛 BusinessException(403/401) 中文 message；成功 Map 含 token 与 user 摘要。",
                    "design": "所有登录安全策略集中 Service，Controller 与 adminLogin 共用 JwtService。",
                    "qa": "问：密码怎么存？答：user_account.password_hash BCrypt，永不回传明文。",
                }
            if "表现" in layer:
                return {
                    "chain": "async loginStudent()：读 studentLogin ref → call('post','/auth/login') → afterLogin(token,'STUDENT',data)。",
                    "impl": "L2457+ JS 函数；authLoading 防重复提交；catch notify(e.message) 显示待审核等后端文案。",
                    "design": "JS 不解析 JWT，只存字符串；角色由 login 响应 role 字段决定。",
                    "qa": "问：remember me？答：课设未做，token 存 localStorage 即持久登录。",
                }
            return SYMBOL_DETAIL.get("loginStudent")
    if symbol in SYMBOL_DETAIL:
        return SYMBOL_DETAIL[symbol]
    for key, val in SYMBOL_DETAIL.items():
        if key.lower() == sym or (len(key) > 4 and key in locate):
            return val
    return None


# Controller 符号 → API 路径（infer 兜底用）
ROUTE_HINT: dict[str, str] = {
    "rooms": "GET /api/rooms",
    "availableSeats": "GET /api/seats/available",
    "createReservation": "POST /api/reservations",
    "myReservations": "GET /api/reservations/my",
    "cancel": "POST /api/reservations/{id}/cancel",
    "cancelReservation": "POST /api/reservations/{id}/cancel",
    "changePassword": "POST /api/auth/change-password",
    "profile": "PUT /api/student/profile",
    "updateProfile": "PUT /api/student/profile",
    "auditUser": "POST /api/admin/users/{id}/approve",
    "approve": "POST /api/admin/users/{id}/approve",
    "statisticsReport": "GET /api/admin/statistics/report",
    "exportCsv": "GET /api/admin/statistics/export",
    "loadAdminStatistics": "GET /api/admin/statistics/report",
}


def line_ref(locate: str) -> str:
    m = re.search(r"\[L(\d+)", locate)
    return f"GitHub L{m.group(1)} 起 `【Fx-y】`+`【行】`" if m else "定位列 GitHub 链接"


def infer_detail(
    f_code: str, story: str, layer: str, symbol: str, locate: str
) -> dict[str, str]:
    """无 SYMBOL_DETAIL 时，按层级+故事+路由推断五段原理，避免「见定位列」空泛描述。"""
    sym = symbol.lower()
    story_snip = condense_chain_text(story, 100) or "见本节功能链实例"
    lr = line_ref(locate)
    layer_short = layer.split("·")[0].strip()

    if "Controller" in layer or "接口" in layer:
        route = ROUTE_HINT.get(symbol) or ROUTE_HINT.get(sym, f"/api/...（见 AppController `{symbol}`）")
        svc = symbol if sym not in ("cancel", "profile") else {
            "cancel": "cancelReservation",
            "profile": "updateProfile",
        }.get(sym, symbol)
        return {
            "chain": (
                f"浏览器已带 JWT 发 HTTP 到 `{route}` → 进入 `{symbol}` 方法 → "
                f"Spring 自动把 JSON/query 绑成 Java 参数 → 调用 `service.{svc}(...)` → "
                f"把 Service 返回值包进 ApiResponse 写回浏览器。"
            ),
            "impl": (
                f"{lr}：`@RestController` 类；本方法 `@GetMapping`/`@PostMapping` 等注解即 URL 路径；"
                f"方法体通常仅 `return ApiResponse.ok(service.{svc}(...))`，不含 SQL；"
                f"当前用户从 `@AuthenticationPrincipal` 或 SecurityContext 取 userId。"
            ),
            "design": "Controller 像「前台接待」：只懂 HTTP，不懂预约规则；所有 if/else 与 SQL 在 Service，定时任务也能调同一 Service。",
            "qa": f"问：`{symbol}` 有多厚？答：答辩可指行号证明几乎只有一行 return service；问：会做鉴权吗？答：JwtAuthFilter 在进 Controller 前已完成，本方法只取已解析的 userId。",
        }
    if "Service" in layer or "业务" in layer:
        if sym.startswith("scheduledprocess") or sym == "runmaintenancetasks":
            scheduled_chain = {
                "runmaintenancetasks": "ScheduledTaskService @Scheduled 入口：依次调 AppService 内 package 维护方法（无 HTTP）。",
                "scheduledprocessnoshow": "扫「待使用且过 grace 未签到」→ status=已违约 → 扣分写 credit_log。",
                "scheduledprocessautocheckout": "扫「使用中且已过 end_time」→ 写 sign_out_time → status=已完成。",
                "scheduledprocessblacklistrelease": "扫 blacklist_record 到期行 → 解除限制。",
                "scheduledprocessinvalidcheckin": "纠正无效/异常 checkin_record 与预约状态不一致。",
            }
            return {
                "chain": scheduled_chain.get(sym, f"`{symbol}`：F4.3 定时维护，@Scheduled 触发，无 Controller。"),
                "impl": f"{lr}：`AppService.{symbol}` 或 ScheduledTaskService；JdbcTemplate UPDATE/INSERT；status 须为 schema 中文枚举。",
                "design": "Java @Scheduled 替代 MySQL EVENT/触发器，逻辑可调试、答辩可指 AppService 行号。",
                "qa": "问：关掉 8080 还跑吗？答：不跑，定时随 JVM；演示需保持 CSRRMS-Backend 窗口在线。",
            }
        if "databaseinitializer" in sym:
            return {
                "chain": "Spring Boot 启动后 @PostConstruct：若 classpath 补丁 SQL 对应表缺失则执行 DDL（与 database-full.sql 全量导入互补）。",
                "impl": f"{lr}：DatabaseInitializer.run 读 resources SQL；JdbcTemplate.execute；不负责造演示数据。",
                "design": "答辩机以 start.bat → database-full.sql 为主；Initializer 防表结构缺失。",
                "qa": "问：数据从哪来？答：database-full.sql 整库导入；Initializer 只做结构补丁。",
            }
        tables = SECTION_GLOSSARY.get(f_code, "").split("、")[0:3]
        table_hint = "、".join(tables) if tables else "user_account/reservation/checkin_record 等"
        return {
            "chain": (
                f"Controller 把参数传入 `{symbol}` → 本方法先业务校验（状态对不对、是不是本人、信用够不够）→ "
                f"通过则 JdbcTemplate 执行 INSERT/UPDATE/SELECT → 必要时写 credit_log 或 notifyUser → "
                f"返回 Map/DTO 给 Controller。"
            ),
            "impl": (
                f"{lr}：`AppService.{symbol}` 内 SQL 字符串 + `jdbcTemplate.query/update`；"
                f"常见表 {table_hint}；status 字段值必须与 schema.sql 第三版中文 CHECK 一致；"
                f"失败 `throw new BusinessException(\"中文原因\")`，不会返回 half-done 数据。"
            ),
            "design": "业务规则只写一份在 Service：Controller、@Scheduled、导出 CSV 都调这里，改规则不会漏改某一层。",
            "qa": f"问：为何不用 JPA？答：F6.1/F5.1 动态 SQL 多，JDBC 字符串答辩时可逐行指；问：`{symbol}` 会事务回滚吗？答：关键写操作在 Spring @Transactional 边界内（见方法注解）。",
        }
    if "表现" in layer or "Presentation" in layer:
        verb = "GET" if sym.startswith("load") or sym.startswith("fetch") else "POST/PUT"
        path_guess = ROUTE_HINT.get(symbol, ROUTE_HINT.get(sym, "/api/..."))
        if sym.startswith("load"):
            path_guess = path_guess.replace("GET ", "")
        return {
            "chain": (
                f"用户操作（点击/切换 Tab/提交表单）触发 `{symbol}` → 改 Vue ref（如 loading=true）→ "
                f"`await call('{verb.lower()}', '{path_guess}', ...)` 发 HTTP → "
                f"收到 JSON 后写入 ref/computed → 模板自动刷新 DOM；全程不直连 MySQL。"
            ),
            "impl": (
                f"{lr}：`App.vue` 中 async function 或模板 `@click`/`@change`；"
                f"`call()` 从 localStorage 取 token 加 Authorization Bearer；"
                f"成功取 res.data，失败 notify/ElMessage 显示后端 message；块首 `【Fx-y】` 讲整体，块内 `【行】` 逐行。"
            ),
            "design": "前端是「遥控器」：只发请求和展示；信用、时长、status 权威值以后端为准，避免换浏览器结果不一致。",
            "qa": f"问：为何 `{symbol}` 不算信用/时长？答：安全与一致性；分数在 user_account，由 Service 改，前端只 GET 展示。",
        }
    if "配置" in layer or "Config" in layer:
        return {
            "chain": f"「{story_snip}」→ `{symbol}`：Spring 配置/安全组件，被 Filter 或 Service 注入调用。",
            "impl": f"{lr}：见 config 包；与 application.properties 密钥/白名单配合。",
            "design": "横切关注点（JWT/安全）抽离 config，Controller 不写鉴权 if。",
            "qa": f"问：`{symbol}` 谁调用？答：见本表上下行 Controller/Filter 链路。",
        }
    if "运维" in layer or ".ps1" in locate or ".bat" in locate:
        return {
            "chain": f"「{story_snip}」→ `{symbol}`：脚本/启动链一步，失败 exit 非 0 向上传递。",
            "impl": f"{lr}：PowerShell/bat 逐行 `【行】`；MySQL 用 mysql.exe；Java 用 mvnw。",
            "design": "运维与业务代码分离，clone 后双击 start.bat 即可答辩。",
            "qa": "问：脚本做什么？答：建库导入 database-full.sql、verify PASS=17、启动 8080。",
        }
    return {
        "chain": f"「{story_snip}」→ `{symbol}`（{layer_short}）：见 {lr} 与上下表行衔接。",
        "impl": f"{lr}：首行 `【Fx-y】` 总体讲解，随后每 executable 行 `【行】` 中文注释。",
        "design": "与 F1.2 分层一致，职责边界见模块总览表。",
        "qa": f"问：这一行在故事哪步？答：对照本节功能链实例顺序，符号 `{symbol}` 所在行。",
    }


def _norm_sym(symbol: str) -> str:
    return re.sub(r"[^a-z0-9]", "", symbol.lower())


def _strip_bold(text: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", text or "")


# 每行所属层「相关概念」：从链路+实现中提取并零基础引入（优先于 pick_glossary）
ROW_CONCEPTS: dict[str, str] = {
    "start.bat": (
        "`@echo off`=关闭命令回显；`%~dp0`=bat 所在目录即项目根；"
        "`pom.xml`=Maven 项目标志，防在错误目录启动；"
        "`PowerShell`=执行 .ps1 的 Windows 脚本引擎；"
        "`ERRORLEVEL`=透传 ps1 退出码给 pause；`pause`=答辩时保留窗口看 PASS/FAIL"
    ),
    "start-system.ps1": (
        "`Java/JDK`=运行 Spring Boot 后端的程序；"
        "`MySQL`=关系型数据库，存预约与用户；"
        "`index.html`=static 下预构建的前端登录页（HTML）；"
        "`Spring Boot`=`mvnw spring-boot:run` 启动的内嵌 Tomcat Web 框架；"
        "`application-local.properties`=本地 MySQL 密码配置文件；"
        "`setup-after-clone.ps1`=DROP 库并导入 database-full.sql 的子脚本；"
        "`database-full.sql`=整库演示数据快照；"
        "`PASS=17`=第三版字典 17 项验收；"
        "`8080`=浏览器访问端口；`mvnw`=Maven Wrapper"
    ),
    "verify-v3-dictionary.ps1": (
        "`information_schema`=MySQL 系统库，查表数/外键；"
        "`Test-Check`=脚本内 PASS/FAIL 计数；"
        "`PASS=17`=第三版验收标准；`mysql.exe`=命令行连库执行 SQL"
    ),
    "DatabaseInitializer.run": (
        "`@PostConstruct`=Spring Boot 启动后自动执行；"
        "`JdbcTemplate`=Java 里执行 SQL 的工具；"
        "`classpath` SQL=jar 内补丁脚本；与 database-full.sql 全量导入互补"
    ),
    "loginStudent": (
        "`BCrypt`=密码单向哈希，库中不存明文；"
        "`JWT`=登录成功后的 token；"
        "`localStorage`=浏览器存 token；"
        "`user_account`=学生账号表；`auditStatus`=待审核/已通过"
    ),
    "createReservation": (
        "`reservation`=预约主表；`reservation_slot`=10 分钟占位表；"
        "`uk_seat_slot`=唯一索引防两人同座同时段；"
        "`reservation_no`=16 位预约号"
    ),
    "myStudyDuration": (
        "`statsDateWhereCondition`=统计时间窗 SQL 条件；"
        "`TIMESTAMPDIFF`=MySQL 算学习分钟；"
        "`rangeMode`=当期 current / 往期 past"
    ),
    "statisticsReport": (
        "`JDBC 动态 SQL`=Java 字符串拼 SELECT，非查视图；"
        "`statisticsUsage`=各室使用率；`exportCsv`=与报表同 SQL 导出"
    ),
}

# 在链路/实现文本中扫描到的关键词 → 零基础一句（长模式优先）
CONCEPT_SCAN: list[tuple[str, str]] = [
    ("application-local.properties", "`application-local.properties`=本地数据源密码配置"),
    ("database-full.sql", "`database-full.sql`=整库演示数据快照"),
    ("setup-after-clone", "`setup-after-clone.ps1`=导库子脚本"),
    ("spring-boot:run", "`Spring Boot`=内嵌 Tomcat 的 Java Web 框架"),
    ("index.html", "`index.html`=浏览器入口 HTML 页"),
    ("static/index", "`static/`=Spring Boot 托管的前端资源目录"),
    ("information_schema", "`information_schema`=MySQL 元数据，验表/外键"),
    ("reservation_slot", "`reservation_slot`=10 分钟座位占位"),
    ("uk_seat_slot", "`uk_seat_slot`=唯一索引，防抢座双占"),
    ("@postconstruct", "`@PostConstruct`=容器启动后自动执行"),
    ("@transactional", "`@Transactional`=事务，失败整组回滚"),
    ("@scheduled", "`@Scheduled`=Java 定时任务"),
    ("jdbctemplate", "`JdbcTemplate`=Spring 执行 SQL"),
    ("bcrypt", "`BCrypt`=密码哈希"),
    ("localstorage", "`localStorage`=浏览器存 token"),
    ("pass=17", "`PASS=17`=第三版 17 项验收"),
    ("mvnw", "`mvnw`=Maven Wrapper"),
    ("8080", "`8080`=浏览器访问端口"),
    ("pom.xml", "`pom.xml`=Maven 项目标志"),
    ("@echo off", "`@echo off`=bat 关闭回显"),
    ("errorlevel", "`ERRORLEVEL`=命令退出码"),
    ("powershell", "`PowerShell`=Windows 脚本引擎"),
    ("mysql", "`MySQL`=关系型数据库"),
    ("spring boot", "`Spring Boot`=Java Web 后端框架"),
    ("vue", "`Vue`=前端单页框架"),
    ("rest", "`REST`=URL+HTTP 动词"),
    ("json", "`JSON`={键:值} 文本格式"),
    ("jwt", "`JWT`=登录通行证 token"),
    ("apiresponse", "`ApiResponse`={code,data,message} 统一响应"),
    ("echarts", "`ECharts`=图表库"),
    ("element plus", "`Element Plus`=Vue UI 组件库"),
    ("java", "`Java`=后端运行时"),
]


def build_row_concepts(
    symbol: str,
    chain: str,
    locate: str,
    impl: str,
    layer: str,
    f_code: str,
) -> str:
    """所属层相关概念：链路与实现中出现的关键名词，零基础引入。"""
    parts: list[str] = []
    seen: set[str] = set()

    def add(chunk: str) -> None:
        c = chunk.strip().strip("；")
        if not c:
            return
        key = c.split("=", 1)[0].strip() if "=" in c else c
        if key in seen:
            return
        seen.add(key)
        parts.append(c)

    sym_norm = _norm_sym(symbol)
    for key, val in ROW_CONCEPTS.items():
        if key.lower() == symbol.lower() or _norm_sym(key) == sym_norm:
            for seg in val.split("；"):
                add(seg)
            break

    blob = " ".join([chain or "", locate or "", impl or ""]).lower()
    for pat, intro in CONCEPT_SCAN:
        if pat in blob:
            add(intro)

    if len(parts) < 3:
        fallback = pick_glossary(f_code, symbol, layer, locate)
        for seg in re.split(r"[；、]", fallback):
            add(seg)

    return "<br>".join(parts[:8])


def minimal_concept(symbol: str, layer: str) -> str:
    hints = {
        "表现": "前端 UI/事件",
        "Presentation": "前端 UI/事件",
        "Controller": "REST 接口转发",
        "接口": "REST 接口转发",
        "Service": "业务规则与 SQL",
        "业务": "业务规则与 SQL",
        "Config": "JWT/安全配置",
        "配置": "JWT/安全配置",
        "运维": "启动/导库脚本",
        "Ops": "启动/导库脚本",
        "样式": "CSS 布局",
    }
    for k, v in hints.items():
        if k in layer:
            return f"`{symbol}`={v}"
    return f"`{symbol}`=见链中位置与 GitHub 【行】"


def pick_glossary(f_code: str, symbol: str, layer: str, locate: str = "") -> str:
    sym = symbol.lower().replace(" ", "")
    sym_norm = _norm_sym(symbol)

    # 模板行：按页面类型区分，不用整节 glossary
    if "模板" in locate or "page" in sym or "首页" in symbol or "公告区" in symbol:
        if "stats" in locate.lower() or "统计" in locate:
            return "**v-if**、**el-radio-group**（当期/往期）、**type=date**、**bar-chart-lite**"
        if "login" in locate.lower() or "登录" in locate:
            return "**v-model**、**el-form**、**@click → loginStudent**"
        if "公告" in locate or "announcement" in locate.lower():
            return "**announcement** 表、**v-for** 卡片、**loadAnnouncements**"
        if "预约" in locate or "reserve" in locate.lower():
            return "**studentPage='reserve'**、**seat 网格**、**loadAvailableSeats**"
        if "我的预约" in locate:
            return "**v-for reservations**、**status tag**、**refresh 轮询**"
        return "**Vue 模板** + **Element Plus**（本块 UI 结构）"

    # 符号级精确匹配（仅全键相等，禁止子串误伤）
    for key, val in SYMBOL_GLOSSARY.items():
        if key.lower() == sym or _norm_sym(key) == sym_norm:
            return val

    # 方法/脚本精确表（小写键）
    METHOD_EXACT: dict[str, str] = {
        "loginstudent": "**BCrypt.matches**、**createToken**、**afterLogin**",
        "loginadmin": "**admin_account**、**/admin/auth/login**",
        "login": "**POST /auth/login**、**LoginRequest**、**ApiResponse**",
        "registerstudent": "**auditStatus 待审核**、**Multipart 材料**",
        "register": "**POST /auth/register**、**BCrypt 哈希入库**",
        "createreservation": "**reservation_no**、**INSERT slot**、**uk_seat_slot**",
        "cancelreservation": "**releaseSlots**、**credit_cancel_penalty**、**已取消**",
        "availabeseats": "**WHERE 可用 seat**、**排除 slot 占用**",
        "scancheckin": "**checkin_record**、**status 使用中**、**credit +5**",
        "checkout": "**sign_out_time**、**studyMinutes**、**已完成**",
        "docheckout": "**POST checkout**、**call()** 触发",
        "confirmcheckout": "**确认弹窗**、**使用中才可签退**",
        "statisticsreport": "**reportType 六种**、**动态 JOIN SQL**",
        "exportcsv": "**与 report 同 SQL**、**text/csv 响应**",
        "mystudyduration": "**statsDateWhereCondition**、**TIMESTAMPDIFF**、**series[]**",
        "statsdatewherecondition": "**current/past 时间窗**、**LocalDate 闭区间**",
        "revokeviolation": "**恢复 credit**、**撤销违约标记**",
        "audituser": "**auditStatus 已通过**、**operation_log**",
        "saveannouncement": "**INSERT/UPDATE announcement**",
        "loadadminstatistics": "**GET statistics/report**、**ECharts 四块**",
    }
    if sym_norm in METHOD_EXACT:
        return METHOD_EXACT[sym_norm]

    # 窄域匹配（仅当 sym 以关键词开头或完全相等）
    if sym in ("checkout", "docheckout", "confirmcheckout") or sym.startswith("checkout"):
        return SYMBOL_GLOSSARY.get("checkout", METHOD_EXACT["checkout"])
    if sym in ("credit", "loadcredit"):
        return "**credit_score**、**credit_log**、**GET /credit/my**"
    if sym in ("loadnotifications", "readnotification", "readallnotifications", "notifyuser"):
        return SYMBOL_GLOSSARY.get(sym, "**notification_message**、**is_read**")
    if sym.startswith("scheduledprocess") or sym == "runmaintenancetasks":
        for key, val in SYMBOL_GLOSSARY.items():
            if _norm_sym(key) == sym_norm:
                return val
    if sym.startswith("stat") or "studystats" in sym or "studybar" in sym or "popper" in sym:
        return "**rangeMode**、**statPeriod**、**studyStats ref**、**studyBars**"

    # 禁止 fallback 到整节 BEGINNER_SECTION
    return minimal_concept(symbol, layer)


def generic_impl(layer: str, symbol: str, path: str, locate: str) -> str:
    if "App.vue" in path or "App.vue" in locate:
        return (
            f"Vue 单文件 `frontend/src/App.vue`：跳转首行 `【F*】` 总体讲解，块内 `// 【行】` 或 `<!-- 【行】 -->` 逐行说明。"
            f"本符号 `{symbol}` 通过 ref/computed 与模板 `@click/@change` 绑定；HTTP 统一经 `call()` 发 `/api` 请求。"
        )
    if "AppService" in path or "Service" in layer:
        return (
            f"`AppService.{symbol}`：JdbcTemplate 执行参数化 SQL；业务异常 `BusinessException` 转 JSON message；"
            f"涉及表见本节功能链（常见 reservation/user_account/checkin_record/credit_log）。中文 status 与 schema 字典一致。"
        )
    if "Controller" in layer or "AppController" in path:
        return (
            f"`AppController` 映射 `/api/...`：方法参数由 Spring 自动绑定 JSON/query；返回 `ApiResponse.ok(dto)`；"
            f"鉴权依赖上游 JwtAuthFilter 解析的 CurrentUser/@AuthenticationPrincipal。"
        )
    if "Jwt" in symbol or "Filter" in symbol:
        return "Spring Security 过滤器链：解析 Authorization Bearer → 校验签名与过期 → 写入 SecurityContext → 后续 Controller 取 userId。"
    if "schema.sql" in path:
        return "DDL 定义表结构、索引、外键与 CHECK；第三版中文枚举注释见文件头 `【F7-2】`；导入走 database-full.sql 全量快照。"
    if "styles.css" in path:
        return "全局 CSS：`.stats-date-popper-single` 等修复 Element Plus teleported 弹层 z-index/宽度，避免与图表重叠。"
    if ".ps1" in path or "ps1" in symbol:
        return "PowerShell 5+：`-ErrorAction Stop` 遇错即停；MySQL 用 `mysql.exe` 与 `$env:MYSQL_PWD`；脚本间用 `$LASTEXITCODE` 传递成败。"
    if "start.bat" in symbol:
        return SYMBOL_DETAIL["start.bat"]["impl"]
    return f"详见定位列 GitHub 链接首行 `【Fx-y】` 注释与随后逐行 `【行】` 注释；符号 `{symbol}` 文件 `{path or '见定位列'}`。"


def generic_qa(f_code: str, symbol: str, layer: str) -> str:
    if "Service" in layer:
        return f"问：为什么规则放 Service 不在 Controller？答：Controller 只做 HTTP 适配，业务可复用（如定时任务也调同一 Service）。符号 `{symbol}` 即业务入口。"
    if "Presentation" in layer:
        return f"问：前端为何不做密码校验/信用计算？答：安全与权威数据在后端；前端只做格式校验与展示。`{symbol}` 只负责交互与发请求。"
    if "Controller" in layer:
        return "问：Controller 有多厚？答：本项目极薄，几乎只有 @PostMapping + return service.method()，答辩可指行号证明。"
    return f"问：这一行在演示故事哪一步？答：对照本节「功能链实例」与 `{symbol}` 在表中的顺序；细节见 03-功能问答同 F 编号。"


def extract_layer_cell(layer_col: str) -> str:
    """从第一列还原所属层名称（兼容已合并相关概念的旧表）。"""
    s = re.sub(r"<br\s*/?>", "\n", layer_col, flags=re.I)
    for line in s.splitlines():
        line = line.strip()
        if line:
            return line.split("相关概念：")[0].strip() or line
    return layer_col.strip()


def build_layer_column(layer: str, concepts: str) -> str:
    base = extract_layer_cell(layer)
    c = concepts.strip()
    if not c:
        return base
    return f"{base}{INTRA_SEP}相关概念：{c}"


def split_principle_sections(text: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    for label in ("① 相关概念", "③ 底层实现", "④ 设计取舍", "⑤ 答辩要点"):
        m = re.search(rf"\*\*{re.escape(label)}\*\*：(.+?)(?=\*\*[①③④⑤]|$)", text, re.S)
        if m:
            sections[label] = m.group(1).strip()
    return sections


def _plain_label(line: str) -> str:
    return re.sub(r"\*\*([^*]+)\*\*", r"\1", line.strip())


def _is_locate_meta_line(line: str) -> bool:
    t = _plain_label(line)
    if re.match(r"^\d+\.\s", t):
        return True
    if t.startswith("   输入：") or t.startswith("   输出："):
        return True
    return t.startswith(
        ("链中位置：", "输入：", "输出：", "失败时：", "输入/输出：", "总输入：", "总输出：")
    )


def extract_code_locate(locate_col: str) -> str:
    """从第二列还原「函数·路径·行号」首段（不含链中位置正文）。"""
    raw = locate_col.strip()
    head = re.split(r"链中位置：", raw, maxsplit=1)[0].strip()
    head = re.sub(r"<br\s*/?>", " ", head, flags=re.I)
    head = re.sub(r"\s+", " ", head).strip()
    if head:
        return head
    s = re.sub(r"<br\s*/?>", "\n", locate_col, flags=re.I)
    for line in s.splitlines():
        line = line.strip()
        if not line or _is_locate_meta_line(line):
            continue
        return line
    return raw


def build_principle(
    f_code: str,
    story: str,
    layer: str,
    locate: str,
    old: str,
) -> tuple[str, str, str]:
    layer_base = extract_layer_cell(layer)
    code_locate = extract_code_locate(locate)
    symbol = extract_symbol(code_locate)
    path = extract_path(code_locate)

    detail = lookup_detail(symbol, layer_base, code_locate)

    if not detail:
        detail = infer_detail(f_code, story, layer_base, symbol, code_locate)

    detail = enrich_detail_sections(
        f_code, story, layer_base, symbol, code_locate, path, detail, line_ref, ROUTE_HINT
    )
    concepts = normalize_concepts(
        build_row_concepts(
            symbol,
            detail.get("chain", ""),
            code_locate,
            _strip_bold(detail.get("impl", "")),
            layer_base,
            f_code,
        )
    )

    layer_col = build_layer_column(layer_base, concepts)
    locate_col = build_locate_column(
        code_locate, layer_base, symbol, detail["chain"], f_code, ROUTE_HINT
    )
    principle = format_principle(
        _strip_bold(detail["impl"]),
        _strip_bold(detail["design"]),
        _strip_bold(detail["qa"]),
    )
    return layer_col, locate_col, principle


def format_principle(impl: str, design: str, qa: str) -> str:
    """实现讲解三列：无 ** 加粗，概念已并入所属层。"""
    s = PRINCIPLE_SEP
    return clean_principle_text(
        f"③ 底层实现：{impl}{s}"
        f"④ 设计取舍：{design}{s}"
        f"⑤ 答辩要点：{qa}"
    )


GH = "https://github.com/CZF312/CampusStudyRoomReservationManagementSystem/blob/master"

# F1.2 八卡「链路中位置与代码地址」列固定路径（不依赖历史损坏的 path 列）
CONCEPT_LOCATE: dict[str, str] = {
    "Browser 浏览器": f"`static/index.html` · 浏览器入口 · [L1-L8]({GH}/src/main/resources/static/index.html#L1-L8)",
    "Vue 单页框架": f"`App.vue` · 单页根组件 · [L1-L120]({GH}/frontend/src/App.vue#L1-L120)",
    "HTTP 请求": f"`App.vue` · call() 封装 · [L2380-L2420]({GH}/frontend/src/App.vue#L2380-L2420)",
    "JSON 数据格式": f"`ApiResponse.java` · 统一响应 · [L1-L40]({GH}/src/main/java/com/scau/campusstudyroomreservationmanagementsystem/dto/ApiResponse.java#L1-L40)",
    "REST API": f"`AppController.java` · REST 映射 · [L1-L80]({GH}/src/main/java/com/scau/campusstudyroomreservationmanagementsystem/controller/AppController.java#L1-L80)",
    "Service 业务层": f"`AppService.java` · 业务规则 · [L1-L120]({GH}/src/main/java/com/scau/campusstudyroomreservationmanagementsystem/service/AppService.java#L1-L120)",
    "MySQL 数据库": f"`schema.sql` · 表结构 · [L1-L80]({GH}/src/main/resources/schema.sql#L1-L80)",
    "JWT 令牌": f"`JwtService.java` · 签发解析 · [L1-L60]({GH}/src/main/java/com/scau/campusstudyroomreservationmanagementsystem/service/JwtService.java#L1-L60)",
}


def parse_concept_card_sections(name: str) -> dict[str, str]:
    card = CONCEPT_CARDS.get(name, "")
    out: dict[str, str] = {}
    for label in ("③ 底层实现", "④ 设计取舍", "⑤ 答辩要点"):
        m = re.search(rf"\*\*{re.escape(label)}\*\*：(.+?)(?=\*\*[③④⑤]|$)", card, re.S)
        if not m:
            continue
        body = m.group(1).strip()
        body = re.sub(r"\*\*怎么读代码[^*]*\*\*：", "", body)
        body = re.sub(r"\*\*技术细节\*\*：", "", body)
        body = re.sub(r"\*\*为何不这样做\*\*：", "**若不这样做**：", body)
        body = re.sub(r"(?<!\*\*)为何不这样做：", "**若不这样做**：", body)
        body = re.sub(r"(<br>){3,}", "<br><br>", body)
        out[label] = body.strip()
    return out


def extract_concept_card_concepts(name: str) -> str:
    card = CONCEPT_CARDS.get(name, "")
    m = re.search(r"\*\*① 相关概念\*\*：(.+?)(?=\*\*本行|\*\*②|\*\*③|$)", card, re.S)
    if m:
        return normalize_concepts(m.group(1).strip())
    return normalize_concepts(name)


def clean_principle_text(text: str) -> str:
    text = _strip_bold(text)
    text = re.sub(rf"({re.escape(PRINCIPLE_SEP)})+", PRINCIPLE_SEP, text)
    text = re.sub(r"(<br>){3,}", "<br><br>", text, flags=re.I)
    return text.strip()


def build_concept_locate(concept: str, instance: str, path_cell: str = "") -> str:
    name = extract_layer_cell(concept)
    code = CONCEPT_LOCATE.get(name) or extract_code_locate(path_cell) or path_cell.strip()
    return f"{code}{INTRA_SEP}链中位置：F1.2 八卡串起「小明点确认预约」全链路，本卡实例「{instance.strip()}」为其中一环。"


def build_concept_layer(concept: str, instance: str) -> str:
    name = extract_layer_cell(concept)
    if name in CONCEPT_CARDS:
        return f"{name}{INTRA_SEP}相关概念：{extract_concept_card_concepts(name)}"
    return f"{name}{INTRA_SEP}{normalize_concepts(name)}——{instance.strip()}"


def build_concept_principle(concept: str, instance: str, path_cell: str) -> str:
    name = extract_layer_cell(concept)
    if name in CONCEPT_CARDS:
        secs = parse_concept_card_sections(name)
        return format_principle(
            secs.get("③ 底层实现", ""),
            secs.get("④ 设计取舍", ""),
            secs.get("⑤ 答辩要点", ""),
        )
    return format_principle(
        strip_old_principle(path_cell) or path_cell,
        "概念与源码行号一一对应，答辩指 L 行即可。",
        "用本卡名词解释相邻下一卡如何衔接。",
    )


def parse_md_cells(line: str) -> list[str] | None:
    if not line.strip().startswith("|"):
        return None
    parts = [p.strip() for p in line.strip().strip("|").split("|")]
    if len(parts) < 3:
        return None
    if all(re.fullmatch(r"[-:\s]+", p or "-") for p in parts):
        return None
    if not any(parts):
        return None
    return parts


def is_impl_data_row(cells: list[str]) -> bool:
    if len(cells) < 3:
        return False
    c0 = cells[0]
    if not c0 or c0.startswith("-"):
        return False
    if "所属层" in c0 and "Layer" in c0:
        return False
    if "概念 Concept" in c0:
        return False
    if len(c0) < 2 and len(cells[1]) < 2:
        return False
    return True


def is_concept_table(f_code: str, first_row: list[str]) -> bool:
    if f_code == "f1-2":
        return True
    c0 = first_row[0] if first_row else ""
    return "Concept" in c0 or ("浏览器" in c0 or "Vue" in c0 or "HTTP" in c0) and "·" not in c0[:20]


def strip_html_cell(text: str) -> str:
    """HTML 表单元格还原为 rebuild 可处理的纯文本（保留 <br>）。"""
    import html as html_mod

    t = text.strip()
    t = re.sub(r"<br\s*/?>", "<br>", t, flags=re.I)
    t = re.sub(
        r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        r"[\2](\1)",
        t,
        flags=re.S | re.I,
    )
    t = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", t, flags=re.S | re.I)
    t = re.sub(r"<span[^>]*>(.*?)</span>", r"\1", t, flags=re.S | re.I)
    return html_mod.unescape(t).strip()


def rebuild_html_table(html: str, f_code: str, story: str) -> tuple[str, int]:
    changed = 0

    def repl_tr(m: re.Match[str]) -> str:
        nonlocal changed
        tr = m.group(0)
        if re.search(r"<th[\s>]", tr, flags=re.I):
            return tr
        tds = [strip_html_cell(x) for x in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.DOTALL)]
        if len(tds) < 3:
            return tr
        if len(tds) >= 4 and f_code == "f1-2":
            concept_col = build_concept_layer(tds[0], tds[1])
            locate_col = build_concept_locate(tds[0], tds[1], tds[2])
            new_p = build_concept_principle(tds[0], tds[1], tds[3] if len(tds) > 3 else tds[2])
            changed += 1
            return (
                "    <tr>\n"
                f"      <td>{concept_col}</td>\n"
                f"      <td>{tds[1]}</td>\n"
                f"      <td>{locate_col}</td>\n"
                f"      <td>{new_p}</td>\n"
                "    </tr>"
            )
        layer_col, locate_col, new_p = build_principle(
            f_code, story, tds[0], tds[1], tds[2] if len(tds) > 2 else ""
        )
        changed += 1
        return (
            "    <tr>\n"
            f"      <td>{layer_col}</td>\n"
            f"      <td>{locate_col}</td>\n"
            f"      <td>{new_p}</td>\n"
            "    </tr>"
        )

    new_html = re.sub(
        r"<tr[^>]*>\s*(?:<td[^>]*>.*?</td>\s*){3,4}\s*</tr>",
        repl_tr,
        html,
        flags=re.DOTALL,
    )
    return new_html, changed


def emit_md_table(rows: list[list[str]], four_col: bool) -> list[str]:
    if four_col:
        header = "| 概念 Concept | 实例 | 路径 Path（英 · 中）· 行号 | 原理 Principle |"
        sep = "|---|---|---|---|"
        width = 4
    else:
        header = "| 所属层 Layer | 链路中位置与代码地址 | 原理 Principle |"
        sep = "|---|---|---|"
        width = 3
    out = [header, sep]
    for row in rows:
        cells = row[:width]
        while len(cells) < width:
            cells.append("")
        out.append("| " + " | ".join(cells) + " |")
    return out


def process_doc(text: str) -> tuple[str, int]:
    lines = text.splitlines()
    out: list[str] = []
    f_code = ""
    story = ""
    changed = 0
    expect_table = False
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.search(r'<a id="(f\d+-\d+)"></a>', line)
        if m:
            f_code = m.group(1)
        if "**功能链实例" in line and i + 1 < len(lines):
            story = lines[i + 1].strip()
        if "#### 实现定位表" in line:
            expect_table = True
            out.append(line)
            i += 1
            continue

        # HTML 定位表
        if "impl-loc-table" in line and line.strip().startswith("<table"):
            block = [line]
            i += 1
            while i < len(lines) and "</table>" not in lines[i]:
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append(lines[i])
            html = "\n".join(block)
            html, n = rebuild_html_table(html, f_code, story)
            changed += n
            out.append(html)
            i += 1
            expect_table = False
            continue

        # Markdown 定位表（含损坏的无表头表）
        if line.strip().startswith("|") and (
            "所属层 Layer" in line
            or "概念 Concept" in line
            or expect_table
        ):
            # 若仅为空表头行则跳过收集时处理
            table_lines: list[str] = []
            if "所属层" in line or "概念 Concept" in line:
                table_lines.append(line)
                i += 1
                if i < len(lines) and "---" in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i])
                i += 1
            data_rows: list[list[str]] = []
            for tl in table_lines:
                cells = parse_md_cells(tl)
                if cells and is_impl_data_row(cells):
                    data_rows.append(cells)
            if data_rows:
                four = is_concept_table(f_code, data_rows[0])
                new_rows: list[list[str]] = []
                for cells in data_rows:
                    if four and len(cells) >= 4:
                        c, inst, path_c = cells[0], cells[1], cells[2]
                        concept_col = build_concept_layer(c, inst)
                        locate_col = build_concept_locate(c, inst, path_c)
                        new_p = build_concept_principle(c, inst, path_c)
                        changed += 1
                        new_rows.append([concept_col, inst, locate_col, new_p])
                    elif len(cells) >= 3:
                        layer_col, locate_col, new_p = build_principle(
                            f_code,
                            story,
                            cells[0],
                            cells[1],
                            cells[2] if len(cells) > 2 else "",
                        )
                        changed += 1
                        new_rows.append([layer_col, locate_col, new_p])
                out.extend(emit_md_table(new_rows, four))
                out.append("")
            expect_table = False
            continue

        if expect_table and line.strip() == "":
            out.append(line)
            i += 1
            continue
        if expect_table and not line.strip().startswith("|"):
            expect_table = False
        out.append(line)
        i += 1
    return "\n".join(out) + "\n", changed


def update_reading_convention(text: str) -> str:
    old = """2. **实现定位表三列** — 除 F1.2 概念卡（四列，多「原理」）外，各子项表统一为：
   - **所属层 Layer**：表现 / 接口 / 业务 / 配置 / 数据 / 运维等架构层；
   - **定位**：函数（英·中）+ 路径 + **Lx–Ly** GitHub 链接（首行含 `【Fx-y】` 总体讲解）；
   - **原理 Principle**（五段，**不重复**拆「链中位置/输入/输出/上下游」）：
     - **① 相关概念**：本节涉及的名词与术语释义；
     - **② 链路与职责**：在功能链实例中的步骤、谁调用谁、读入什么/产出什么（合并为一段）；
     - **③ 底层实现**：API 路径、HTTP 方法、表名字段、SQL 条件、状态枚举、关键 ref/函数（尽量到底层）；
     - **④ 设计取舍**：为何放该层、为何这样实现；
     - **⑤ 答辩要点**：老师常问一句 + 推荐答法。"""
    return text  # 已在 md 中更新，无需重复替换


def main() -> None:
    text = DOC.read_text(encoding="utf-8")
    text, n = process_doc(text)
    DOC.write_text(text, encoding="utf-8")
    print(f"rebuilt {n} principle cells in {DOC.name}")


if __name__ == "__main__":
    main()
