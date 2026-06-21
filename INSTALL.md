# 安装部署指南

> **校园自习室预约管理系统** · 版本 V3.0  
> 适用：Windows 10/11 · JDK 20+ · MySQL 8.x

---

## 1. 安装前准备

| 组件 | 要求 | 验证命令 |
|------|------|----------|
| JDK | 20 或更高 | `java -version` |
| MySQL | 8.x 服务运行中 | 服务管理器中 MySQL80 为 Running |
| MySQL 客户端 | bin 目录加入 PATH | `mysql --version` |

无需安装 Node.js（前端已预构建在 `src/main/resources/static/`）。

---

## 2. 一键安装与启动

1. 解压发布包至任意目录（路径建议不含特殊字符）
2. 进入项目根目录（与 `pom.xml`、`start.bat` 同级）
3. **双击 `start.bat`**
4. 首次运行输入本机 **MySQL root 密码**（仅保存在本机 `application-local.properties`）
5. 等待出现 `PASS=17 FAIL=0` 与 `CSRRMS-Backend` 窗口
6. 浏览器访问 http://localhost:8080

### 启动器自动执行流程

```
环境检测 → 保存配置 → DROP 数据库 → 导入 database-full.sql
→ 数据完整性校验 → 启动 Spring Boot → 打开浏览器
```

每次运行 `start.bat` 都会**清空并重新导入**标准演示数据，确保与发布包一致。

---

## 3. 演示账号

| 角色 | 账号 | 密码 |
|------|------|------|
| 学生 | `202225220101` | `123456` |
| 管理员 | `admin` | `admin123` |
| 超级管理员 | `superadmin` | `super123` |

---

## 4. 停止服务

关闭标题为 **CSRRMS-Backend** 的命令行窗口即可停止后端。

---

## 5. 常见问题

| 现象 | 处理 |
|------|------|
| 提示找不到 `database-full.sql` | 重新下载完整发布包，确认 `docs/06-部署配置/` 下有该文件 |
| `Access denied` | 使用本机 MySQL root 密码，非系统登录密码 |
| `Malformed \uxxxx` | 删除 `application-local.properties` 后重新运行 start.bat |
| 端口 8080 占用 | 结束占用进程或修改 `application.properties` 中 `server.port` |
| 校验 FAIL | 查看红色提示，确认 MySQL 版本为 8.x 后重试 start.bat |

---

## 6. 命令行方式（可选）

```powershell
cd <项目根目录>
.\scripts\import-database-local.ps1 -UseFullDump -Password <密码>
.\scripts\verify-v3-dictionary.ps1 -Password <密码>
.\mvnw.cmd spring-boot:run
```

---

## 7. 数据库说明

- 库名：`study_room_reservation`
- 表：16 张业务表 + 1 个统计视图 + 24 条外键
- 完整 SQL：`docs/06-部署配置/database-full.sql`

详见 `docs/06-部署配置/数据库完整说明.md`。
