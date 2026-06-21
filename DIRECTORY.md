# 目录说明

> 项目根目录 = 含 `pom.xml` 与 `start.bat` 的文件夹

---

## 根目录（运行入口）

| 文件 | 说明 |
|------|------|
| `QUICKSTART.txt` | 快速开始（三步上手） |
| `start.bat` | **主启动入口**（推荐双击） |
| `start.cmd` / `start.vbs` | 备用启动方式 |
| `组长一键启动.bat` / `.vbs` | 旧版入口（已跳转到与 start.bat 相同脚本） |
| `00-组长请看这里.txt` | 验收快速指引（内容与 QUICKSTART 一致） |
| `INSTALL.md` | 安装部署与排错 |
| `README.md` | 项目简介与快速启动 |
| `PROJECT_STRUCTURE.md` | 完整目录索引 |
| `DIRECTORY.md` | 本文件：目录说明 |

---

## 数据与资源

| 路径 | 说明 |
|------|------|
| `docs/06-部署配置/database-full.sql` | 完整数据库（启动时自动导入） |
| `docs/06-部署配置/schema.sql` | 仅表结构 |
| `docs/06-部署配置/data.sql` | 仅演示数据 |
| `uploads/material/` | 学生注册材料 PDF（运行时生成） |
| `uploads/layout/` | 自习室平面图（运行时生成） |
| `src/main/resources/static/` | 已构建前端（无需 npm 即可访问 8080） |

---

## 脚本（`scripts/`）

| 路径 | 说明 |
|------|------|
| `scripts/start-system.ps1` | 一键启动核心逻辑 |
| `scripts/setup-after-clone.ps1` | clone 后配置 + 导入 + 校验 |
| `scripts/import-database-local.ps1` | 导入数据库到本机 MySQL |
| `scripts/export-database-for-git.ps1` | 从本机 MySQL 导出三份 SQL 文件 |
| `scripts/verify-v3-dictionary.ps1` | 数据库 17 项验收 |
| `scripts/build-frontend.ps1` | 前端构建并输出到 static |
| `scripts/check-env.ps1` | 检查 JDK/MySQL/Node 环境 |
| `scripts/test-db-connection.ps1` | 验证数据库连接 |
| `scripts/verify-startup.ps1` | 验证系统启动完整性 |
| `scripts/setup-shared-mysql-docker.ps1` | 组内共用 MySQL Docker 容器 |
| `scripts/open-firewall-shared.ps1` | 开放防火墙端口（共用模式） |
| `scripts/start-shared-server.ps1` | 启动共用服务器模式 |
| `scripts/prepare-full-delivery.ps1` | 准备完整交付包 |

---

## 文档（`docs/`）

| 路径 | 说明 |
|------|------|
| `docs/00-部署与验收/` | 部署与验收索引 |
| `docs/01-使用指南/` | 启动流程、答辩清单、GitHub 提交说明 |
| `docs/02-架构说明/` | 技术架构、目录规范 |
| `docs/03-开发维护/` | 开发原则、UI 对齐、问题记录 |
| `docs/04-版本记录/` | changelog、更新日志 |
| `docs/05-需求与设计/` | 需求分析、概要设计、数据字典规范 |
| `docs/06-部署配置/` | 数据库 SQL 与部署说明 |
| `docs/07-原型资源/` | HTML 原型（参考 UI，非正式运行代码） |
| `docs/08-课设交付/` | 课程设计报告 Word、全量验收清单 |

---

## 本机生成（不在发布包内）

| 路径 | 说明 |
|------|------|
| `src/main/resources/application-local.properties` | 本机 MySQL 密码（从 .example 复制后填写） |
| `src/main/resources/application-shared.properties` | 共用库配置（可选） |
| `target/` | Maven 编译输出 |
| `uploads/` | 本地上传文件 |
