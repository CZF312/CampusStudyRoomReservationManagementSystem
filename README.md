# 校园自习室预约管理系统

> **版本**：V3.1 · Spring Boot 3.5 + Vue 3 + MySQL 8

---

## 快速开始

```
项目根目录/
├── QUICKSTART.txt     ← 三步上手
├── start.bat          ← 双击启动（推荐）
├── INSTALL.md         ← 安装部署指南
├── DIRECTORY.md       ← 目录说明
└── pom.xml
```

**启动步骤**：解压 → 双击 `start.bat` → 输入 MySQL root 密码 → 浏览器打开 http://localhost:8080

启动器将自动：清空旧库 → 导入 `database-full.sql` → 校验数据 → 启动服务。

**演示账号**：
* 学生：`202225220101` / `123456`
* 普通管理员：`admin` / `admin123`
* 超级管理员：`superadmin` / `super123`（包含专属系统设置页面权限）

---

## 文档

| 文档 | 路径 |
|------|------|
| 项目结构 | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |
| 安装部署 | [INSTALL.md](INSTALL.md) |
| 数据库说明 | [docs/06-部署配置/数据库完整说明.md](docs/06-部署配置/数据库完整说明.md) |
| 课设报告 Word | [docs/08-课设交付/数据库课程设计报告.docx](docs/08-课设交付/数据库课程设计报告.docx) |
| **理解与讲解（Markdown，可页内跳转）** | [docs/09-理解与讲解/00-文档导航.md](docs/09-理解与讲解/00-文档导航.md) |
| **项目理解指南（F 编号 + 代码行链接）** | [docs/09-理解与讲解/01-项目理解指南.md](docs/09-理解与讲解/01-项目理解指南.md) |
| **答辩讲解手册** | [docs/09-理解与讲解/02-答辩讲解手册.md](docs/09-理解与讲解/02-答辩讲解手册.md) |
| 功能问答 | [docs/09-理解与讲解/03-功能问答-定位环境.md](docs/09-理解与讲解/03-功能问答-定位环境.md) |
| API 交付矩阵 | [docs/09-理解与讲解/DELIVERY_MATRIX.md](docs/09-理解与讲解/DELIVERY_MATRIX.md) |
| **新人理解指南 Word** | [docs/09-理解与讲解/01-项目理解指南.docx](docs/09-理解与讲解/01-项目理解指南.docx) |
| **答辩讲解手册 Word** | [docs/09-理解与讲解/02-答辩讲解手册.docx](docs/09-理解与讲解/02-答辩讲解手册.docx) |
| 架构与导航 | [架构与文档导航.md](架构与文档导航.md) |
| 需求与设计 | [docs/05-需求与设计/](docs/05-需求与设计/) |

---

## 环境要求

| 组件 | 版本 |
|------|------|
| JDK | 20+ |
| MySQL | 8.x |
| Node.js | 仅修改前端时需要 |

---

## 交付物

| 路径 | 说明 |
|------|------|
| `docs/06-部署配置/database-full.sql` | 完整数据库 |
| `uploads/` | 材料与布局图 |
| `src/main/resources/static/` | 已构建前端 |
| `start.bat` | 一键启动 |

完整文档索引：[docs/README.md](docs/README.md)
