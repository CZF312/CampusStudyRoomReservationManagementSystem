# CSRRMS 最终交付矩阵（65 HTTP 端点）

> 与 `AppController`（63）+ `UploadController`（2）一致。  
> 自检：`python scripts/verify_f_doc_delivery.py`

## 图例

| 状态 | 含义 |
|------|------|
| **主链** | 01 实现定位表有 UI + Controller/Service 行号链接 |
| **F8** | 仅附录说明或纯 API、无独立 UI |
| **注释** | 源码含 `【Fx-y·步骤N】` 实例注释 |

## F2 认证与账号（9）

| 方法 | 路径 | F 节 | 状态 | 01 节 / 说明 |
|------|------|------|------|----------------|
| POST | `/auth/register` | F2.3 | 主链 | 注册 + 待审核 |
| POST | `/auth/login` | F2.1 | 主链 | 学生登录 JWT |
| POST | `/admin/auth/login` | F2.2 | 主链 | 管理员登录 |
| GET | `/auth/me` | F2.1 | 主链 | bootstrap 会话恢复 |
| POST | `/auth/change-password` | F2.4 | 主链 | 改密强制重登 |
| GET | `/student/profile` | F2.4 | 主链 | 读资料（me 含） |
| PUT | `/student/profile` | F2.4 | 主链 | 更新学院/专业 |
| POST | `/auth/register/upload` | F2.3 | 主链 | UploadController |

## F3 自习室与预约（6）

| 方法 | 路径 | F 节 | 状态 | 说明 |
|------|------|------|------|------|
| GET | `/rooms` | F3.1 | 主链 | 学生自习室列表 |
| GET | `/rooms/{id}` | F8 | F8 | 单室详情，前端少用 |
| GET | `/rooms/{id}/seats` | F8 | F8 | 多用 `/seats/available` |
| GET | `/seats/available` | F3.1 | 主链 | 绿色可选座 |
| POST | `/reservations` | F3.1 | 主链 | 创建预约 + slot |
| GET | `/reservations/my` | F3.3 | 主链 | 我的预约列表 |
| GET | `/reservations/{id}` | F8 | F8 | 单条详情 API |
| POST | `/reservations/{id}/cancel` | F3.2 | 主链 | 取消扣信用分 |

## F4 签到签退与信用（5）

| 方法 | 路径 | F 节 | 状态 | 说明 |
|------|------|------|------|------|
| GET | `/checkin/qrcode` | F8 | F8 | 后端 QR；前端本地 SVG |
| POST | `/reservations/{id}/checkout` | F4.2 | 主链 | 签退计时长 |
| GET | `/credits/my` | F4.2 | 主链 | 信用流水 |
| POST | `/admin/checkin/scan` | F4.1 | 主链 | 学号/拍照扫码 |
| GET | `/admin/checkins` | F4.1 | 主链 | 签到记录 |

## F5 学生端辅助（10）

| 方法 | 路径 | F 节 | 状态 | 说明 |
|------|------|------|------|------|
| GET | `/statistics/my-study-duration` | F5.1 | 主链 | ECharts 学习统计 |
| GET | `/announcements` | F5.2 | 主链 | 首页公告卡片 |
| POST | `/announcements/{id}/read` | F5.2 | 主链 | 公告已读 |
| GET | `/notifications` | F5.2 | 主链 | 铃铛未读 |
| POST | `/notifications/{id}/read` | F5.2 | 主链 | 单条已读 |
| POST | `/notifications/read-all` | F5.2 | 主链 | 全部已读 |
| POST | `/feedback` | F5.3 | 主链 | 学生提交 |
| GET | `/feedback/my` | F8 | F8 | 无「我的反馈」页 |
| GET | `/admin/announcements` | F5.2 | 主链 | 管理端公告 |
| POST | `/admin/announcements` | F5.2 | 主链 | 发布 |
| PUT | `/admin/announcements/{id}` | F5.2 | 主链 | 编辑 |
| DELETE | `/admin/announcements/{id}` | F8 | F8 | 无删按钮 |
| GET | `/admin/feedback` | F5.3 | 主链 | 反馈列表 |
| PUT | `/admin/feedback/{id}` | F5.3 | 主链 | 处理反馈 |

## F6 管理端（32）

| 方法 | 路径 | F 节 | 状态 | 说明 |
|------|------|------|------|------|
| GET | `/admin/dashboard` | F8 | F8 | `{ok:true}` 桩 |
| GET | `/admin/live-reservations` | F6.6 | 主链 | 实时预约看板 |
| GET | `/admin/users` | F6.3 | 主链 | 用户列表 |
| GET | `/admin/users/export` | F6.3 | 主链 | CSV 导出 |
| POST | `/admin/users/{id}/approve` | F2.3 | 主链 | 审核通过 |
| POST | `/admin/users/{id}/reject` | F6.3 | 主链 | 拒绝 |
| POST | `/admin/users/{id}/disable` | F6.3 | 主链 | 禁用 |
| POST | `/admin/users/{id}/enable` | F6.3 | 主链 | 启用 |
| GET/POST/PUT/DELETE | `/admin/rooms` 等 | F6.4 | 主链 | 自习室与座位 CRUD |
| GET | `/admin/reservations` | F6.5 | 主链 | 预约监管 |
| POST | `/admin/reservations/{id}/revoke-violation` | F6.5 | 主链 | 撤销违约 |
| GET | `/admin/statistics/*` | F6.1 | 主链 | 统计与 CSV |
| GET/POST | `/admin/settings/config` | F6.2 | 主链 | 系统配置 JSON |
| GET | `/admin/operation-logs` | F6.7 | 主链 | 操作日志 |
| GET/POST/PUT | `/admin/admins` | F6.7 | 主链 | 管理员账号 |
| POST | `/upload` | F6.4 | 主链 | 布局图 |

## 答辩勿写错

- 取消扣分默认 **−50** · 单次最长 **4 小时** · V3 **无 temp_leave**
- 扫码：**拍照/选图 + jsQR** · `GET /admin/dashboard` 仅为桩
