# 校园自习室预约管理系统 — 项目结构说明

> **产品名称**：校园自习室预约管理系统（CSRRMS）  
> **版本**：V3.0 · Spring Boot 3.5 + Vue 3 + MySQL 8

---

## 一级目录职责

```
CampusStudyRoomReservationManagementSystem/
├── QUICKSTART.txt              # 快速开始（三步上手）
├── start.bat / start.cmd / start.vbs   # 一键启动入口
├── INSTALL.md                  # 安装部署指南
├── DIRECTORY.md                # 目录说明
├── README.md                   # 项目入口
├── PROJECT_STRUCTURE.md        # 本文件：完整目录索引
├── pom.xml / mvnw*             # Maven 后端构建
├── docs/                       # 全部文档（按序号分子目录）
├── frontend/                   # Vue 3 前端源码
├── scripts/                    # 自动化脚本（导入/验收/构建/共用库）
├── src/                        # Spring Boot 源码 + static 构建产物
├── uploads/                    # 注册材料 PDF、房间布局图（运行时生成）
└── target/                     # 编译输出（可删，不提交 Git）
```

---

## docs 子目录

| 目录 | 内容 |
|------|------|
| `00-部署与验收/` | 部署与验收索引 |
| `01-使用指南/` | 启动、提交、答辩、Git、傻瓜式讲解 |
| `02-架构说明/` | 技术架构、目录说明 |
| `03-开发维护/` | UI 对齐、问题记录、验收对照、开发原则 |
| `04-版本记录/` | changelog、第三版实施总结 |
| `05-需求与设计/` | 需求文档、概要设计、数据字典规范 |
| `06-部署配置/` | SQL（schema/data/full）、Docker、数据库范式说明 |
| `07-原型资源/` | HTML 原型（参考 UI，非正式运行代码） |
| `08-课设交付/` | 课设报告 Word、全量验收清单 |
| `09-理解与讲解/` | 零基础理解指南、答辩讲解手册（md 真源） |

---

## 路径敏感配置

| 配置 | 默认值 |
|------|--------|
| `application.properties` → `app.upload.dir` | `${user.dir}/uploads`（项目启动目录下） |
| SQL 导入路径 | `docs/06-部署配置/database-full.sql` |
| 静态资源 | `src/main/resources/static/` |
| 本机密码配置 | `src/main/resources/application-local.properties`（不提交 Git） |

---

## 常用命令

```powershell
# 进入项目根目录（与 pom.xml 同级）
cd <项目根目录>

# 一键清空导入 + 验收 + 启动
.\start.bat

# 仅验收数据库
.\scripts\verify-v3-dictionary.ps1 -Password 123456

# 后端启动
.\mvnw.cmd spring-boot:run

# 单元测试
.\mvnw.cmd test

# 前端构建（输出到 src/main/resources/static）
cd frontend
npm run build
```

---

## 演示账号

| 角色 | 账号 | 密码 |
|------|------|------|
| 学生 | `202225220101` | `123456` |
| 管理员 | `admin` | `admin123` |
| 超级管理员 | `superadmin` | `super123` |

---

## 后端源码结构（`src/`）

```
src/main/java/com/scau/campusstudyroomreservationmanagementsystem/
├── CampusStudyRoomReservationManagementSystemApplication.java  # 启动类
├── controller/
│   ├── AppController.java        # 全部业务 REST API
│   └── UploadController.java     # 文件上传
├── service/
│   ├── AppService.java           # 核心业务逻辑
│   ├── DatabaseInitializer.java  # 启动时建表、种子数据
│   └── ScheduledTaskService.java # 定时任务（违约、签退、黑名单解除）
├── config/
│   ├── SecurityConfig.java       # Spring Security 配置
│   ├── JwtAuthFilter.java        # JWT 过滤器
│   ├── JwtService.java           # JWT 签发/解析
│   ├── UploadStorage.java        # 上传存储配置
│   └── WebConfig.java            # 静态资源映射
└── support/
    ├── ApiResponse.java          # 统一成功响应 { code, message, data }
    ├── BusinessException.java    # 业务异常
    ├── CurrentUser.java          # 当前用户上下文
    ├── GlobalExceptionHandler.java  # 统一错误处理
    └── SqlFragments.java         # SQL 片段工具

src/main/resources/
├── application.properties        # 端口、数据库、JWT、上传目录等配置
├── application-local.properties.example   # 本机配置示例（复制后填密码）
├── application-shared.properties.example  # 共用库配置示例
└── static/                       # 前端 build 产物（由 npm run build 生成）
```

---

## 前端源码结构（`frontend/`）

```
frontend/
├── src/
│   ├── App.vue       # 主应用（学生端 + 管理端所有页面）
│   ├── main.js       # Vue 入口
│   ├── qr.js         # 二维码 SVG 生成
│   └── styles.css    # 全局样式
├── index.html        # HTML 壳
├── vite.config.js    # 开发服务器 + /api 代理到 8080
├── package.json      # npm 依赖与脚本
└── package-lock.json
```

---

## 脚本目录（`scripts/`）

| 脚本 | 说明 |
|------|------|
| `start-system.ps1` | 一键启动核心逻辑 |
| `setup-after-clone.ps1` | clone 后配置 + 导入 + 校验 |
| `import-database-local.ps1` | 导入数据库到本机 MySQL |
| `export-database-for-git.ps1` | 从本机 MySQL 导出三份 SQL 文件 |
| `verify-v3-dictionary.ps1` | 数据库 17 项验收 |
| `build-frontend.ps1` | 前端构建并输出到 static |
| `check-env.ps1` | 检查 JDK/MySQL/Node 环境 |
| `test-db-connection.ps1` | 验证数据库连接 |
| `test-mysql-login.ps1` | 测试 MySQL 登录 |
| `verify-startup.ps1` | 验证系统启动完整性 |
| `setup-shared-mysql-docker.ps1` | 组内共用 MySQL Docker 容器 |
| `open-firewall-shared.ps1` | 开放防火墙端口（共用模式） |
| `start-shared-server.ps1` | 启动共用服务器模式 |
| `backup-shared-db.ps1` | 备份共用数据库 |
| `install-tunnel-tools.ps1` | 安装隧道工具（ngrok/Tailscale） |
| `start-public-tunnel.ps1` | 启动公网隧道 |
| `start-tailscale-team.ps1` | Tailscale 组网 |
| `prepare-full-delivery.ps1` | 准备完整交付包 |
| `generate_course_report_docx.py` | 生成课设报告 Word |
| `generate_upload_assets_from_sql.py` | 从 SQL 生成上传资产 |
| `normalize_third_dictionary_sql.py` | 规范化第三版数据字典 SQL |
