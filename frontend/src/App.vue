<template>
  <div class="device" :class="{ desktop: isDesktop, mobile: !isDesktop }">
    <div class="app-container">
    <div v-if="toast" class="toast">{{ toast }}</div>

    <section v-if="!token" :class="loginRole === 'admin' ? 'admin-login-page' : 'login-page'">
      <!-- 【F2-1·学生登录】功能链实例：小明在登录页输入 `202225220101` / `123456` → 点「登录」→ 首页显示「你好，小明」→ 再进「我的预约」无需重输密码（`localStorage` 已有 token）。 本处职责：小明或 admin 在登录页填账号密码 -->
      <template v-if="loginRole === 'student'">
      <div class="login-logo-box">🎓</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
      <div class="login-title">校园自习室预约系统</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
      <div class="login-subtitle">{{ loginRole === 'student' ? 'Campus Study Room Reservation' : 'Study Room Admin Console' }}</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
      <div class="login-card"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
        <div class="field"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          <label>学号</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <input v-model="studentLogin.username" class="input" placeholder="请输入学号" autocomplete="username" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        <div class="field"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          <label>密码</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <input v-model="studentLogin.password" class="input" type="password" placeholder="请输入密码" autocomplete="current-password" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        <button type="button" class="btn btn-primary btn-block" :disabled="authLoading" @click="loginStudent">{{ authLoading ? '登录中…' : '登录' }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
        <div class="login-links"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          <button type="button" @click="forgetPassword">忘记密码？</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          <button type="button" @click="openRegister">注册账号 →</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
        </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        <button type="button" class="btn btn-outline btn-block" @click="loginRole = 'admin'">🔧 切换管理员登录</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
      </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
      </template>
      <div v-else class="admin-login-card">
        <h2 class="modal-title">管理员登录</h2>
        <div class="field">
          <label>管理员账号</label>
          <input v-model="adminLogin.account" class="input" placeholder="请输入管理员账号" autocomplete="username" />
        </div>
        <div class="field">
          <label>密码</label>
          <input v-model="adminLogin.password" class="input" type="password" placeholder="请输入密码" autocomplete="current-password" />
        </div>
        <button type="button" class="btn btn-primary btn-block" :disabled="authLoading" @click="loginAdmin">{{ authLoading ? '登录中…' : '登录' }}</button>
        <button type="button" class="btn btn-outline btn-block" @click="loginRole = 'student'">🎓 切换学生登录</button>
      </div>
    </section>

    <section v-else-if="role === 'STUDENT'" class="student-app">
      <header class="topbar" :class="{ 'home-topbar': studentPage === 'home' }">
        <button class="icon-btn" v-if="studentPage !== 'home'" @click="goBackStudent">←</button>
        <span class="topbar-spacer" v-else></span>
        <h1>{{ studentTitle }}</h1>
        <button v-if="studentPage === 'notifications'" type="button" class="header-action" @click="readAllNotifications">全部已读</button>
        <button class="icon-btn bell-btn" v-else-if="studentPage === 'home'" @click="openNotifications">🔔<span v-if="unreadCount" class="badge">{{ unreadCount }}</span></button>
        <span v-else class="topbar-spacer"></span>
      </header>

      <main class="content page-fade">
        <template v-if="studentPage === 'home'">
          <div class="hero-card">
            <strong class="hero-title">你好，{{ me.name || '同学' }}</strong>
            <span class="hero-sub">{{ homeDateText }}</span>
          </div>
          <!-- 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：管理员发布公告后，小明首页此处展示公告卡片 -->
          <h2 class="section-title">📣 公告通知</h2> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="announce-row"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <article class="announce-card" v-for="a in sortedAnnouncements.slice(0, 4)" :key="a.id" @click="readAnnouncement(a)"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="announce-tag">📌 {{ a.pinned ? '系统通知' : (a.type || '公告') }}</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <strong>{{ a.title }}</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <p>{{ formatDate(a.published_at || a.created_at) }}</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </article> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <h2 class="section-title">📅 今日预约</h2> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <article class="card" v-if="todayReservation"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="today-head"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <strong>📌 今日预约</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <span class="status" :class="todayReservation.status">{{ statusText(todayReservation.status) }}</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="today-grid"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <div class="label">自习室</div><div class="value">{{ todayReservation.roomName }}</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <div class="label">座位</div><div class="value">{{ todayReservation.seatNo }}</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <div class="label">时段</div><div class="value">{{ timeRangeText(todayReservation) }}</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </article> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div v-else class="card empty muted">今日暂无预约，可前往预约页选择座位。</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          <h2 class="section-title">🏠 推荐自习室</h2> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="recommend-list"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <article class="recommend-item" v-for="r in rooms" :key="r.id" @click="selectRoom(r.id)"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="recommend-icon">🏫</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <strong>{{ r.name }}</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <p class="muted">{{ r.location }} · 普通</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="recommend-badge">余{{ r.availableSeats }}座</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </article> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="hero-banner"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <h4>💡 学习小贴士</h4> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p>番茄工作法：每学习 25 分钟休息 5 分钟，建议预约 2-3 小时提高效率。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        </template>

        <template v-if="studentPage === 'reservation'">
          <!-- 【F3-1·查座预约】功能链实例：小明登录 → 预约 Tab → 选明天 **14:00–16:00** → 座位图点绿色 **A-12** → 确认 → 提示成功，状态「待使用」；库中 `reservation` 一行 + 多条 `reservation_slot`… 本处职责：小明选日期、14:00–16:00 快捷时段与绿色 A-12 -->
          <div v-if="creditBlocked" class="card warn-hint" style="border-color:#fecaca;background:#fff1f2;color:#b91c1c;font-weight:700"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            信用积分不足，暂不可预约。请前往「我的 → 信用积分」查看详情。
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <h2>🗓️ 选择日期</h2> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="date-rail"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <button v-for="d in dateOptions" :key="d.date" class="date-pill" :class="{ active: reservationForm.date === d.date }" @click="setReservationDate(d.date)"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <span>{{ d.label }}</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <strong>{{ d.day }}</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <small>{{ d.month }}月</small> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

          <h2 class="section-title">⏱️ 选择时段</h2> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <p v-if="currentRoom" class="scanner-hint">当前自习室开放时间：{{ currentRoomOpenTime }} — {{ currentRoomCloseTime }}（以下选项随所选自习室自动变化）</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="time-slots"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <button v-for="slot in availableQuickTimeSlots" :key="slot.label" type="button" class="time-chip" :class="{ active: isQuickSlotActive(slot), disabled: slot.expired }" :disabled="slot.expired" @click="applyQuickSlot(slot)">{{ slot.label }}{{ slot.expired ? '（已过期）' : '' }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="card reserve-config"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="time-select-row"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <label>开始</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-select v-model="reservationForm.startTime" placeholder="请选择开始时间" :teleported="false" @change="handleStartTimeChange"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <el-option v-for="t in startTimeOptions" :key="`s-${t}`" :label="t" :value="t" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </el-select> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <span>→</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <label>结束</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-select v-model="reservationForm.endTime" placeholder="请选择结束时间" :teleported="false" @change="handleEndTimeChange"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <el-option v-for="t in endTimeOptions" :key="`e-${t}`" :label="t" :value="t" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </el-select> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

          <h2 class="section-title">🧮 预约配置</h2> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="card reserve-config"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <label>自习室</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-select v-model="reservationForm.roomId" @change="handleRoomChange"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-option v-for="r in rooms" :key="r.id" :label="`${r.name}（余${r.availableSeats}）`" :value="r.id" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </el-select> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="seat-filters"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <button v-for="f in seatFilterOptions" :key="f.key" type="button" class="filter-chip" :class="{ active: seatFilter === f.key }" @click="seatFilter = f.key">{{ f.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="legend legend-row"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <span><i class="legend-dot free"></i>可选</span><span><i class="legend-dot busy"></i>不可用</span><span><i class="legend-dot sel"></i>已选</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

          <div class="seat-overview"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="seat-overview-head"><strong>🗺️ 座位分布图</strong><span class="muted">{{ currentRoom?.name || '自习室' }}</span></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <img v-if="roomLayoutImage" class="seat-layout-image" :src="roomLayoutImage" :alt="`${currentRoom?.name || '自习室'}座位分布图`" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div v-else class="seat-layout-empty">管理员尚未上传该自习室的座位分布图</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

          <div class="seat-sections"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <section v-for="sec in groupedSeats" :key="sec.name" class="seat-section"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="seat-section-title">{{ sec.name }}（可预约 {{ sec.availableCount }}）</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <div class="seat-section-grid"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <button v-for="s in sec.seats" :key="s.id" type="button" class="seat" :class="seatVisualClass(s)" :disabled="!canSelectSeat(s)" @click="openSeatDetail(s)">{{ s.seat_no }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </section> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <button class="primary-action reserve-submit" :disabled="!selectedSeat || creditBlocked" @click="openConfirmReservation">确认预约 {{ selectedSeat ? selectedSeat.seat_no : '' }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
        </template>

        <template v-if="studentPage === 'checkin'">
          <!-- 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：小明签到页展示学号 QR，等 admin 扫码 -->
          <div class="card check-card check-hero"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <span class="status" :class="reservationStatusClass(activeReservation?.status) || 'PENDING'">{{ activeReservation ? statusText(activeReservation.status) : '暂无预约' }}</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="timer">{{ timerText }}</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="card reservation-detail-card checkin-info-card" v-if="activeReservation"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="checkin-row"><div class="k">自习室</div><div class="v">{{ activeReservation.roomName }}</div></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="checkin-row"><div class="k">座位号</div><div class="v">{{ activeReservation.seatNo }}</div></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="checkin-row"><div class="k">预约时段</div><div class="v">{{ timeRangeText(activeReservation) }}</div></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="checkin-row"><div class="k">预约日期</div><div class="v">{{ formatDate(activeReservation.reserve_date) }}</div></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="card check-actions" v-if="activeReservation"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <template v-if="isPendingReservation(activeReservation.status)">
              <div class="check-wait-card card"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <strong>等待管理员签到</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <p class="check-student-no">学号：<span>{{ studentNoDisplay }}</span></p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <div v-if="checkinQrSvg" class="qr-image checkin-qr" v-html="checkinQrSvg"></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <p class="muted check-wait-tip">可向管理员<strong>报学号</strong>，或出示上方二维码供管理员<strong>拍照扫码</strong>（无需 token）</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="check-actions-state"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <button type="button" class="round-action warning-round" @click="openFeedbackModal"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                  <span>💬</span><strong>问题反馈</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                </button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="check-hint">{{ checkinWindowHint }}</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </template>
            <template v-else-if="isUsingReservation(activeReservation.status)">
              <div class="check-actions-state">
                <button type="button" class="round-action danger-round" @click="confirmCheckout">
                  <span>🚪</span><strong>签退</strong>
                </button>
                <button type="button" class="round-action warning-round" @click="openFeedbackModal">
                  <span>💬</span><strong>问题反馈</strong>
                </button>
              </div>
              <div class="check-hint">请在预约结束前完成签退。</div>
            </template>
          </div>
          <div v-else class="card empty muted">当前没有进行中的预约，可前往预约页选座。</div>
        </template>

        <template v-if="studentPage === 'profile'">
          <div class="profile-head">
            <div class="avatar">{{ (me.name || '同').slice(0, 1) }}</div>
            <div>
              <strong>{{ me.name || '同学' }}</strong>
              <p class="muted">学号：{{ me.student_no || me.username }}</p>
              <p class="muted">{{ me.college || '计算机学院' }}</p>
            </div>
          </div>
          <div class="profile-group-title">功能服务</div>
          <div class="profile-menu">
            <button type="button" class="profile-item" @click="studentPage = 'myres'"><span>📋</span><span>我的预约</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item" @click="studentPage = 'credit'"><span>⭐</span><span>信用积分</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item" @click="openStudyStats()"><span>📊</span><span>学习统计</span><span class="arrow">›</span></button>
          </div>
          <div class="profile-group-title">账号与安全</div>
          <div class="profile-menu">
            <button type="button" class="profile-item" @click="openProfileInfo"><span>📝</span><span>个人信息</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item" @click="openChangePassword"><span>🔐</span><span>修改密码</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item" @click="studentPage = 'settings'"><span>⚙️</span><span>设置</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item" @click="aboutOpen = true"><span>ℹ️</span><span>关于系统</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item" @click="openFeedbackModal"><span>💬</span><span>问题反馈</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item danger" @click="logout"><span>🚪</span><span>退出登录</span><span class="arrow">›</span></button>
          </div>
        </template>

        <template v-if="studentPage === 'myres'">
          <!-- 【F3-3·我的预约】功能链实例：小明在「我的 → 我的预约」按 Tab 筛「待使用」→ 看到刚约的 A-12；管理员签到后，签到页每 2 秒轮询同一接口，状态自动变「使用中」。 本处职责：小明在「我的预约」按 Tab 筛选，卡片上可取消待使用单 -->
          <div class="filter-row"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <button v-for="s in reservationTabs" :key="s.key" :class="{ active: reservationStatus === s.key }" @click="reservationStatus = s.key">{{ s.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <ReservationCard v-for="r in shownReservations" :key="r.id" :item="r" :status-text="statusText" @cancel="cancelReservation(r)" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        </template>

        <template v-if="studentPage === 'credit'">
          <div class="card credit-ring-card">
            <div class="credit-ring" :style="{ '--score': creditPercent + '%' }">
              <strong>{{ credit.score }}</strong>
              <span>/ {{ CREDIT_SCORE_MAX }}</span>
            </div>
            <b>{{ creditLevel }}</b>
          </div>
          <div class="credit-metrics">
            <div class="card"><strong>{{ reservations.length }}</strong><span>总预约次数</span></div>
            <div class="card"><strong>{{ checkinCount }}</strong><span>准时签到</span></div>
            <div class="card"><strong>{{ violationCount }}</strong><span>违约次数</span></div>
          </div>
          <h2 class="section-title">📜 积分变动记录</h2>
          <div class="credit-rules card">
            <div class="credit-rule"><strong>按时签到</strong> +5 分；主动取消预约 -50 分；超时未签到 -50 分。</div>
            <div class="credit-rule"><strong>积分上限</strong> {{ CREDIT_SCORE_MAX }} 分；280 分以上优秀，200 分以上良好。</div>
          </div>
          <div class="timeline">
            <div v-for="l in credit.logs" :key="l.id" class="timeline-item">
              <strong :class="Number(l.change_value) >= 0 ? 'credit-gain' : 'credit-deduct'">{{ Number(l.change_value) > 0 ? '+' : '' }}{{ l.change_value }}</strong>
              <span>{{ l.reason }}</span>
              <small>{{ l.created_at }}</small>
            </div>
          </div>
        </template>

        <template v-if="studentPage === 'stats'">
          <!-- 【F5-1·学习统计】功能链实例：小明打开学习统计切换当期/往期查看柱图 本处职责：学习统计页模板，含独立起止日期选择与快捷区间按钮 -->
          <div class="period-tabs stats-range-tabs"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <button type="button" :class="{ active: studyStatsRangeMode === 'current' }" @click="changeStudyStatsRangeMode('current')">当期</button> <!-- 【行】绑定当期/往期 Tab 高亮与点击切换 -->
            <button type="button" :class="{ active: studyStatsRangeMode === 'past' }" @click="changeStudyStatsRangeMode('past')">往期</button> <!-- 【行】绑定当期/往期 Tab 高亮与点击切换 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div v-if="studyStatsRangeMode === 'past'" class="student-stats-range-row"> <!-- 【行】绑定当期/往期 Tab 高亮与点击切换 -->
            <div class="student-date-range-fields"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <el-date-picker
                v-model="studyStatsStartDate"
                type="date"
                teleported
                placement="bottom-start"
                placeholder="开始日期"
                value-format="YYYY-MM-DD"
                :popper-options="statsSingleDatePopperOptions"
                :popper-style="statsSingleDatePopperStyle"
                popper-class="stats-date-popper-single"
                class="student-stats-date-picker"
                @change="onStudyStatsStartDateChange"
              /> <!-- 【行】Element Plus 开始日期：独立单月历，避免 daterange 双面板重叠 -->
              <span class="student-date-sep">至</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-date-picker
                v-model="studyStatsEndDate"
                type="date"
                teleported
                placement="bottom-end"
                placeholder="结束日期"
                value-format="YYYY-MM-DD"
                :popper-options="statsSingleDatePopperOptions"
                :popper-style="statsSingleDatePopperStyle"
                popper-class="stats-date-popper-single"
                class="student-stats-date-picker"
                @change="onStudyStatsEndDateChange"
              /> <!-- 【行】Element Plus 结束日期：独立单月历，teleported 挂 body -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="stats-date-shortcuts"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button v-for="s in statsRangeShortcuts" :key="s.text" type="button" class="btn btn-outline btn-sm" @click="applyStudyStatsShortcut(s)">{{ s.text }}</button> <!-- 【行】快捷区间按钮：一键写入起止日期并拉数 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <button type="button" class="btn btn-outline" @click="resetStudyStatsDateRange">全部历史</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <p v-if="studyStatsHint" class="scanner-hint">{{ studyStatsHint }}</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="stats-tabs"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <button v-for="p in statPeriods" :key="p.key" :class="{ active: statPeriod === p.key }" @click="changeStatPeriod(p.key)">{{ p.label }}</button> <!-- 【行】日报~年报周期 Tab 切换 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="stat-summary-grid"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="card"><strong>{{ totalStudyHours }}</strong><span>小时</span><b>总学习时长</b></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="card"><strong>{{ averageStudyHours }}</strong><span>小时</span><b>日均时长</b></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div class="card"><strong>{{ studyDays }}</strong><span>天</span><b>学习天数</b></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="card stat-card"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <h2>{{ studyChartTitle }}</h2> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="bar-chart-lite"> <!-- 【行】轻量柱图：按 studyBars 计算属性渲染每日/每月学习时长 -->
              <div v-for="b in studyBars" :key="b.label" class="bar-col"> <!-- 【行】轻量柱图：按 studyBars 计算属性渲染每日/每月学习时长 -->
                <strong>{{ b.value }}<span class="bar-unit">小时</span></strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <div class="bar-track"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                  <span :style="{ height: `${barHeight(b.value)}%` }"></span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <small>{{ b.label }}</small> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <div class="card study-advice"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <strong>📈 学习建议</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p>{{ studyAdvice }}</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        </template>

        <template v-if="studentPage === 'feedback'">
          <FeedbackBox @submit="submitFeedback" />
        </template>

        <!-- 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：小明点铃铛进入通知页，可单条/全部标已读 -->
        <template v-if="studentPage === 'notifications'">
          <el-button plain @click="readAllNotifications">全部已读</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          <article class="notif-item" :class="{ read: n.read_flag }" v-for="n in notifications" :key="n.id" @click="readNotification(n)"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="notif-icon">🔔</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            <div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <strong><span v-if="!n.read_flag" class="dot"></span>{{ n.title }}</strong> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <p class="muted">{{ n.content }}</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </article> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
        </template>

        <template v-if="studentPage === 'settings'">
          <div class="profile-group-title">账号与安全</div>
          <div class="profile-menu">
            <button type="button" class="profile-item" @click="openChangePassword"><span>🔐</span><span>修改密码</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item"><span>📱</span><span>手机绑定</span><span class="muted">{{ me.phone || '未绑定' }}</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item"><span>✉️</span><span>邮箱绑定</span><span class="muted">{{ me.email || '未绑定' }}</span><span class="arrow">›</span></button>
          </div>
          <div class="profile-group-title">通知偏好</div>
          <div class="card">
            <div class="setting-item"><span>预约提醒</span><button type="button" class="switch" :class="{ on: notifyPrefs.reservation }" @click="toggleNotifyPref('reservation')"></button></div>
            <div class="setting-item"><span>签到提醒</span><button type="button" class="switch" :class="{ on: notifyPrefs.checkin }" @click="toggleNotifyPref('checkin')"></button></div>
            <div class="setting-item"><span>公告通知</span><button type="button" class="switch" :class="{ on: notifyPrefs.announcement }" @click="toggleNotifyPref('announcement')"></button></div>
            <div class="setting-item"><span>免打扰模式</span><button type="button" class="switch" :class="{ on: notifyPrefs.dnd }" @click="toggleNotifyPref('dnd')"></button></div>
          </div>
          <div class="profile-group-title">通用</div>
          <div class="profile-menu">
            <button type="button" class="profile-item" @click="openFeedbackModal"><span>❓</span><span>帮助与反馈</span><span class="arrow">›</span></button>
            <button type="button" class="profile-item" @click="aboutOpen = true"><span>ℹ️</span><span>关于系统</span><span class="muted">v1.1</span><span class="arrow">›</span></button>
          </div>
        </template>
      </main>

      <nav class="bottom-nav">
        <button v-for="n in studentNav" :key="n.page" :class="{ active: activeStudentTab === n.page }" @click="studentPage = n.page">
          <span>{{ n.icon }}</span>
          <b>{{ n.label }}</b>
        </button>
      </nav>
    </section>

    <section v-else class="admin-app admin-shell">
      <aside class="admin-sidebar" v-if="isDesktop">
        <strong>管理后台</strong>
        <button v-for="n in adminNav" :key="n.page" type="button" class="admin-side-item" :class="{ active: adminPage === n.page }" @click="openAdmin(n.page)">{{ n.icon }} {{ n.label }}</button>
        <div class="admin-profile-chip" aria-label="当前管理员信息" @click.stop="adminProfileMenuOpen = !adminProfileMenuOpen">
          <div class="admin-profile-avatar">{{ adminProfileInitial }}</div>
          <div class="admin-profile-meta">
            <strong>{{ me.name || me.account || '管理员' }}</strong>
            <span>{{ adminRoleLabel }}</span>
          </div>
          <div v-if="adminProfileMenuOpen" class="admin-profile-popup" @click.stop>
            <button type="button" @click="switchAdminAccount">🔄 切换账号</button>
            <button type="button" class="danger" @click="logout">🚪 退出登录</button>
          </div>
        </div>
      </aside>
      <div class="admin-main">
        <header class="topbar">
          <h1>{{ adminNav.find(n => n.page === adminPage)?.label }}</h1>
        </header>
        <nav class="admin-tabs" v-if="!isDesktop">
          <button v-for="n in adminNav" :key="n.page" :class="{ active: adminPage === n.page }" @click="openAdmin(n.page)">{{ n.label }}</button>
        </nav>

        <main class="content admin-content">
          <template v-if="adminPage === 'users'">
            <!-- 【F6-3·用户管理】功能链实例：管理员在用户管理拒绝小李注册，或禁用违规学生；可导出 CSV。 本处职责：管理员审核/拒绝/禁用学生，可导出 CSV -->
            <div class="admin-head-actions"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <h3 class="section-title">学生用户管理</h3> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <button type="button" class="btn btn-primary" @click="exportUsersCsv">导出 CSV</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p class="scanner-hint">审核注册申请、禁用/启用学生账号；导出包含当前筛选条件下的全部学生。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-input v-model="userKeyword" placeholder="搜索学号或姓名" @input="loadUsers" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="filter-row user-audit-filters"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button v-for="f in userAuditFilters" :key="f.key" type="button" :class="{ active: userAuditFilter === f.key }" @click="userAuditFilter = f.key; loadUsers()">{{ f.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <DataTable :rows="pagedUsers" :columns="['student_no','name','college','credit_score','auditLabel','statusLabel']" empty-text="暂无用户数据"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <template #actions="{ row }">
                <el-button size="small" @click="openUserDetail(row)">详情</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <el-button v-if="isPendingAudit(row.audit_status)" size="small" type="success" @click="approve(row)">通过</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <el-button v-if="isPendingAudit(row.audit_status)" size="small" type="warning" @click="reject(row)">拒绝</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <el-button v-if="!isDisabledAccount(row.accountStatus) && isApprovedAudit(row.audit_status)" size="small" @click="disable(row)">禁用</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <el-button v-if="isDisabledAccount(row.accountStatus)" size="small" @click="enable(row)">启用</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </template>
            </DataTable>
            <AdminPager v-model:page="userPage" v-model:page-size="userPageSize" :total="userTotalPages" :count="users.length" />
          </template>

          <template v-if="adminPage === 'admins'">
            <!-- 【F6-7·管理员与日志】功能链实例：superadmin 在「设置 → 操作日志」查看审核/改密等记录；在「管理员管理」新增普管账号。 本处职责：superadmin 新增/编辑/禁用其他管理员账号 -->
            <div class="admin-head-actions"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <h3>管理员管理</h3> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <button v-if="isSuperAdmin" type="button" class="btn btn-primary" @click="openAdminForm()">新增管理员</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p v-if="!isSuperAdmin" class="scanner-hint">仅超级管理员可新增、编辑或禁用其他管理员；您当前只能查看自己的账号信息。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p v-else class="scanner-hint">超级管理员可分配图书馆负责人、新增/编辑/禁用普通管理员账号。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-input v-model="adminKeyword" placeholder="搜索账号或姓名" clearable /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="filter-row user-audit-filters"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button v-for="f in adminStatusFilters" :key="f.key" type="button" :class="{ active: adminStatusFilter === f.key }" @click="adminStatusFilter = f.key">{{ f.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <DataTable :rows="pagedAdminAccounts" :columns="adminAccountColumns" empty-text="暂无管理员"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <template #actions="{ row }">
                <template v-if="isSuperAdmin">
                  <el-button v-if="!isSuperAdminRole(row.role)" size="small" @click="openAdminForm(row)">编辑</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <el-button v-if="!isAdminLeft(row.status) && row.id !== me.id && !isSuperAdminRole(row.role)" size="small" type="warning" @click="disableAdminAccount(row)">禁用</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <el-button v-if="isAdminLeft(row.status)" size="small" type="success" @click="enableAdminAccount(row)">启用</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                </template>
                <span v-else class="muted">—</span>
              </template>
            </DataTable>
            <AdminPager v-model:page="adminAccountPage" v-model:page-size="adminAccountPageSize" :total="adminAccountTotalPages" :count="filteredAdminAccounts.length" />
          </template>

          <template v-if="adminPage === 'rooms'">
            <!-- 【F6-4·自习室与座位】功能链实例：superadmin 新增 B 自习室并保存 → 同步 4×6 座位网格 → 在布局图里改 A-12 为「靠窗」。 本处职责：管理员维护自习室信息与座位网格，超管可删室 -->
            <div class="admin-head-actions"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <h3>自习室管理</h3> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <button v-if="isSuperAdmin" type="button" class="btn btn-primary" @click="openRoomFormCreate">新增自习室</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p v-if="!isSuperAdmin" class="scanner-hint">普通管理员仅可编辑本人负责的自习室；点击「编辑」可在同一界面管理座位网格。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p v-else class="scanner-hint">超级管理员可新增/删除自习室，并为每个自习室指定图书馆负责人。点击「编辑」可在同一界面管理座位网格。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-input v-model="roomKeyword" placeholder="搜索名称、位置或楼层" clearable /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="filter-row user-audit-filters"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button v-for="f in roomStatusFilters" :key="f.key" type="button" :class="{ active: roomStatusFilter === f.key }" @click="roomStatusFilter = f.key">{{ f.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <article class="room-item" v-for="r in pagedRooms" :key="r.id"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <div class="room-item-head"><strong>{{ r.name }}</strong><span class="mini-badge active">余 {{ r.availableSeats ?? r.available_seats ?? 0 }}</span></div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <p class="muted">{{ r.location }} · {{ r.floor || '未设置' }} · {{ roomStatusText(r.status) }}</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <div class="room-tags"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                  <span v-for="tag in parseRoomFacilities(r)" :key="tag" class="room-tag">{{ tag }}</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <button type="button" class="btn btn-outline" @click="editRoom(r)">编辑</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <button v-if="isSuperAdmin" type="button" class="btn btn-danger" @click="deleteRoom(r)">删除</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </article> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <AdminPager v-model:page="roomPage" v-model:page-size="roomPageSize" :total="roomTotalPages" :count="filteredRooms.length" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </template>

          <template v-if="adminPage === 'reservations'">
            <!-- 【F6-5·预约监管】功能链实例：小明被标「已违约」→ 管理员在预约管理点「撤销违约」→ 信用分恢复。 本处职责：管理员查全站预约，对违约单点「撤销违约」恢复信用 -->
            <p class="scanner-hint">可按学号、姓名、预约号、自习室筛选；违约记录可在此撤销并恢复信用分。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-input v-model="reservationKeyword" placeholder="搜索学号、姓名、预约号或自习室" clearable /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="filter-row user-audit-filters"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button v-for="f in reservationAdminStatusFilters" :key="f.key" type="button" :class="{ active: reservationStatusFilter === f.key }" @click="reservationStatusFilter = f.key">{{ f.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-select v-model="reservationRoomFilter" placeholder="全部自习室" clearable style="min-width:220px;margin-bottom:12px"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-option v-for="r in rooms" :key="r.id" :label="r.name" :value="r.id" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </el-select> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <DataTable :rows="pagedAdminReservations" :columns="['reservation_no','studentName','roomName','seatNo','reserve_date','status','cancel_reason']" empty-text="暂无预约记录"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <template #actions="{ row }">
                <el-button v-if="isViolatedReservation(row._rawStatus)" size="small" type="warning" @click="openRevokeViolation(row)">撤销违约</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <span v-else class="muted">—</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </template>
            </DataTable>
            <AdminPager v-model:page="reservationPage" v-model:page-size="reservationPageSize" :total="reservationTotalPages" :count="filteredAdminReservations.length" />
          </template>

          <template v-if="adminPage === 'checkins'">
            <!-- 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：admin 输入小明学号或拍照扫码签到 -->
            <div class="card scan-box"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <p class="scanner-hint">{{ scanHint || '优先「确认签到」输入学号（最稳）；拍照扫码为辅助，部分手机因照片格式/屏幕摩尔纹可能识别失败。' }}</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="scanner-toolbar"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <button type="button" class="btn btn-primary" :disabled="scanBusy" @click="triggerPhotoScan">{{ scanBusy ? '处理中…' : '拍照扫码' }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <button type="button" class="btn btn-outline" :disabled="scanBusy || !scanStudentNo.trim()" @click="scanCheckin">{{ scanBusy ? '提交中…' : '确认签到' }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <input ref="scanPhotoInput" type="file" accept="image/*" capture="environment" class="scan-photo-input" @change="onScanPhotoSelected" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="scan-student-row"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <input v-model="scanStudentNo" class="input" placeholder="请输入学生学号，如 202225220101" maxlength="20" :disabled="scanBusy" @keyup.enter="scanCheckin" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-input v-model="checkinKeyword" placeholder="搜索学号、姓名、自习室或座位" clearable /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="filter-row user-audit-filters"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button v-for="f in checkinResultFilters" :key="f.key" type="button" :class="{ active: checkinResultFilter === f.key }" @click="checkinResultFilter = f.key">{{ f.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <DataTable :rows="pagedCheckins" :columns="['studentName','roomName','seatNo','checkin_time','checkout_time','result']" empty-text="暂无签到记录" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <AdminPager v-model:page="checkinPage" v-model:page-size="checkinPageSize" :total="checkinTotalPages" :count="filteredCheckins.length" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <h3 class="section-title">实时预约</h3> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <p class="scanner-hint">待签到、使用中的预约（进入本页时自动刷新）。</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <DataTable :rows="pagedLiveReservations" :columns="['studentNo','studentName','roomName','seatNo','reserveDate','status']" empty-text="暂无进行中的预约" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <AdminPager v-model:page="liveReservationPage" v-model:page-size="liveReservationPageSize" :total="liveReservationTotalPages" :count="decoratedLiveReservations.length" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </template>

          <!-- 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：管理员在公告页点「发布公告」打开弹窗 -->
          <template v-if="adminPage === 'announcements'">
            <el-input v-model="announcementKeyword" placeholder="搜索公告标题或内容" clearable style="margin-bottom:12px" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-button type="primary" @click="editAnnouncement()">发布公告</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <article class="card announcement" v-for="a in pagedAnnouncements" :key="a.id"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <strong>{{ a.title }}</strong><p>{{ a.content }}</p> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-button size="small" @click="editAnnouncement(a)">编辑</el-button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </article> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <AdminPager v-model:page="announcementPage" v-model:page-size="announcementPageSize" :total="announcementTotalPages" :count="filteredAnnouncements.length" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </template>
          <template v-if="adminPage === 'statistics'">
            <!-- 【F6-1·统计与CSV】功能链实例：管理员打开统计页，切换当期/往期与报表类型，查看图表并导出 CSV 本处职责：管理员打开统计页，ECharts 展示使用率与趋势 -->
            <div class="admin-head-actions"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <h3>统计分析</h3> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-dropdown trigger="click" @command="handleExportCommand"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <button type="button" class="btn btn-primary"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                  📤 导出报表 ▾
                </button> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <template #dropdown>
                  <el-dropdown-menu> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-dropdown-item command="current">📊 导出当前图表数据</el-dropdown-item> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-dropdown-item command="usage" divided>座位使用率报表</el-dropdown-item> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-dropdown-item command="reservation">预约量趋势报表</el-dropdown-item> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-dropdown-item command="peak">高峰时段分析报表</el-dropdown-item> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-dropdown-item command="activity" divided>用户活跃度报表</el-dropdown-item> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-dropdown-item command="studyDuration">自习时长排名报表</el-dropdown-item> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-dropdown-item command="credit">信用与违约统计报表</el-dropdown-item> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </el-dropdown-menu> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                </template>
              </el-dropdown> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <el-select v-model="adminStatsRoomId" placeholder="全部自习室（汇总）" clearable style="width:100%;max-width:360px;margin-bottom:12px" @change="loadAdminStatistics"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-option label="全部自习室（汇总）" :value="null" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-option v-for="r in rooms" :key="r.id" :label="r.name" :value="r.id" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </el-select> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="period-tabs adminStatsRange"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button type="button" :class="{ active: adminStatsRangeMode === 'current' }" @click="changeAdminStatsRangeMode('current')">当期</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button type="button" :class="{ active: adminStatsRangeMode === 'past' }" @click="changeAdminStatsRangeMode('past')">往期</button>
            </div>
            <div class="period-tabs adminStatsPeriod">
              <button type="button" :class="{ active: adminStatsPeriod === 'day' }" @click="changeAdminStatsPeriod('day')">日报</button>
              <button type="button" :class="{ active: adminStatsPeriod === 'week' }" @click="changeAdminStatsPeriod('week')">周报</button>
              <button type="button" :class="{ active: adminStatsPeriod === 'month' }" @click="changeAdminStatsPeriod('month')">月报</button>
              <button type="button" :class="{ active: adminStatsPeriod === 'year' }" @click="changeAdminStatsPeriod('year')">年报</button>
            </div>
            <div v-if="adminStatsRangeMode === 'past'" class="admin-stats-range-row">
              <el-date-picker
                v-model="adminStatsDateRange"
                type="daterange"
                unlink-panels
                teleported
                placement="bottom-start"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
                :shortcuts="statsRangeShortcuts"
                :popper-options="{ strategy: 'fixed' }"
                popper-class="stats-date-popper"
                class="admin-stats-date-picker"
                @change="onAdminStatsDateRangeChange"
              />
              <button type="button" class="btn btn-outline" @click="resetAdminStatsDateRange">全部历史</button>
            </div>
            <div class="stat-view-tabs">
              <button type="button" :class="{ active: statAdminView === 'usage' }" @click="switchStatAdminView('usage')">使用统计</button>
              <button type="button" :class="{ active: statAdminView === 'peak' }" @click="switchStatAdminView('peak')">高峰分析</button>
              <button type="button" :class="{ active: statAdminView === 'share' }" @click="switchStatAdminView('share')">自习室占比</button>
            </div>
            <p class="scanner-hint">当前统计：{{ adminStatsScopeLabel }} · {{ adminStatsReport.summary?.periodLabel || '今日' }} · {{ adminStatsReport.summary?.rangeWindowLabel || '' }}</p>
            <div class="admin-dashboard-grid">
              <div class="stat-card"><div class="lbl">总预约</div><div class="num">{{ adminStatSummary.totalReserve }}<span class="stat-unit">次</span></div></div>
              <div class="stat-card"><div class="lbl">使用中</div><div class="num">{{ adminStatSummary.usingCount }}<span class="stat-unit">人</span></div></div>
              <div class="stat-card"><div class="lbl">签到率</div><div class="num">{{ adminStatSummary.checkinRate }}<span class="stat-unit">%</span></div></div>
              <div class="stat-card"><div class="lbl">平均信用分</div><div class="num">{{ adminStatSummary.avgCredit }}<span class="stat-unit">分</span></div></div>
            </div>
            <div class="card"><div ref="usageChart" class="chart"></div></div>
          </template>

          <template v-if="adminPage === 'feedback'">
            <el-input v-model="feedbackKeyword" placeholder="搜索学号、姓名、类型或反馈内容" clearable />
            <div class="filter-row user-audit-filters">
              <button v-for="f in feedbackStatusFilters" :key="f.key" type="button" :class="{ active: feedbackStatusFilter === f.key }" @click="feedbackStatusFilter = f.key">{{ f.label }}</button>
            </div>
            <DataTable :rows="pagedAdminFeedback" :columns="['studentName','roomName','seatNo','type','severity','content','status']" empty-text="暂无反馈">
              <template #actions="{ row }">
                <el-button v-if="isFeedbackPending(row._rawStatus)" size="small" type="primary" @click="openFeedbackHandle(row)">标记处理</el-button>
                <span v-else class="muted">已处理</span>
              </template>
            </DataTable>
            <AdminPager v-model:page="feedbackPage" v-model:page-size="feedbackPageSize" :total="feedbackTotalPages" :count="filteredAdminFeedback.length" />
          </template>

          <template v-if="adminPage === 'settings'">
            <!-- 【F6-2·系统配置】功能链实例：superadmin 把单次最长预约改为 4 小时 → 保存 → 写入 `system_config.json` → 下次预约立即按新规则校验。 本处职责：superadmin 在设置页修改预约时长、信用扣分等规则 -->
            <div class="card" style="margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center;"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <span>👤 当前管理员：<strong>{{ me.name }}</strong> ({{ me.role }})</span> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

            <!-- Tab Headers  【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div class="admin-tab-headers" style="display: flex; gap: 8px; margin-bottom: 20px; border-bottom: 2px solid #f0f2f5; padding-bottom: 8px;"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button type="button" class="tab-btn" :class="{ active: activeSettingsTab === 'config' }" @click="activeSettingsTab = 'config'" style="padding: 8px 16px; border: none; background: none; font-weight: bold; cursor: pointer; border-radius: 4px; border-bottom: 2px solid transparent; color: #606266; outline: none;">⚙️ 系统参数配置</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <button type="button" class="tab-btn" :class="{ active: activeSettingsTab === 'logs' }" @click="activeSettingsTab = 'logs'" style="padding: 8px 16px; border: none; background: none; font-weight: bold; cursor: pointer; border-radius: 4px; border-bottom: 2px solid transparent; color: #606266; outline: none;">📝 安全与操作日志</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

            <!-- Tab 1: Configuration Form  【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div v-if="activeSettingsTab === 'config'" class="card settings-config-panel" style="padding: 24px;"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <h3 style="margin-top: 0; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px;">🛠️ 全局业务规则设定</h3> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <form @submit.prevent="saveSystemConfig"> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <!-- Group 1: Booking Rules  【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <div class="config-group-title" style="font-weight: bold; color: #409eff; margin-bottom: 12px; font-size: 1.1em;">📅 预约限制规则</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px;"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">提前预约天数限制 (天)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.reservation_advance_days" :min="1" :max="30" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">单次最长预约时长 (小时)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.reservation_limit_duration" :min="1" :max="24" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">每日最多预约次数 (次)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.reservation_limit_daily" :min="1" :max="10" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

                <!-- Group 2: Credit Rules  【行】模板标记：绑定数据或事件到 Vue 实例 -->
                <div class="config-group-title" style="font-weight: bold; color: #e6a23c; margin-bottom: 12px; font-size: 1.1em;">🛡️ 信用与惩罚机制</div> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-bottom: 24px;"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">准时签到奖励分 (正数)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.credit_checkin_reward" :min="1" :max="50" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">取消预约处罚分 (负数)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.credit_cancel_penalty" :min="-200" :max="-1" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">超时违约处罚分 (负数)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.credit_violation_penalty" :min="-200" :max="-1" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">拉黑信用分阈值 (低于或等于该值拉黑)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.credit_blocked_threshold" :min="-100" :max="100" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  <div class="form-item"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                    <label style="display: block; margin-bottom: 6px; font-size: 0.9em; color: #606266;">黑名单封禁时长 (天)</label> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                    <el-input-number v-model="sysConfigForm.blacklist_days" :min="1" :max="365" style="width: 100%" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                  </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
                </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

                <div style="border-top: 1px solid #eee; padding-top: 20px; text-align: right;"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                  <button type="submit" class="btn btn-primary">💾 保存参数配置</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              </form> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->

            <!-- Tab 2: Logs  【行】模板标记：绑定数据或事件到 Vue 实例 -->
            <div v-show="activeSettingsTab === 'logs'"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              <h3>最近操作日志</h3> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <el-input v-model="logKeyword" placeholder="搜索模块、操作或详情" clearable /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <div class="filter-row user-audit-filters"> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
                <button v-for="f in logModuleFilters" :key="f.key" type="button" :class="{ active: logModuleFilter === f.key }" @click="logModuleFilter = f.key">{{ f.label }}</button> <!-- 【行】模板 UI 节点：展示学习统计页对应区域 -->
              </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <DataTable :rows="pagedOperationLogs" :columns="['module','action','target_type','detail','created_at']" empty-text="暂无操作日志" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
              <AdminPager v-model:page="logPage" v-model:page-size="logPageSize" :total="logTotalPages" :count="filteredOperationLogs.length" /> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
            </div> <!-- 【行】模板标记：绑定数据或事件到 Vue 实例 -->
          </template>
        </main>
      </div>
      <div v-if="!isDesktop" class="admin-profile-chip admin-profile-chip--mobile" aria-label="当前管理员信息" @click.stop="adminProfileMenuOpen = !adminProfileMenuOpen">
        <div class="admin-profile-avatar">{{ adminProfileInitial }}</div>
        <div class="admin-profile-meta">
          <strong>{{ me.name || me.account || '管理员' }}</strong>
          <span>{{ adminRoleLabel }}</span>
        </div>
        <div v-if="adminProfileMenuOpen" class="admin-profile-popup admin-profile-popup--mobile" @click.stop>
          <button type="button" @click="switchAdminAccount">🔄 切换账号</button>
          <button type="button" class="danger" @click="logout">🚪 退出登录</button>
        </div>
      </div>
    </section>

    <div v-if="confirmReservationOpen" class="modal-mask" @click.self="confirmReservationOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">🪑 确认预约</div>
          <button type="button" class="modal-close" @click="confirmReservationOpen = false">✕</button>
        </div>
        <div v-if="selectedSeat" class="modal-body">
          <div class="summary-row"><span>自习室</span><strong>{{ currentRoom?.name }}</strong></div>
          <div class="summary-row"><span>座位</span><strong>{{ selectedSeat.seat_no }}</strong></div>
          
          <div class="summary-row">
            <span>配置</span>
            <div class="seat-config-list" style="margin: 0; width: 100%;">
              <span :class="{ on: selectedSeat.has_power }">插座：{{ selectedSeat.has_power ? '有' : '无' }}</span>
              <span :class="{ on: selectedSeat.near_window }">靠窗：{{ selectedSeat.near_window ? '是' : '否' }}</span>
              <span :class="{ on: selectedSeat.quiet_zone }">静音：{{ selectedSeat.quiet_zone ? '是' : '否' }}</span>
              <span :class="{ on: selectedSeat.hot_seat }">热门：{{ selectedSeat.hot_seat ? '是' : '否' }}</span>
            </div>
          </div>

          <div class="reservation-confirm-edit" style="margin-top: 14px;">
            <div class="confirm-date-pills">
              <div v-for="d in dateOptions" :key="d.date" class="mini-date-pill" :class="{ active: reservationForm.date === d.date }" @click="setReservationDate(d.date)">
                <span>{{ d.label }}</span>
                <strong>{{ d.day }}</strong>
              </div>
            </div>
            <div class="confirm-time-row">
              <label>
                <span>开始时间</span>
                <el-select v-model="reservationForm.startTime" placeholder="开始" :teleported="false" @change="handleStartTimeChange">
                  <el-option v-for="t in startTimeOptions" :key="`c-s-${t}`" :label="t" :value="t" />
                </el-select>
              </label>
              <label>
                <span>结束时间</span>
                <el-select v-model="reservationForm.endTime" placeholder="结束" :teleported="false" @change="handleEndTimeChange">
                  <el-option v-for="t in endTimeOptions" :key="`c-e-${t}`" :label="t" :value="t" />
                </el-select>
              </label>
            </div>
          </div>

          <div class="summary-row"><span>时长</span><strong>{{ reservationDurationText }}</strong></div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="confirmReservationOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="createReservation">确认预约</button>
        </div>
      </div>
    </div>

    <div v-if="checkoutModalOpen" class="modal-mask" @click.self="checkoutModalOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">🎉 签退成功</div>
          <button type="button" class="modal-close" @click="checkoutModalOpen = false">✕</button>
        </div>
        <div class="modal-body" style="text-align:center">
          <div style="font-size:44px">🎊</div>
          <strong>今日学习完成！</strong>
        </div>
        <div class="card">
          <div class="summary-row"><span>自习室</span><strong>{{ checkoutSummary.roomName }}</strong></div>
          <div class="summary-row"><span>座位号</span><strong>{{ checkoutSummary.seatNo }}</strong></div>
          <div class="summary-row"><span>学习时长</span><strong>{{ checkoutSummary.minutes }} 分钟</strong></div>
          <div class="summary-row"><span>信用积分</span><strong style="color:#00b894">{{ checkoutSummary.creditChange }}</strong></div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-primary" @click="checkoutModalOpen = false">完成</button>
        </div>
      </div>
    </div>

    <div v-if="genericModal.open" class="modal-mask modal-confirm-layer" @click.self="genericModal.open = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">{{ genericModal.title }}</div>
          <button type="button" class="modal-close" @click="genericModal.open = false">✕</button>
        </div>
        <div class="modal-body">{{ genericModal.message }}</div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="genericModal.open = false">取消</button>
          <button type="button" class="btn btn-primary" @click="runGenericConfirm">确定</button>
        </div>
      </div>
    </div>

    <div v-if="adminFormOpen" class="modal-mask" @click.self="adminFormOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">{{ adminForm.id ? '编辑管理员' : '新增管理员' }}</div>
          <button type="button" class="modal-close" @click="adminFormOpen = false">✕</button>
        </div>
        <div class="dialog-form">
          <div class="field"><label>登录账号</label><input v-model="adminForm.account" class="input" :disabled="!!adminForm.id" placeholder="如 lib_admin01" /></div>
          <div class="field"><label>姓名</label><input v-model="adminForm.name" class="input" placeholder="真实姓名" /></div>
          <div class="field"><label>手机号</label><input v-model="adminForm.phone" class="input" placeholder="联系电话" /></div>
          <div class="field">
            <label>角色</label>
            <p v-if="adminForm.isSuperAdmin" class="muted admin-role-fixed">超级管理员（系统内置，不可通过此界面变更）</p>
            <p v-else class="muted admin-role-fixed">普通管理员（图书馆负责人，可分配自习室）</p>
          </div>
          <div class="field"><label>{{ adminForm.id ? '新密码（留空不改）' : '初始密码' }}</label><input v-model="adminForm.password" type="password" class="input" placeholder="6位以上" /></div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="adminFormOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="saveAdminAccount">保存</button>
        </div>
      </div>
    </div>

    <div v-if="userDetailOpen" class="modal-mask" @click.self="userDetailOpen = false">
      <div class="modal-card user-detail-modal">
        <div class="modal-head">
          <div class="modal-title">注册申请详情</div>
          <button type="button" class="modal-close" @click="userDetailOpen = false">✕</button>
        </div>
        <div class="user-detail-grid">
          <div><span>学号</span><strong>{{ userDetail.student_no || userDetail.username || '—' }}</strong></div>
          <div><span>姓名</span><strong>{{ userDetail.name || '—' }}</strong></div>
          <div><span>性别</span><strong>{{ userDetail.gender || '—' }}</strong></div>
          <div><span>学院</span><strong>{{ userDetail.college || '—' }}</strong></div>
          <div><span>专业</span><strong>{{ userDetail.major || '—' }}</strong></div>
          <div><span>年级</span><strong>{{ userDetail.grade || '—' }}</strong></div>
          <div><span>手机</span><strong>{{ userDetail.phone || '—' }}</strong></div>
          <div><span>邮箱</span><strong>{{ userDetail.email || '—' }}</strong></div>
          <div><span>审核状态</span><strong>{{ userDetail.auditLabel || auditStatusLabel(userDetail.audit_status) }}</strong></div>
          <div v-if="userDetail.audit_remark"><span>审核备注</span><strong>{{ userDetail.audit_remark }}</strong></div>
        </div>
        <div class="field user-material-block">
          <label>身份材料</label>
          <button v-if="userDetail.material_url" type="button" class="material-preview-trigger" @click="openResourcePreview(userDetail.material_url, `${userDetail.name || '学生'}身份材料`)">
            <img v-if="isImageMaterial(userDetail.material_url)" class="user-material-preview" :src="assetUrl(userDetail.material_url)" alt="身份材料" />
            <span v-else class="user-material-link">点击查看上传的材料（PDF/文件）</span>
          </button>
          <p v-else class="muted">未上传身份材料</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="userDetailOpen = false">关闭</button>
          <button v-if="isPendingAudit(userDetail.audit_status)" type="button" class="btn btn-danger" @click="rejectFromDetail">拒绝</button>
          <button v-if="isPendingAudit(userDetail.audit_status)" type="button" class="btn btn-primary" @click="approveFromDetail">通过审核</button>
        </div>
      </div>
    </div>

    <div v-if="resourcePreview.open" class="modal-mask modal-confirm-layer asset-preview-mask" @click.self="closeResourcePreview">
      <div class="modal-card asset-preview-card">
        <div class="modal-head">
          <div class="modal-title">{{ resourcePreview.title }}</div>
          <button type="button" class="modal-close" @click="closeResourcePreview">✕</button>
        </div>
        <div class="asset-preview-body">
          <img v-if="resourcePreview.kind === 'image'" class="asset-preview-image" :src="resourcePreview.url" :alt="resourcePreview.title" />
          <iframe v-else-if="resourcePreview.kind === 'pdf'" class="asset-preview-frame" :src="resourcePreview.url" :title="resourcePreview.title"></iframe>
          <div v-else class="asset-preview-file">
            <p>该材料无法直接预览，请使用下方按钮打开。</p>
          </div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="closeResourcePreview">关闭</button>
          <a class="btn btn-primary" :href="resourcePreview.url" target="_blank" rel="noopener">新窗口打开</a>
        </div>
      </div>
    </div>

    <div v-if="profileInfoOpen" class="modal-mask" @click.self="profileInfoOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">📝 个人信息</div>
          <button type="button" class="modal-close" @click="profileInfoOpen = false">✕</button>
        </div>
        <div class="dialog-form">
          <el-input v-model="profileForm.name" placeholder="姓名" />
          <el-input v-model="profileForm.phone" placeholder="手机号" />
          <el-input v-model="profileForm.email" placeholder="邮箱" />
          <el-input v-model="profileForm.college" placeholder="学院" />
          <el-input v-model="profileForm.major" placeholder="专业" />
          <el-input v-model="profileForm.grade" placeholder="年级" />
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="profileInfoOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="saveProfileAndClose">保存</button>
        </div>
      </div>
    </div>

    <div v-if="feedbackModalOpen" class="modal-mask" @click.self="feedbackModalOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">💬 问题反馈</div>
          <button type="button" class="modal-close" @click="feedbackModalOpen = false">✕</button>
        </div>
        <div class="field">
          <label>严重程度</label>
          <select v-model="feedbackForm.severity" class="input">
            <option v-for="opt in feedbackSeverityOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
          </select>
        </div>
        <div class="field">
          <label>反馈内容</label>
          <textarea v-model="feedbackForm.content" class="input" rows="5" placeholder="请输入你遇到的问题或建议"></textarea>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="feedbackModalOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="submitFeedbackModal">提交反馈</button>
        </div>
      </div>
    </div>

    <div v-if="changePasswordOpen" class="modal-mask" @click.self="changePasswordOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">🔐 修改密码</div>
          <button type="button" class="modal-close" @click="changePasswordOpen = false">✕</button>
        </div>
        <div class="dialog-form">
          <div class="field"><label>原密码</label><input v-model="changePasswordForm.oldPassword" type="password" class="input" placeholder="请输入原密码" /></div>
          <div class="field"><label>新密码</label><input v-model="changePasswordForm.newPassword" type="password" class="input" placeholder="6-20位，含字母和数字" /></div>
          <div class="field"><label>确认新密码</label><input v-model="changePasswordForm.confirmPassword" type="password" class="input" placeholder="请再次输入新密码" /></div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="changePasswordOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="submitChangePassword">保存</button>
        </div>
      </div>
    </div>

    <div v-if="rejectOpen" class="modal-mask" @click.self="rejectOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">拒绝注册申请</div>
          <button type="button" class="modal-close" @click="rejectOpen = false">✕</button>
        </div>
        <div class="field">
          <label>拒绝原因</label>
          <textarea v-model="rejectRemark" class="input" rows="4" placeholder="请填写拒绝原因"></textarea>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="rejectOpen = false">取消</button>
          <button type="button" class="btn btn-danger" @click="confirmReject">确认拒绝</button>
        </div>
      </div>
    </div>

    <div v-if="roomFormOpen" class="modal-mask modal-fullscreen">
      <div class="modal-card modal-fullscreen-card">
        <div class="modal-head modal-fullscreen-head">
          <div class="modal-title">{{ roomForm.id ? '编辑自习室' : '新增自习室' }}</div>
          <button type="button" class="modal-close" aria-label="关闭" @click="closeRoomForm">✕</button>
        </div>
        <p v-if="!isSuperAdmin" class="scanner-hint room-form-hint">可修改您负责的自习室信息；保存后请在下方座位控制区编辑格子属性。</p>
        <p v-else-if="roomForm.id" class="scanner-hint room-form-hint">修改行列数并保存后将同步座位网格；点击格子可编辑座位属性。</p>
        <p v-else class="scanner-hint room-form-hint">请填写基本信息与行列数；首次保存后将显示座位控制图。</p>
        <div class="modal-fullscreen-body room-dialog-form">
          <div class="room-row">
            <div class="field"><label>编号</label><input v-model="roomForm.roomCode" class="input" placeholder="编号" :disabled="!!roomForm.id && !isSuperAdmin" /></div>
            <div class="field"><label>名称</label><input v-model="roomForm.name" class="input" placeholder="名称" /></div>
          </div>
          <div class="room-row">
            <div class="field"><label>位置</label><input v-model="roomForm.location" class="input" placeholder="位置" /></div>
            <div class="field"><label>楼层</label><input v-model="roomForm.floor" class="input" placeholder="楼层" /></div>
          </div>
          <div class="room-row">
            <div class="field"><label>开放开始</label><input v-model="roomForm.openTime" class="input" placeholder="07:00:00" /></div>
            <div class="field"><label>开放结束</label><input v-model="roomForm.closeTime" class="input" placeholder="22:30:00" /></div>
          </div>
          <div class="field"><label>设施（逗号分隔）</label><input v-model="roomForm.facilities" class="input" placeholder="空调,WiFi" /></div>
          <div class="field"><label>分布图地址</label><input v-model="roomForm.layoutImageUrl" class="input" placeholder="上传后自动填入" /></div>
          <div class="upload-row">
            <input type="file" accept="image/*" @change="uploadLayoutImage" />
            <button v-if="roomForm.layoutImageUrl" type="button" class="layout-preview-button" @click="openResourcePreview(roomForm.layoutImageUrl, `${roomForm.name || '自习室'}布局图`)">
              <img class="layout-preview" :src="assetUrl(roomForm.layoutImageUrl)" alt="预览" />
            </button>
          </div>
          <div class="room-row">
            <div class="field"><label>行数</label><input v-model.number="roomForm.rowCount" class="input" type="number" min="1" max="20" /></div>
            <div class="field"><label>列数</label><input v-model.number="roomForm.colCount" class="input" type="number" min="1" max="20" /></div>
          </div>
          <div class="field" v-if="isSuperAdmin">
            <label>负责人（图书馆管理员）</label>
            <el-select v-model="roomForm.managerId" placeholder="请选择负责人" style="width:100%">
              <el-option v-for="a in managerOptions" :key="a.id" :label="`${a.name}（${a.account}）`" :value="a.id" />
            </el-select>
          </div>

          <section class="room-seat-section">
            <div class="room-seat-section-head">
              <h3 class="section-title">座位控制</h3>
              <button v-if="roomForm.id" type="button" class="btn btn-outline btn-sm" @click="addAdminSeat">补全座位</button>
            </div>
            <template v-if="roomForm.id">
              <p class="scanner-hint">点击格子可编辑属性；修改行列数后请先保存自习室以同步网格。删除前请确认无进行中预约。</p>
              <el-input v-model="seatKeyword" placeholder="搜索座位号或行列，如 A-12 / R1-C2" clearable />
              <div class="filter-row user-audit-filters">
                <button v-for="f in seatStatusFilters" :key="f.key" type="button" :class="{ active: seatStatusFilter === f.key }" @click="seatStatusFilter = f.key">{{ f.label }}</button>
              </div>
              <div class="seat-map-grid" :style="{ gridTemplateColumns: `repeat(${seatGridColCount}, minmax(0, 1fr))` }">
                <button
                  v-for="cell in filteredSeatGridCells"
                  :key="cell.id ? `s-${cell.id}` : `p-${cell.row_no}-${cell.col_no}`"
                  type="button"
                  class="cell-grid-btn"
                  :class="seatCellClass(cell)"
                  @click="openSeatEdit(cell)"
                >
                  <div>R{{ cell.row_no }}-C{{ cell.col_no }}</div>
                  <div class="cell-tags">
                    <span v-for="tag in seatCellTags(cell)" :key="tag" class="cell-tag">{{ tag }}</span>
                  </div>
                </button>
              </div>
            </template>
            <p v-else class="scanner-hint room-seat-placeholder">请先保存自习室基本信息，保存后此处将显示座位控制图。</p>
          </section>
        </div>
        <div class="modal-fullscreen-footer">
          <button type="button" class="btn btn-outline" @click="closeRoomForm">取消</button>
          <button type="button" class="btn btn-primary btn-block" @click="saveRoom">保存自习室</button>
        </div>
      </div>
    </div>

    <div v-if="seatEditOpen" class="modal-mask modal-seat-edit-layer" @click.self="seatEditOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">{{ seatEditForm.seat_no || '座位' }} 配置</div>
          <button type="button" class="modal-close" @click="seatEditOpen = false">✕</button>
        </div>
        <div class="dialog-form seat-edit-form">
          <label><input type="checkbox" v-model="seatEditForm.is_seat" /> 座位类单元格</label>
          <label><input type="checkbox" v-model="seatEditForm.has_power" /> 有电源</label>
          <label><input type="checkbox" v-model="seatEditForm.near_window" /> 靠窗</label>
          <label><input type="checkbox" v-model="seatEditForm.quiet_zone" /> 静音区</label>
          <label><input type="checkbox" v-model="seatEditForm.hot_seat" /> 热门座位</label>
          <label><input type="checkbox" v-model="seatEditEnabled" /> 可预约（启用）</label>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-danger" @click="deleteSeatEdit">删除座位</button>
          <button type="button" class="btn btn-outline" @click="seatEditOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="saveSeatEdit">保存</button>
        </div>
      </div>
    </div>

    <div v-if="feedbackHandleOpen" class="modal-mask" @click.self="feedbackHandleOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">处理学生反馈</div>
          <button type="button" class="modal-close" @click="feedbackHandleOpen = false">✕</button>
        </div>
        <div class="dialog-form">
          <p class="muted">学生：{{ feedbackHandleForm.studentName }} · {{ feedbackHandleForm.type }}</p>
          <p>{{ feedbackHandleForm.content }}</p>
          <div class="field"><label>处理说明</label><textarea v-model="feedbackHandleForm.handleResult" class="input" rows="4" placeholder="请填写处理结果，将通知学生"></textarea></div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="feedbackHandleOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="submitFeedbackHandle">确认处理</button>
        </div>
      </div>
    </div>

    <div v-if="revokeViolationOpen" class="modal-mask" @click.self="revokeViolationOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">撤销违约记录</div>
          <button type="button" class="modal-close" @click="revokeViolationOpen = false">✕</button>
        </div>
        <div class="dialog-form">
          <p class="muted">学生：{{ revokeViolationForm.studentName }} · 预约号 {{ revokeViolationForm.reservationNo }}</p>
          <p class="muted">{{ revokeViolationForm.roomName }} · {{ revokeViolationForm.seatNo }} · {{ revokeViolationForm.reserveDate }}</p>
          <p>撤销后将恢复该次违约扣除的信用分，并将预约标记为「已取消」。</p>
          <div class="field"><label>撤销说明（可选）</label><textarea v-model="revokeViolationForm.remark" class="input" rows="3" placeholder="如：学生已说明情况，予以撤销"></textarea></div>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-outline" @click="revokeViolationOpen = false">取消</button>
          <button type="button" class="btn btn-primary" @click="submitRevokeViolation">确认撤销</button>
        </div>
      </div>
    </div>

    <div v-if="aboutOpen" class="modal-mask" @click.self="aboutOpen = false">
      <div class="modal-card">
        <div class="modal-head">
          <div class="modal-title">ℹ️ 关于系统</div>
          <button type="button" class="modal-close" @click="aboutOpen = false">✕</button>
        </div>
        <div class="modal-body" style="text-align:center">
          <div style="font-size:48px">📚</div>
          <p><strong>校园自习室预约管理系统 V1.1</strong></p>
          <p class="muted">华南农业大学 · 数据库课程设计</p>
          <p class="muted">界面依据《原型设计.html》与概要设计文档实现。</p>
        </div>
        <div class="modal-actions">
          <button type="button" class="btn btn-primary" @click="aboutOpen = false">确定</button>
        </div>
      </div>
    </div>

    <div v-if="registerOpen" class="modal-mask" @click.self="registerOpen = false">
      <div class="modal-card register-card">
        <div class="modal-head">
          <div class="modal-title">📝 注册账号</div>
          <button type="button" class="modal-close" @click="registerOpen = false">✕</button>
        </div>
        <div class="field"><label>学号</label><input v-model="registerForm.studentNo" class="input" placeholder="请输入12位学号" /></div>
        <div class="field"><label>姓名</label><input v-model="registerForm.name" class="input" placeholder="请输入真实姓名" /></div>
        <div class="field"><label>性别</label>
          <select v-model="registerForm.gender" class="input"><option>男</option><option>女</option><option>保密</option></select>
        </div>
        <div class="field"><label>学院</label><input v-model="registerForm.college" class="input" /></div>
        <div class="field"><label>专业</label><input v-model="registerForm.major" class="input" placeholder="请输入专业名称" /></div>
        <div class="field"><label>年级</label>
          <select v-model="registerForm.grade" class="input">
            <option>2026</option><option>2025</option><option>2024</option><option>2023</option>
          </select>
        </div>
        <div class="field"><label>手机号</label><input v-model="registerForm.phone" class="input" placeholder="请输入11位手机号" /></div>
        <div class="field"><label>邮箱</label><input v-model="registerForm.email" class="input" placeholder="请输入校园邮箱" /></div>
        <div class="field"><label>身份材料上传</label><input class="input" type="file" accept=".jpg,.jpeg,.png,.pdf" @change="onRegisterFile" /></div>
        <div class="field"><label>密码</label><input v-model="registerForm.password" type="password" class="input" placeholder="6-20位，包含字母和数字" /></div>
        <div class="field"><label>确认密码</label><input v-model="registerPassword2" type="password" class="input" placeholder="请再次输入密码" /></div>
        <button type="button" class="btn btn-primary btn-block" :disabled="authLoading" @click="register">{{ authLoading ? '提交中…' : '注册' }}</button>
        <p class="muted register-foot">已有账号？<button type="button" class="link-btn" @click="registerOpen = false">立即登录</button></p>
      </div>
    </div>

    <el-dialog v-model="announcementDialog" title="公告" width="min(92vw, 620px)">
      <div class="dialog-form">
        <el-input v-model="announcementForm.title" placeholder="标题" />
        <el-input v-model="announcementForm.content" type="textarea" :rows="5" placeholder="内容" />
        <el-switch v-model="announcementForm.pinned" active-text="置顶" />
      </div>
      <template #footer><el-button type="primary" @click="saveAnnouncement">发布</el-button></template>
    </el-dialog>

    <el-dialog v-model="announcementDetailOpen" :title="activeAnnouncement.title || '公告通知'" width="min(92vw, 620px)">
      <div class="detail-dialog">
        <p>{{ activeAnnouncement.content }}</p>
        <small>{{ formatDate(activeAnnouncement.published_at || activeAnnouncement.created_at) }}</small>
      </div>
    </el-dialog>

    <el-dialog v-model="seatDialogOpen" :title="pendingSeat ? `${pendingSeat.seat_no} 座位配置` : '座位配置'" width="min(92vw, 520px)">
      <div v-if="pendingSeat" class="seat-detail-dialog">
        <div class="seat-config-list">
          <span :class="{ on: pendingSeat.has_power }">插座：{{ pendingSeat.has_power ? '有' : '无' }}</span>
          <span :class="{ on: pendingSeat.near_window }">靠窗：{{ pendingSeat.near_window ? '是' : '否' }}</span>
          <span :class="{ on: pendingSeat.quiet_zone }">静音：{{ pendingSeat.quiet_zone ? '是' : '否' }}</span>
          <span :class="{ on: pendingSeat.hot_seat }">热门：{{ pendingSeat.hot_seat ? '是' : '否' }}</span>
        </div>
        <p>座位类型：{{ pendingSeat.seat_type || '普通座位' }}</p>
        <p>当前状态：{{ pendingSeat.available ? '可预约' : seatUnavailableText(pendingSeat) }}</p>
      </div>
      <template #footer>
        <el-button @click="seatDialogOpen = false">关闭</el-button>
        <el-button type="primary" :disabled="!pendingSeat?.available" @click="confirmSeatSelection">选择该座位</el-button>
      </template>
    </el-dialog>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import * as echarts from 'echarts'
import jsQR from 'jsqr'
import { computed, defineComponent, h, nextTick, onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'
import { createQrSvg } from './qr'
import {
  ADMIN_COLUMN_LABELS,
  formatAdminCell,
  decorateReservationRow,
  decorateFeedbackRow,
  decorateCheckinRow,
  reservationStatusText
} from './admin-i18n'

const api = axios.create({ baseURL: '/api', timeout: 25000 })
const token = ref(localStorage.getItem('token') || '')
const role = ref(localStorage.getItem('role') || '')
const authLoading = ref(false)
api.interceptors.request.use(config => {
  if (token.value) config.headers.Authorization = `Bearer ${token.value}`
  return config
})
api.interceptors.response.use(res => {
  if (res.data && typeof res.data.code === 'number' && res.data.code !== 200) {
    throw new Error(res.data.message)
  }
  return res
}, err => {
  const status = err.response?.status
  const msg = err.response?.data?.message || err.message || '请求失败'
  if (status === 401 && token.value) {
    clearSession('登录已过期，请重新登录')
  }
  return Promise.reject(new Error(msg))
})

const width = ref(window.innerWidth)
const isDesktop = computed(() => width.value >= 900)
const toast = ref('')
const me = ref({})
const loginRole = ref('student')
const studentLogin = reactive({ username: '202225220101', password: '123456' })
const adminLogin = reactive({ account: 'superadmin', password: 'super123' })
const adminProfileMenuOpen = ref(false)
const registerOpen = ref(false)
const registerPassword2 = ref('')
const registerForm = reactive({ studentNo: '', name: '', gender: '男', college: '计算机科学与技术学院', major: '软件工程', grade: '2023', phone: '', email: '', password: '', materialUrl: '' })

const rooms = ref([])
const seats = ref([])
const selectedSeat = ref(null)
// 【F1-2·技术概念】功能链实例：小明点「确认预约」→ 浏览器用 **Vue** 发 **HTTP** **JSON** 到 **REST API** → **Controller** 转 **Service** 写 **MySQL** → 返回 **JSON** `… 本处职责：小明点「预约」时 studentPage='reservation'，网址不变只换内容
const studentPage = ref('home') // 【行】声明并赋值变量 `studentPage`
const reservationForm = reactive({ date: new Date().toISOString().slice(0, 10), roomId: null, startTime: '09:00', endTime: '11:00' }) // 【行】声明并赋值变量 `reservationForm`
const reservations = ref([]) // 【行】声明并赋值变量 `reservations`
const reservationStatus = ref('ALL') // 【行】声明并赋值变量 `reservationStatus`
const announcements = ref([]) // 【行】声明并赋值变量 `announcements`
const notifications = ref([]) // 【行】声明并赋值变量 `notifications`
let checkinPollTimer = null // 【行】声明并赋值变量 `checkinPollTimer`
const credit = ref({ score: 0, logs: [] }) // 【行】声明并赋值变量 `credit`
const studyStats = ref({}) // 【行】声明并赋值变量 `studyStats`
const studentChart = ref(null) // 【行】声明并赋值变量 `studentChart`
const statPeriod = ref('day') // 【行】声明并赋值变量 `statPeriod`
const announcementDetailOpen = ref(false) // 【行】声明并赋值变量 `announcementDetailOpen`
const activeAnnouncement = ref({}) // 【行】声明并赋值变量 `activeAnnouncement`
const seatDialogOpen = ref(false) // 【行】声明并赋值变量 `seatDialogOpen`
const pendingSeat = ref(null) // 【行】声明并赋值变量 `pendingSeat`
const seatFilter = ref('all') // 【行】声明并赋值变量 `seatFilter`
const seatFilterOptions = [ // 【行】声明并赋值变量 `seatFilterOptions`
  { key: 'all', label: '全部' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { key: 'power', label: '有电源' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { key: 'window', label: '靠窗' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { key: 'quiet', label: '静音' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { key: 'hot', label: '热门' }
] // 【行】执行本行语句，推进功能链中的当前步骤
const quickTimeSlots = [ // 【行】声明并赋值变量 `quickTimeSlots`
  { label: '08:00-10:00', start: '08:00', end: '10:00' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { label: '10:00-12:00', start: '10:00', end: '12:00' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { label: '14:00-16:00', start: '14:00', end: '16:00' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { label: '19:00-21:00', start: '19:00', end: '21:00' }
] // 【行】执行本行语句，推进功能链中的当前步骤
const RESERVATION_PAST_GRACE_MINUTES = 15 // 【行】声明并赋值变量 `RESERVATION_PAST_GRACE_MINUTES`
const CREDIT_SCORE_MAX = 500 // 【行】声明并赋值变量 `CREDIT_SCORE_MAX`
const RES_STATUS_MAP = { // 【行】声明并赋值变量 `RES_STATUS_MAP`
  // 【F7-3·前端状态】功能链实例：见 01 项目理解指南对应节功能链实例 本处职责：库中 PENDING/USING 等映射为页面「待使用」「使用中」
  PENDING: '待使用', USING: '使用中', COMPLETED: '已完成', CANCELLED: '已取消', // 【行】执行本行语句，推进功能链中的当前步骤
  VIOLATED: '已违约', AUTO_CANCELLED: '已违约', AUTO_CHECKOUT: '已完成', // 【行】执行本行语句，推进功能链中的当前步骤
  待签到: '待使用', 违约: '已违约', 超时取消: '已违约', 自动签退: '已完成' // 【行】执行本行语句，推进功能链中的当前步骤
}
const AUDIT_STATUS_MAP = { PENDING: '待审核', APPROVED: '已通过', REJECTED: '已拒绝' } // 【行】声明并赋值变量 `AUDIT_STATUS_MAP`
const ACCOUNT_STATUS_MAP = { NORMAL: '正常', PENDING: '待审核', DISABLED: '禁用', BLACKLIST: '黑名单', 已禁用: '禁用' } // 【行】声明并赋值变量 `ACCOUNT_STATUS_MAP`
const ADMIN_STATUS_MAP = { NORMAL: '正常', DISABLED: '离职', 禁用: '离职', 已禁用: '离职', 已离职: '离职' } // 【行】声明并赋值变量 `ADMIN_STATUS_MAP`
const ADMIN_ROLE_MAP = { ADMIN: '普通管理员', NORMAL_ADMIN: '普通管理员', SUPER_ADMIN: '超级管理员' } // 【行】声明并赋值变量 `ADMIN_ROLE_MAP`
const ROOM_STATUS_MAP = { OPEN: '开放', CLOSED: '关闭', MAINTENANCE: '维护中', MAINTAINING: '维护中' } // 【行】声明并赋值变量 `ROOM_STATUS_MAP`
const SEAT_STATUS_MAP = { NORMAL: '空闲', DAMAGED: '维修', MAINTAINING: '维修', DISABLED: '停用', 禁用: '停用' } // 【行】声明并赋值变量 `SEAT_STATUS_MAP`
const FEEDBACK_STATUS_MAP = { PENDING: '待处理', PROCESSING: '待处理', DONE: '已处理', CLOSED: '已处理' } // 【行】声明并赋值变量 `FEEDBACK_STATUS_MAP`
const CHECKIN_RESULT_MAP = { ON_TIME: '准时', LATE: '迟到', INVALID: '无效' } // 【行】声明并赋值变量 `CHECKIN_RESULT_MAP`
const canonical = (value, map) => map[value] || value || '' // 【行】声明并赋值变量 `canonical`
const reservationStatusValue = value => canonical(value, RES_STATUS_MAP) // 【行】声明并赋值变量 `reservationStatusValue`
const auditStatusValue = value => canonical(value, AUDIT_STATUS_MAP) // 【行】声明并赋值变量 `auditStatusValue`
const accountStatusValue = value => canonical(value, ACCOUNT_STATUS_MAP) // 【行】声明并赋值变量 `accountStatusValue`
const adminStatusValue = value => canonical(value, ADMIN_STATUS_MAP) // 【行】声明并赋值变量 `adminStatusValue`
const adminRoleValue = value => canonical(value, ADMIN_ROLE_MAP) // 【行】声明并赋值变量 `adminRoleValue`
const roomStatusValue = value => canonical(value, ROOM_STATUS_MAP) // 【行】声明并赋值变量 `roomStatusValue`
const seatStatusValue = value => canonical(value, SEAT_STATUS_MAP) // 【行】声明并赋值变量 `seatStatusValue`
const feedbackStatusValue = value => canonical(value, FEEDBACK_STATUS_MAP) // 【行】声明并赋值变量 `feedbackStatusValue`
const checkinResultValue = value => canonical(value, CHECKIN_RESULT_MAP) // 【行】声明并赋值变量 `checkinResultValue`
const isPendingReservation = value => reservationStatusValue(value) === '待使用' // 【行】声明并赋值变量 `isPendingReservation`
const isUsingReservation = value => reservationStatusValue(value) === '使用中' // 【行】声明并赋值变量 `isUsingReservation`
const isViolatedReservation = value => reservationStatusValue(value) === '已违约' // 【行】声明并赋值变量 `isViolatedReservation`
const isPendingAudit = value => auditStatusValue(value) === '待审核' // 【行】声明并赋值变量 `isPendingAudit`
const isApprovedAudit = value => auditStatusValue(value) === '已通过' // 【行】声明并赋值变量 `isApprovedAudit`
const isDisabledAccount = value => accountStatusValue(value) === '禁用' // 【行】声明并赋值变量 `isDisabledAccount`
const isAdminLeft = value => adminStatusValue(value) === '离职' // 【行】声明并赋值变量 `isAdminLeft`
const isSuperAdminRole = value => adminRoleValue(value) === '超级管理员' // 【行】声明并赋值变量 `isSuperAdminRole`
const isFeedbackPending = value => feedbackStatusValue(value) === '待处理' // 【行】声明并赋值变量 `isFeedbackPending`
const reservationStatusClass = value => ({ // 【行】声明并赋值变量 `reservationStatusClass`
  待使用: 'PENDING', // 【行】执行本行语句，推进功能链中的当前步骤
  使用中: 'USING', // 【行】执行本行语句，推进功能链中的当前步骤
  已完成: 'COMPLETED', // 【行】执行本行语句，推进功能链中的当前步骤
  已取消: 'CANCELLED', // 【行】执行本行语句，推进功能链中的当前步骤
  已违约: 'VIOLATED' // 【行】执行本行语句，推进功能链中的当前步骤
}[reservationStatusValue(value)] || '') // 【行】执行本行语句，推进功能链中的当前步骤
const feedbackSeverityOptions = [ // 【行】声明并赋值变量 `feedbackSeverityOptions`
  { value: '低', label: '低 — 一般建议' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { value: '中', label: '中 — 影响使用' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { value: '高', label: '高 — 较严重问题' }, // 【行】执行本行语句，推进功能链中的当前步骤
  { value: '紧急', label: '紧急 — 需立即处理' }
] // 【行】执行本行语句，推进功能链中的当前步骤
const confirmReservationOpen = ref(false) // 【行】声明并赋值变量 `confirmReservationOpen`
const checkoutModalOpen = ref(false) // 【行】声明并赋值变量 `checkoutModalOpen`
const checkoutSummary = ref({}) // 【行】声明并赋值变量 `checkoutSummary`
const profileInfoOpen = ref(false) // 【行】声明并赋值变量 `profileInfoOpen`
const feedbackModalOpen = ref(false) // 【行】声明并赋值变量 `feedbackModalOpen`
const feedbackForm = reactive({ type: '建议', severity: '中', content: '' }) // 【行】声明并赋值变量 `feedbackForm`
const roomFormOpen = ref(false) // 【行】声明并赋值变量 `roomFormOpen`
const seatEditOpen = ref(false) // 【行】声明并赋值变量 `seatEditOpen`
const seatEditForm = reactive({}) // 【行】声明并赋值变量 `seatEditForm`
const seatEditEnabled = computed({ // 【行】声明并赋值变量 `seatEditEnabled`
  get: () => seatStatusValue(seatEditForm.status) === '空闲', // 【行】执行本行语句，推进功能链中的当前步骤
  set: val => { seatEditForm.status = val ? '空闲' : '停用' }
}) // 【行】执行本行语句，推进功能链中的当前步骤
const adminStatsPeriod = ref('week') // 【行】声明并赋值变量 `adminStatsPeriod`
const adminStatsRangeMode = ref('current') // 【行】声明并赋值变量 `adminStatsRangeMode`
const adminStatsRoomId = ref(null) // 【行】声明并赋值变量 `adminStatsRoomId`
const adminStatsDateRange = ref(null) // 【行】声明并赋值变量 `adminStatsDateRange`
const adminStatsRangeTouched = ref(false) // 【行】声明并赋值变量 `adminStatsRangeTouched`
const studyStatsRangeMode = ref('current') // 【行】声明并赋值变量 `studyStatsRangeMode`
const studyStatsStartDate = ref(null) // 【行】声明并赋值变量 `studyStatsStartDate`
const studyStatsEndDate = ref(null) // 【行】声明并赋值变量 `studyStatsEndDate`
const studyStatsRangeTouched = ref(false) // 【行】声明并赋值变量 `studyStatsRangeTouched`
/** 学生端单日历 popper 固定 322px，避免随 200px 输入框收缩导致只显示 3 列 */
const statsSingleDatePopperStyle = Object.freeze({ width: '322px', minWidth: '322px', padding: '0' }) // 【行】声明并赋值变量 `statsSingleDatePopperStyle`
const statsSingleDatePopperOptions = Object.freeze({ strategy: 'fixed' }) // 【行】声明并赋值变量 `statsSingleDatePopperOptions`
const statsRangeShortcuts = [ // 【行】声明并赋值变量 `statsRangeShortcuts`
  {
    text: '近30天', // 【行】执行本行语句，推进功能链中的当前步骤
    value: () => { // 【行】进入代码块
      const end = new Date() // 【行】声明并赋值变量 `end`
      end.setDate(end.getDate() - 1) // 【行】执行本行语句，推进功能链中的当前步骤
      const start = new Date(end) // 【行】声明并赋值变量 `start`
      start.setDate(start.getDate() - 29) // 【行】执行本行语句，推进功能链中的当前步骤
      return [toDateValue(start), toDateValue(end)] // 【行】返回本函数计算结果给调用方
    }
  },
  {
    text: '近12个月', // 【行】执行本行语句，推进功能链中的当前步骤
    value: () => { // 【行】进入代码块
      const end = new Date() // 【行】声明并赋值变量 `end`
      end.setDate(end.getDate() - 1) // 【行】执行本行语句，推进功能链中的当前步骤
      const start = new Date(end) // 【行】声明并赋值变量 `start`
      start.setMonth(start.getMonth() - 11) // 【行】执行本行语句，推进功能链中的当前步骤
      start.setDate(1) // 【行】执行本行语句，推进功能链中的当前步骤
      return [toDateValue(start), toDateValue(end)] // 【行】返回本函数计算结果给调用方
    }
  },
  {
    text: '今年以来', // 【行】执行本行语句，推进功能链中的当前步骤
    value: () => { // 【行】进入代码块
      const end = new Date() // 【行】声明并赋值变量 `end`
      end.setDate(end.getDate() - 1) // 【行】执行本行语句，推进功能链中的当前步骤
      const start = new Date(end.getFullYear(), 0, 1) // 【行】声明并赋值变量 `start`
      return [toDateValue(start), toDateValue(end)] // 【行】返回本函数计算结果给调用方
    }
  }
] // 【行】执行本行语句，推进功能链中的当前步骤
const userPage = ref(1)
const DEFAULT_ADMIN_PAGE_SIZE = 10
const ADMIN_PAGE_SIZE_OPTIONS = [5, 10, 20, 50]
const userPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const adminAccountPage = ref(1)
const adminAccountPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const reservationPage = ref(1)
const reservationPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const checkinPage = ref(1)
const checkinPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const liveReservationPage = ref(1)
const liveReservationPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const feedbackPage = ref(1)
const feedbackPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const logPage = ref(1)
const logPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const roomPage = ref(1)
const roomPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const announcementPage = ref(1)
const announcementPageSize = ref(DEFAULT_ADMIN_PAGE_SIZE)
const adminAccounts = ref([])
const adminFormOpen = ref(false)
const adminForm = reactive({ id: null, account: '', name: '', phone: '', password: '', isSuperAdmin: false })
const rejectRemark = ref('')
const rejectUserId = ref(null)
const rejectOpen = ref(false)
const userDetailOpen = ref(false)
const userDetail = ref({})
const changePasswordOpen = ref(false)
const changePasswordForm = reactive({ oldPassword: '', newPassword: '', confirmPassword: '' })
const userAuditFilter = ref('')
const userAuditFilters = [
  { key: '', label: '全部' },
  { key: '待审核', label: '待审核' },
  { key: '已通过', label: '已通过' },
  { key: '已拒绝', label: '已拒绝' }
]
const genericModal = reactive({ open: false, title: '', message: '', onConfirm: null })
const resourcePreview = reactive({ open: false, title: '', url: '', kind: 'file' })
const studySeconds = ref(0)
const statAdminView = ref('usage')
const liveReservations = ref([])
const aboutOpen = ref(false)
const notifyPrefs = reactive({ reservation: true, checkin: true, announcement: true, dnd: false })
let studyTimerHandle = null

const adminPage = ref('checkins')
const users = ref([])
const userKeyword = ref('')
const adminReservations = ref([])
const checkins = ref([])
const adminFeedback = ref([])
const adminStatsReport = ref({ summary: {}, usage: [], peak: [], trend: [], credit: [] })
const feedbackHandleOpen = ref(false)
const feedbackHandleForm = reactive({ id: null, studentName: '', type: '', content: '', handleResult: '' })
const adminSeats = ref([])
const scanStudentNo = ref('')
const scanPhotoInput = ref(null)
const scanHint = ref('')
const scanBusy = ref(false)
const checkinQrSvg = ref('')
const usageChart = ref(null)
const roomForm = reactive({})
const announcementDialog = ref(false)
const announcementForm = reactive({})
const profileForm = reactive({ name: '', phone: '', email: '', college: '', major: '', grade: '' })
const operationLogs = ref([])
const adminKeyword = ref('')
const adminStatusFilter = ref('')
const roomKeyword = ref('')
const roomStatusFilter = ref('')
const seatKeyword = ref('')
const seatStatusFilter = ref('')
const reservationKeyword = ref('')
const reservationStatusFilter = ref('')
const reservationRoomFilter = ref(null)
const checkinKeyword = ref('')
const checkinResultFilter = ref('')
const announcementKeyword = ref('')
const feedbackKeyword = ref('')
const feedbackStatusFilter = ref('')
const logKeyword = ref('')
const logModuleFilter = ref('')
const activeSettingsTab = ref('config')
const sysConfigForm = reactive({
  reservation_advance_days: 7,
  reservation_limit_duration: 4,
  reservation_limit_daily: 3,
  credit_checkin_reward: 5,
  credit_cancel_penalty: -50,
  credit_violation_penalty: -50,
  credit_blocked_threshold: 0,
  blacklist_days: 7
})
const revokeViolationOpen = ref(false)
const revokeViolationForm = reactive({ id: null, studentName: '', reservationNo: '', roomName: '', seatNo: '', reserveDate: '', remark: '' })
const adminStatusFilters = [{ key: '', label: '全部' }, { key: '正常', label: '正常' }, { key: '离职', label: '离职' }]
const roomStatusFilters = [{ key: '', label: '全部' }, { key: '开放', label: '开放' }, { key: '关闭', label: '关闭' }, { key: '维护中', label: '维护中' }]
const seatStatusFilters = [{ key: '', label: '全部' }, { key: '空闲', label: '空闲' }, { key: '维修', label: '维修' }, { key: '停用', label: '停用' }]
const reservationAdminStatusFilters = [
  { key: '', label: '全部' }, { key: '待使用', label: '待使用' }, { key: '使用中', label: '使用中' },
  { key: '已完成', label: '已完成' }, { key: '已取消', label: '已取消' }, { key: '已违约', label: '已违约' }
]
const checkinResultFilters = [{ key: '', label: '全部' }, { key: '准时', label: '准时' }, { key: '迟到', label: '迟到' }, { key: '无效', label: '无效' }]
const feedbackStatusFilters = [{ key: '', label: '全部' }, { key: '待处理', label: '待处理' }, { key: '已处理', label: '已处理' }]
const logModuleFilters = [{ key: '', label: '全部' }, { key: '用户', label: '用户' }, { key: '自习室', label: '自习室' }, { key: '预约', label: '预约' }, { key: '反馈', label: '反馈' }]
const todayText = computed(() => new Date().toLocaleDateString('zh-CN', { weekday: 'long', month: 'long', day: 'numeric' }))
const studentNoDisplay = computed(() => me.value.student_no || me.value.username || '—')
const homeDateText = computed(() => `${new Date().getMonth() + 1}月${new Date().getDate()}日`)
const unreadCount = computed(() => notifications.value.filter(n => !n.read_flag).length)
const currentRoom = computed(() => rooms.value.find(r => r.id === reservationForm.roomId))
const seatGridRoom = computed(() => {
  if (!roomFormOpen.value || !roomForm.id) return null
  const r = rooms.value.find(x => Number(x.id) === Number(roomForm.id))
  return {
    ...r,
    col_count: roomForm.colCount || r?.col_count || r?.colCount || 6,
    row_count: roomForm.rowCount || r?.row_count || r?.rowCount || 4
  }
})
const seatGridColCount = computed(() => Math.max(1, Number(seatGridRoom.value?.col_count || seatGridRoom.value?.colCount || roomForm.colCount || 6)))
const seatGridRowCount = computed(() => Math.max(1, Number(seatGridRoom.value?.row_count || seatGridRoom.value?.rowCount || roomForm.rowCount || 4)))
const seatGridCells = computed(() => {
  const rows = seatGridRowCount.value
  const cols = seatGridColCount.value
  const byPos = {}
  for (const s of adminSeats.value) {
    byPos[`${s.row_no}-${s.col_no}`] = s
  }
  const cells = []
  for (let r = 1; r <= rows; r++) {
    for (let c = 1; c <= cols; c++) {
      const found = byPos[`${r}-${c}`]
      cells.push(found || {
        row_no: r,
        col_no: c,
        is_seat: 1,
        status: '空闲',
        seat_no: `R${r}-C${c}`,
        placeholder: true
      })
    }
  }
  return cells
})
const todayReservation = computed(() => reservations.value.find(r => String(r.reserve_date).startsWith(reservationForm.date) && ['待使用', '使用中'].includes(reservationStatusValue(r.status))))
const activeReservation = computed(() => reservations.value.find(r => ['待使用', '使用中'].includes(reservationStatusValue(r.status))))
function parseReservationDateTime(r, timeField = 'start_time') {
  if (!r) return null
  const rawDate = r.reserve_date ?? r.reserveDate
  let datePart = ''
  if (rawDate instanceof Date) {
    datePart = rawDate.toISOString().slice(0, 10)
  } else {
    datePart = String(rawDate || '').replace(' ', 'T').slice(0, 10)
  }
  const altTime = timeField === 'start_time' ? 'startTime' : 'endTime'
  const rawTime = r[timeField] ?? r[altTime] ?? '00:00:00'
  const timePart = String(rawTime).slice(0, 8)
  const [y, mo, d] = datePart.split('-').map(n => Number(n))
  const [hh, mm, ss = 0] = timePart.split(':').map(n => Number(n))
  if (!y || !mo || !d) return null
  return new Date(y, mo - 1, d, hh || 0, mm || 0, ss || 0)
}
function reservationStartDate(r) {
  return parseReservationDateTime(r, 'start_time')
}
function isWithinCheckinWindow(r) {
  const start = reservationStartDate(r)
  if (!start || Number.isNaN(start.getTime())) return false
  const windowStart = start.getTime() - 15 * 60 * 1000
  const windowEnd = start.getTime() + 15 * 60 * 1000
  const now = Date.now()
  return now >= windowStart && now <= windowEnd
}
const checkinWindowHint = computed(() => {
  const r = activeReservation.value
  if (!r || reservationStatusValue(r.status) !== '待使用') return ''
  const start = reservationStartDate(r)
  if (!start) return '请在预约开始前后 15 分钟内完成签到。'
  const windowStart = new Date(start.getTime() - 15 * 60 * 1000)
  const windowEnd = new Date(start.getTime() + 15 * 60 * 1000)
  const fmt = (dt) => dt.toLocaleString('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })
  if (Date.now() < windowStart.getTime()) {
    return `签到尚未开始，开放时间：${fmt(windowStart)} 至 ${fmt(windowEnd)}`
  }
  if (Date.now() > windowEnd.getTime()) {
    return '签到时间已过，请等待系统处理或联系管理员。'
  }
  return '请在预约开始前后 15 分钟内完成签到。'
})
const timerText = computed(() => {
  if (!activeReservation.value) return '00:00:00'
  if (reservationStatusValue(activeReservation.value.status) === '使用中') return formatStudyTime(studySeconds.value)
  return '00:00:00'
})
const groupedSeats = computed(() => {
  const order = ['热门区', '静音区', '开放座位', '非座位区']
  const map = {}
  for (const s of seats.value) {
    const name = resolveSeatSection(s)
    if (!map[name]) map[name] = []
    map[name].push(s)
  }
  return order.filter(name => map[name]?.length).map(name => ({
    name,
    seats: map[name],
    availableCount: map[name].filter(s => s.is_seat && s.available).length
  }))
})
const studentTitle = computed(() => ({ home: '首页', reservation: '座位预约', checkin: '签到签退', profile: '我的', myres: '我的预约', credit: '信用积分', stats: '学习统计', notifications: '消息通知', settings: '设置', feedback: '问题反馈' }[studentPage.value] || '首页'))
const shownReservations = computed(() => reservationStatus.value === 'ALL' ? reservations.value : reservations.value.filter(r => reservationStatusValue(r.status) === reservationStatus.value))
const availableSeatCount = computed(() => seats.value.filter(s => s.available).length)
const roomLayoutImage = computed(() => currentRoom.value?.layout_image_url || currentRoom.value?.layoutImageUrl || '')
const RESERVATION_SLOT_STEP_MINUTES = 10
/** 从自习室实体读取 HH:mm（兼容 open_time / openTime） */
function roomTimePart(room, field, fallback) {
  if (!room) return fallback
  const camel = field.replace(/_([a-z])/g, (_, c) => c.toUpperCase())
  const raw = room[field] ?? room[camel] ?? fallback
  return String(raw).slice(0, 5)
}
const currentRoomOpenTime = computed(() => roomTimePart(currentRoom.value, 'open_time', '07:00'))
const currentRoomCloseTime = computed(() => roomTimePart(currentRoom.value, 'close_time', '22:30'))
/** 最晚开始 = 关闭时间 - 一个时段步长（如 23:30 关则可约 23:20 起） */
const latestReservationStartTime = computed(() => {
  const closeM = timeToMinutes(currentRoomCloseTime.value)
  return minutesToTime(Math.max(0, closeM - RESERVATION_SLOT_STEP_MINUTES))
})
const endSelectStart = computed(() => addMinutes(reservationForm.startTime, RESERVATION_SLOT_STEP_MINUTES))
const todayDateValue = computed(() => toDateValue(new Date()))
const minStartTimeToday = computed(() => {
  const cutoff = new Date(Date.now() - RESERVATION_PAST_GRACE_MINUTES * 60 * 1000)
  let mins = cutoff.getHours() * 60 + cutoff.getMinutes()
  mins = Math.ceil(mins / RESERVATION_SLOT_STEP_MINUTES) * RESERVATION_SLOT_STEP_MINUTES
  if (mins >= 24 * 60) return latestReservationStartTime.value
  const todayMin = minutesToTime(mins)
  return minutesToTime(Math.max(timeToMinutes(currentRoomOpenTime.value), timeToMinutes(todayMin)))
})
const startTimeSelectMin = computed(() => (
  reservationForm.date === todayDateValue.value ? minStartTimeToday.value : currentRoomOpenTime.value
))
const startTimeOptions = computed(() => buildReservationTimeOptions(
  startTimeSelectMin.value, latestReservationStartTime.value, RESERVATION_SLOT_STEP_MINUTES))
const endTimeOptions = computed(() => buildReservationTimeOptions(
  endSelectStart.value, currentRoomCloseTime.value, RESERVATION_SLOT_STEP_MINUTES))
const availableQuickTimeSlots = computed(() => {
  const openM = timeToMinutes(currentRoomOpenTime.value)
  const closeM = timeToMinutes(currentRoomCloseTime.value)
  return quickTimeSlots.map(slot => {
    const startM = timeToMinutes(slot.start)
    const endM = timeToMinutes(slot.end)
    const outOfRoom = startM < openM || endM > closeM
    return {
      ...slot,
      expired: isQuickSlotExpired(slot) || outOfRoom
    }
  })
})
const dateOptions = computed(() => Array.from({ length: 7 }, (_, i) => {
  const d = new Date()
  d.setDate(d.getDate() + i)
  return {
    date: toDateValue(d),
    label: i === 0 ? '今天' : ['周日', '周一', '周二', '周三', '周四', '周五', '周六'][d.getDay()],
    day: String(d.getDate()).padStart(2, '0'),
    month: d.getMonth() + 1
  }
}))
const activeStudentTab = computed(() => ['myres', 'credit', 'stats', 'settings', 'feedback'].includes(studentPage.value) ? 'profile' : studentPage.value)
const creditBlocked = computed(() => Number(credit.value.score ?? me.value.credit_score ?? 300) <= 0)
const creditPercent = computed(() => Math.min(100, Math.round(Number(credit.value.score || 0) / CREDIT_SCORE_MAX * 100)))
const creditLevel = computed(() => Number(credit.value.score || 0) >= 280 ? '优秀' : Number(credit.value.score || 0) >= 200 ? '良好' : '需改进')
const checkinCount = computed(() => credit.value.logs?.filter(l => String(l.reason || '').includes('签到')).length || 0)
const violationCount = computed(() => reservations.value.filter(r => reservationStatusValue(r.status) === '已违约').length)
const totalStudyHours = computed(() => ((studyStats.value.totalMinutes || 0) / 60).toFixed(1).replace('.0', ''))
const studyDays = computed(() => Number(studyStats.value.studyDayCount ?? studyStats.value.series?.length ?? 0))
const averageStudyHours = computed(() => {
  const divisor = Math.max(1, Number(studyStats.value.studyDayCount ?? studyStats.value.series?.length ?? 0))
  return (((studyStats.value.totalMinutes || 0) / 60) / divisor).toFixed(1).replace('.0', '')
})
const studyChartTitle = computed(() => {
  const past = studyStatsRangeMode.value === 'past'
  const titles = {
    day: past ? '往期每日学习时长（小时）' : '今日各时段学习时长（小时）',
    week: past ? '往期每周学习时长（小时）' : '本周每日学习时长（小时）',
    month: past ? '往期每月学习时长（小时）' : '本月每周学习时长（小时）',
    year: past ? '往年年报每月学习时长（小时）' : '本年年报每月学习时长（小时）'
  }
  return titles[statPeriod.value] || '学习时长（小时）'
})
const studyStatsHint = computed(() => {
  const parts = [studyStats.value.periodLabel, studyStats.value.rangeWindowLabel].filter(Boolean)
  return parts.length ? parts.join(' · ') : ''
})
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：studyBars 将 API series 转为 bar-chart-lite 所需的 {label,value} 数组 */
const studyBars = computed(() => { // 【行】声明并赋值变量 `studyBars`
  const rows = studyStats.value.series || [] // 【行】声明并赋值变量 `rows`
  if (statPeriod.value === 'year' || (statPeriod.value === 'month' && studyStatsRangeMode.value === 'past')) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return buildYearStudyBars(rows) // 【行】返回本函数计算结果给调用方
  }
  if (rows.length) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return rows.map(row => ({ // 【行】返回本函数计算结果给调用方
      label: formatStudyLabel(row.label), // 【行】执行本行语句，推进功能链中的当前步骤
      value: Number(((Number(row.minutes || 0)) / 60).toFixed(1)) // 【行】执行本行语句，推进功能链中的当前步骤
    })) // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (statPeriod.value === 'day') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return [8, 10, 12, 14, 16, 18, 20, 22].map(hour => ({ label: `${hour}时`, value: 0 })) // 【行】返回本函数计算结果给调用方
  }
  if (statPeriod.value === 'year') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return buildYearStudyBars([]) // 【行】返回本函数计算结果给调用方
  }
  const days = statPeriod.value === 'month' ? 30 : 7 // 【行】声明并赋值变量 `days`
  return Array.from({ length: days }, (_, i) => ({ label: `${i + 1}`, value: 0 })) // 【行】返回本函数计算结果给调用方
}) // 【行】执行本行语句，推进功能链中的当前步骤
const maxStudyBarValue = computed(() => Math.max(1, ...studyBars.value.map(b => Number(b.value || 0)))) // 【行】柱图纵轴上限：取 studyBars 最大值与 1 的较大者，避免全 0 时除零
const studyAdvice = computed(() => { // 【行】根据日报/周期总时长生成中文学习建议文案
  if (statPeriod.value === 'day') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return Number(totalStudyHours.value) >= 3 ? '你今日的学习效率较高，建议保持。最佳学习时段为上午9-11点。' : '建议增加连续学习时长，并优先预约上午或下午的稳定时段。' // 【行】返回本函数计算结果给调用方
  }
  return Number(averageStudyHours.value) >= 2 ? '本周期学习节奏较稳定，建议继续保持固定预约习惯。' : '建议提高每次学习的连续时长，并保持每周稳定到馆。' // 【行】返回本函数计算结果给调用方
}) // 【行】执行本行语句，推进功能链中的当前步骤

const statPeriods = [{ key: 'day', label: '日报' }, { key: 'week', label: '周报' }, { key: 'month', label: '月报' }, { key: 'year', label: '年报' }] // 【行】声明并赋值变量 `statPeriods`
const reservationTabs = [{ key: 'ALL', label: '全部' }, { key: '待使用', label: '待使用' }, { key: '使用中', label: '使用中' }, { key: '已完成', label: '已完成' }, { key: '已取消', label: '已取消' }] // 【行】声明并赋值变量 `reservationTabs`
const studentNav = [{ page: 'home', label: '首页', icon: '🏠' }, { page: 'reservation', label: '预约', icon: '🪑' }, { page: 'checkin', label: '签到', icon: '✅' }, { page: 'profile', label: '我的', icon: '👤' }] // 【行】声明并赋值变量 `studentNav`
/** 【F2-2·管理员登录】功能链实例：管理员切到「管理员登录」→ 输入 `admin` / `admin123` → 进入管理端签到页；`superadmin` 侧栏额外显示「设置」「管理员管理」。 本处职责：superadmin 登录后 isSuperAdmin 为 true，侧栏显示「设置」*/
const isSuperAdmin = computed(() => role.value === 'SUPER_ADMIN') // 【行】声明并赋值变量 `isSuperAdmin`
const adminRoleLabel = computed(() => { // 【行】声明并赋值变量 `adminRoleLabel`
  if (role.value === 'SUPER_ADMIN') return '超级管理员' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (role.value === 'ADMIN') return '普通管理员' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  return role.value || '管理员' // 【行】返回本函数计算结果给调用方
}) // 【行】执行本行语句，推进功能链中的当前步骤
const adminProfileInitial = computed(() => { // 【行】管理员头像首字母：取姓名或账号首字符
  const name = String(me.value.name || me.value.account || '管').trim() // 【行】声明并赋值变量 `name`
  return name.slice(0, 1).toUpperCase() // 【行】返回本函数计算结果给调用方
}) // 【行】执行本行语句，推进功能链中的当前步骤
const adminNav = computed(() => { // 【行】侧栏菜单：超管额外含设置与管理员管理
  const items = [ // 【行】声明并赋值变量 `items`
    { page: 'checkins', label: '签到', icon: '✅' }, // 【行】执行本行语句，推进功能链中的当前步骤
    { page: 'users', label: '用户管理', icon: '👥' }
  ] // 【行】执行本行语句，推进功能链中的当前步骤
  if (isSuperAdmin.value) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    items.push({ page: 'admins', label: '管理员管理', icon: '🛡️' }) // 【行】执行本行语句，推进功能链中的当前步骤
    items.push({ page: 'settings', label: '设置', icon: '⚙️' }) // 【行】执行本行语句，推进功能链中的当前步骤
  }
  items.push( // 【行】执行本行语句，推进功能链中的当前步骤
    { page: 'rooms', label: '自习室', icon: '🏫' }, // 【行】执行本行语句，推进功能链中的当前步骤
    { page: 'reservations', label: '预约', icon: '📅' }, // 【行】执行本行语句，推进功能链中的当前步骤
    { page: 'announcements', label: '公告', icon: '📣' }, // 【行】执行本行语句，推进功能链中的当前步骤
    { page: 'statistics', label: '统计', icon: '📈' }, // 【行】执行本行语句，推进功能链中的当前步骤
    { page: 'feedback', label: '反馈', icon: '💬' }
  )
  return items // 【行】返回本函数计算结果给调用方
}) // 【行】执行本行语句，推进功能链中的当前步骤
const adminAccountColumns = ['account', 'name', 'roleLabel', 'phone', 'managedRooms', 'statusLabel'] // 【行】声明并赋值变量 `adminAccountColumns`
const managerOptions = computed(() => adminAccounts.value.filter(a => adminRoleValue(a.role) === '普通管理员' && !isAdminLeft(a.status))) // 【行】筛选可分配自习室的普通管理员列表
const decoratedAdminAccounts = computed(() => adminAccounts.value.map(row => ({ // 【行】管理员表格行：附加 roleLabel/statusLabel 展示字段
  ...row, // 【行】执行本行语句，推进功能链中的当前步骤
  roleLabel: adminRoleValue(row.role) || '普通管理员', // 【行】执行本行语句，推进功能链中的当前步骤
  statusLabel: adminStatusValue(row.status) || '正常', // 【行】执行本行语句，推进功能链中的当前步骤
  managedRooms: row.managedRooms || '—' // 【行】执行本行语句，推进功能链中的当前步骤
}))) // 【行】执行本行语句，推进功能链中的当前步骤
function normalizePageSize(pageSize) { // 【行】进入代码块
  const size = Number(pageSize) // 【行】声明并赋值变量 `size`
  return ADMIN_PAGE_SIZE_OPTIONS.includes(size) ? size : DEFAULT_ADMIN_PAGE_SIZE // 【行】返回本函数计算结果给调用方
}
function paginateRows(rows, page, pageSize = DEFAULT_ADMIN_PAGE_SIZE) { // 【行】进入代码块
  const safePageSize = normalizePageSize(pageSize) // 【行】声明并赋值变量 `safePageSize`
  const total = pagerTotal(rows.length, safePageSize) // 【行】声明并赋值变量 `total`
  const safePage = Math.min(Math.max(1, page), total) // 【行】声明并赋值变量 `safePage`
  const start = (safePage - 1) * safePageSize // 【行】声明并赋值变量 `start`
  return rows.slice(start, start + safePageSize) // 【行】返回本函数计算结果给调用方
}
function pagerTotal(count, pageSize = DEFAULT_ADMIN_PAGE_SIZE) { // 【行】进入代码块
  return Math.max(1, Math.ceil(Math.max(0, count) / normalizePageSize(pageSize))) // 【行】返回本函数计算结果给调用方
}
function matchAdminKeyword(row, keyword, fields) { // 【行】进入代码块
  const q = String(keyword || '').trim().toLowerCase() // 【行】声明并赋值变量 `q`
  if (!q) return true // 【行】条件不满足时提前结束，避免无效请求或错误状态
  return fields.some(f => String(row[f] ?? '').toLowerCase().includes(q)) // 【行】返回本函数计算结果给调用方
}
const filteredAdminAccounts = computed(() => { // 【行】声明并赋值变量 `filteredAdminAccounts`
  let rows = decoratedAdminAccounts.value // 【行】声明并赋值变量 `rows`
  if (adminStatusFilter.value) rows = rows.filter(r => adminStatusValue(r.status) === adminStatusFilter.value) // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  return rows.filter(r => matchAdminKeyword(r, adminKeyword.value, ['account', 'name', 'phone', 'managedRooms'])) // 【行】返回本函数计算结果给调用方
}) // 【行】执行本行语句，推进功能链中的当前步骤
const pagedAdminAccounts = computed(() => paginateRows(filteredAdminAccounts.value, adminAccountPage.value, adminAccountPageSize.value)) // 【行】声明并赋值变量 `pagedAdminAccounts`
const adminAccountTotalPages = computed(() => pagerTotal(filteredAdminAccounts.value.length, adminAccountPageSize.value)) // 【行】声明并赋值变量 `adminAccountTotalPages`
const filteredRooms = computed(() => { // 【行】声明并赋值变量 `filteredRooms`
  let rows = rooms.value // 【行】声明并赋值变量 `rows`
  if (roomStatusFilter.value) rows = rows.filter(r => roomStatusValue(r.status) === roomStatusFilter.value) // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  return rows.filter(r => matchAdminKeyword(r, roomKeyword.value, ['name', 'location', 'floor', 'room_code'])) // 【行】返回本函数计算结果给调用方
}) // 【行】执行本行语句，推进功能链中的当前步骤
const pagedRooms = computed(() => paginateRows(filteredRooms.value, roomPage.value, roomPageSize.value)) // 【行】声明并赋值变量 `pagedRooms`
const roomTotalPages = computed(() => pagerTotal(filteredRooms.value.length, roomPageSize.value)) // 【行】声明并赋值变量 `roomTotalPages`
const filteredSeatGridCells = computed(() => { // 【行】声明并赋值变量 `filteredSeatGridCells`
  let cells = seatGridCells.value // 【行】声明并赋值变量 `cells`
  if (seatStatusFilter.value) cells = cells.filter(c => seatStatusValue(c.status || '空闲') === seatStatusFilter.value) // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  const q = String(seatKeyword.value || '').trim().toLowerCase() // 【行】声明并赋值变量 `q`
  if (!q) return cells // 【行】条件不满足时提前结束，避免无效请求或错误状态
  return cells.filter(c => { // 【行】返回本函数计算结果给调用方
    const label = `R${c.row_no}-C${c.col_no} ${c.seat_no || ''}`.toLowerCase() // 【行】声明并赋值变量 `label`
    return label.includes(q) // 【行】返回本函数计算结果给调用方
  }) // 【行】执行本行语句，推进功能链中的当前步骤
}) // 【行】执行本行语句，推进功能链中的当前步骤
const sortedAnnouncements = computed(() => [...announcements.value].sort((a, b) => Number(b.pinned || 0) - Number(a.pinned || 0))) // 【行】声明并赋值变量 `sortedAnnouncements`
const pagedUsers = computed(() => paginateRows(users.value, userPage.value, userPageSize.value)) // 【行】声明并赋值变量 `pagedUsers`
const userTotalPages = computed(() => pagerTotal(users.value.length, userPageSize.value)) // 【行】声明并赋值变量 `userTotalPages`
const decoratedLiveReservations = computed(() => // 【行】声明并赋值变量 `decoratedLiveReservations`
  (liveReservations.value || []).map(r => ({ // 【行】进入代码块
    ...r, // 【行】执行本行语句，推进功能链中的当前步骤
    reserveDate: formatDate(r.reserveDate || r.reserve_date), // 【行】执行本行语句，推进功能链中的当前步骤
    status: reservationStatusText(r.status) // 【行】执行本行语句，推进功能链中的当前步骤
  })) // 【行】执行本行语句，推进功能链中的当前步骤
)
const decoratedAdminReservations = computed(() => adminReservations.value.map(r => ({ // 【行】声明并赋值变量 `decoratedAdminReservations`
  ...decorateReservationRow(r), // 【行】执行本行语句，推进功能链中的当前步骤
  _rawStatus: r.status, // 【行】执行本行语句，推进功能链中的当前步骤
  _rawId: r.id, // 【行】执行本行语句，推进功能链中的当前步骤
  cancel_reason: r.cancel_reason || '—' // 【行】执行本行语句，推进功能链中的当前步骤
}))) // 【行】执行本行语句，推进功能链中的当前步骤
const filteredAdminReservations = computed(() => { // 【行】声明并赋值变量 `filteredAdminReservations`
  let rows = decoratedAdminReservations.value // 【行】声明并赋值变量 `rows`
  if (reservationStatusFilter.value) rows = rows.filter(r => reservationStatusValue(r._rawStatus) === reservationStatusFilter.value) // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (reservationRoomFilter.value) rows = rows.filter(r => Number(r.room_id) === Number(reservationRoomFilter.value)) // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  return rows.filter(r => matchAdminKeyword(r, reservationKeyword.value, [ // 【行】返回本函数计算结果给调用方
    'student_no', 'studentNo', 'studentName', 'roomName', 'seatNo', 'reservation_no' // 【行】执行本行语句，推进功能链中的当前步骤
  ]))
})
const pagedAdminReservations = computed(() => paginateRows(filteredAdminReservations.value, reservationPage.value, reservationPageSize.value))
const reservationTotalPages = computed(() => pagerTotal(filteredAdminReservations.value.length, reservationPageSize.value))
const decoratedCheckins = computed(() => checkins.value.map(r => ({ ...decorateCheckinRow(r), _rawResult: r.result })))
const filteredCheckins = computed(() => {
  let rows = decoratedCheckins.value
  if (checkinResultFilter.value) rows = rows.filter(r => r._rawResult === checkinResultFilter.value)
  return rows.filter(r => matchAdminKeyword(r, checkinKeyword.value, ['studentNo', 'studentName', 'roomName', 'seatNo']))
})
const pagedCheckins = computed(() => paginateRows(filteredCheckins.value, checkinPage.value, checkinPageSize.value))
const checkinTotalPages = computed(() => pagerTotal(filteredCheckins.value.length, checkinPageSize.value))
const pagedLiveReservations = computed(() => paginateRows(decoratedLiveReservations.value, liveReservationPage.value, liveReservationPageSize.value))
const liveReservationTotalPages = computed(() => pagerTotal(decoratedLiveReservations.value.length, liveReservationPageSize.value))
const filteredAnnouncements = computed(() => sortedAnnouncements.value.filter(a =>
  matchAdminKeyword(a, announcementKeyword.value, ['title', 'content'])
))
const pagedAnnouncements = computed(() => paginateRows(filteredAnnouncements.value, announcementPage.value, announcementPageSize.value))
const announcementTotalPages = computed(() => pagerTotal(filteredAnnouncements.value.length, announcementPageSize.value))
const decoratedAdminFeedback = computed(() => adminFeedback.value.map(row => {
  const d = decorateFeedbackRow(row)
  return { ...d, _rawStatus: row.status }
}))
const filteredAdminFeedback = computed(() => {
  let rows = decoratedAdminFeedback.value
  if (feedbackStatusFilter.value) rows = rows.filter(r => feedbackStatusValue(r._rawStatus) === feedbackStatusFilter.value)
  return rows.filter(r => matchAdminKeyword(r, feedbackKeyword.value, ['studentName', 'studentNo', 'type', 'content', 'roomName']))
})
const pagedAdminFeedback = computed(() => paginateRows(filteredAdminFeedback.value, feedbackPage.value, feedbackPageSize.value))
const feedbackTotalPages = computed(() => pagerTotal(filteredAdminFeedback.value.length, feedbackPageSize.value))
const filteredOperationLogs = computed(() => {
  let rows = operationLogs.value
  if (logModuleFilter.value) rows = rows.filter(r => String(r.module || '') === logModuleFilter.value)
  return rows.filter(r => matchAdminKeyword(r, logKeyword.value, ['module', 'action', 'target_type', 'detail', 'operator_name']))
})
const pagedOperationLogs = computed(() => paginateRows(filteredOperationLogs.value, logPage.value, logPageSize.value))
const logTotalPages = computed(() => pagerTotal(filteredOperationLogs.value.length, logPageSize.value))
const adminStatSummary = computed(() => {
  const s = adminStatsReport.value.summary || {}
  return {
    totalReserve: s.totalReserve || 0,
    usingCount: s.usingCount || 0,
    checkinRate: s.checkinRate || 0,
    avgCredit: s.avgCredit || 0
  }
})
const adminStatsScopeLabel = computed(() => {
  if (!adminStatsRoomId.value) return '全部自习室'
  const room = rooms.value.find(r => Number(r.id) === Number(adminStatsRoomId.value))
  return room?.name || '指定自习室'
})
const reservationDurationText = computed(() => {
  if (!reservationForm.startTime || !reservationForm.endTime) return ''
  const mins = timeToMinutes(reservationForm.endTime) - timeToMinutes(reservationForm.startTime)
  const h = Math.floor(mins / 60)
  const m = mins % 60
  return h ? `${h} 小时${m ? ` ${m} 分钟` : ''}` : `${m} 分钟`
})

function notify(message) {
  toast.value = message
  setTimeout(() => { toast.value = '' }, 2200)
}
function assetUrl(path) {
  if (!path) return ''
  if (String(path).startsWith('http')) return path
  return String(path).startsWith('/') ? path : `/${path}`
}
function isImageMaterial(url) {
  return /\.(jpg|jpeg|png|gif|webp|bmp)(\?.*)?$/i.test(String(url || ''))
}
function isPdfMaterial(url) {
  return /\.pdf(\?.*)?$/i.test(String(url || ''))
}
function openResourcePreview(path, title = '材料预览') {
  const url = assetUrl(path)
  if (!url) {
    notify('暂无可预览的文件')
    return
  }
  resourcePreview.url = url
  resourcePreview.title = title
  resourcePreview.kind = isImageMaterial(url) ? 'image' : (isPdfMaterial(url) ? 'pdf' : 'file')
  resourcePreview.open = true
}
function closeResourcePreview() {
  resourcePreview.open = false
  resourcePreview.url = ''
  resourcePreview.title = ''
  resourcePreview.kind = 'file'
}
function statCount(row) {
  return Number(row?.cnt ?? row?.count ?? 0)
}
/** ECharts 坐标轴：次数类指标 */
function countYAxis(name = '预约次数（次）') {
  return {
    type: 'value',
    name,
    nameTextStyle: { fontSize: 12, color: '#667085' },
    axisLabel: { formatter: (v) => `${v} 次` }
  }
}
/** ECharts 坐标轴：百分比类指标 */
function percentYAxis(name = '使用率（%）') {
  return {
    type: 'value',
    name,
    nameTextStyle: { fontSize: 12, color: '#667085' },
    axisLabel: { formatter: (v) => `${v}%` }
  }
}
/** ECharts 坐标轴：学习时长（小时） */
function hourYAxis(name = '学习时长（小时）') {
  return {
    type: 'value',
    name,
    nameTextStyle: { fontSize: 12, color: '#667085' },
    axisLabel: { formatter: (v) => `${v} h` }
  }
}
function countTooltip() {
  return { trigger: 'axis', valueFormatter: (v) => `${v} 次` }
}
function hourTooltip() {
  return { trigger: 'axis', valueFormatter: (v) => `${v} 小时` }
}
function trendXAxisName() {
  const period = adminStatsPeriod.value
  const past = adminStatsRangeMode.value === 'past'
  if (period === 'year') return past ? '年份' : '月份'
  if (period === 'month') return past ? '月份' : '日期'
  if (period === 'week') return past ? '周次' : '日期'
  return past ? '日期' : '时段'
}
function trendAxisLabel(row) {
  if (row?.peakHour != null && row.peakHour !== '') {
    return `${String(row.peakHour).padStart(2, '0')}:00`
  }
  if (row?.yearNum != null && row.yearNum !== '') {
    return `${row.yearNum}年`
  }
  if (row?.monthNum != null && row.monthNum !== '') {
    return `${row.monthNum}月`
  }
  const label = row?.timeLabel ?? row?.label ?? ''
  if (/^\d{4}-\d{2}$/.test(label)) return label
  if (/^\d{4}-\d{2}-\d{2}$/.test(label)) return label.slice(5)
  if (/^\d{4}-\d{2}$/.test(String(label).slice(0, 7))) return String(label).slice(0, 7)
  return label
}
function peakAxisLabel(row) {
  const h = row?.peakHour ?? row?.hour
  return h != null && h !== '' ? `${h}时` : ''
}
function isQuickSlotExpired(slot) {
  if (reservationForm.date !== todayDateValue.value) return false
  const cutoff = Date.now() - RESERVATION_PAST_GRACE_MINUTES * 60 * 1000
  const [h, m] = slot.start.split(':').map(Number)
  const slotStart = new Date()
  slotStart.setHours(h, m, 0, 0)
  return slotStart.getTime() < cutoff
}
function clampReservationStartForToday() {
  if (reservationForm.date !== todayDateValue.value) {
    normalizeReservationTimes()
    return
  }
  if (timeToMinutes(reservationForm.startTime) < timeToMinutes(minStartTimeToday.value)) {
    reservationForm.startTime = minStartTimeToday.value
    if (timeToMinutes(reservationForm.endTime) <= timeToMinutes(reservationForm.startTime)) {
      reservationForm.endTime = addMinutes(reservationForm.startTime, 120)
    }
  }
  normalizeReservationTimes()
}
function ensureReservationTimeAllowed() {
  if (timeToMinutes(reservationForm.startTime) < timeToMinutes(currentRoomOpenTime.value)) {
    throw new Error(`开始时间不能早于自习室开放时间 ${currentRoomOpenTime.value}`)
  }
  if (timeToMinutes(reservationForm.endTime) > timeToMinutes(currentRoomCloseTime.value)) {
    throw new Error(`结束时间不能晚于自习室关闭时间 ${currentRoomCloseTime.value}`)
  }
  if (reservationForm.date !== todayDateValue.value) return
  const cutoff = Date.now() - RESERVATION_PAST_GRACE_MINUTES * 60 * 1000
  const [h, m] = reservationForm.startTime.split(':').map(Number)
  const start = new Date()
  start.setHours(h, m, 0, 0)
  if (start.getTime() < cutoff) {
    throw new Error('不能预约已开始超过15分钟的时段，请选择更晚的开始时间')
  }
}
function roomStatusText(status) {
  return roomStatusValue(status) || '-'
}
function stopCheckinPagePoll() {
  if (checkinPollTimer) {
    clearInterval(checkinPollTimer)
    checkinPollTimer = null
  }
}
/** 签到页轮询：管理员按学号签到后自动切到「使用中」 */
async function syncCheckinStateFromServer() {
  if (studentPage.value !== 'checkin') return
  const tracked = activeReservation.value
  if (!tracked?.id) return
  const prevId = tracked.id
  const prevStatus = tracked.status
  try {
    await loadReservations()
    const updated = reservations.value.find(r => Number(r.id) === Number(prevId))
    if (!updated) return
    if (isPendingReservation(prevStatus) && isUsingReservation(updated.status)) {
      updateStudyTimer()
      notify('签到成功，已进入学习状态')
    }
    if (isUsingReservation(prevStatus) && isPendingReservation(updated.status)) {
      notify('签到无效，已恢复为待签到')
    }
  } catch { /* 轮询失败忽略 */ }
}
function startCheckinPagePoll() {
  stopCheckinPagePoll()
  syncCheckinStateFromServer()
  checkinPollTimer = setInterval(syncCheckinStateFromServer, 2000)
}
function forgetPassword() {
  notify('请联系管理员重置密码，或通过注册邮箱找回')
}
function parseRoomFacilities(room) {
  const raw = room?.facilities
  if (Array.isArray(raw)) return raw
  if (!raw) return []
  return String(raw).split(',').map(x => x.trim()).filter(Boolean)
}
function seatCellClass(seat) {
  if (seat?.placeholder) return 'placeholder'
  if (!seat?.is_seat) return 'nonseat'
  if (seat.has_power) return 'power'
  return ''
}
function seatCellTags(seat) {
  const tags = []
  if (seat?.seat_type) tags.push(seat.seat_type)
  if (seat?.has_power) tags.push('电源')
  if (seat?.near_window) tags.push('靠窗')
  if (seat?.quiet_zone) tags.push('静音')
  if (seat?.hot_seat) tags.push('热门')
  if (!seat?.is_seat) tags.push('非座位')
  return tags.length ? tags : ['普通']
}
function openRoomFormCreate() {
  editRoom()
}
function closeRoomForm() {
  roomFormOpen.value = false
  adminSeats.value = []
  seatKeyword.value = ''
  seatStatusFilter.value = ''
}
function openSeatEdit(seat) {
  if (!seat?.id) {
    notify('该格子暂无座位数据，请先在「自习室管理」保存行列数以同步网格')
    return
  }
  Object.assign(seatEditForm, {
    id: seat.id,
    seat_no: seat.seat_no,
    is_seat: !!seat.is_seat,
    has_power: !!seat.has_power,
    near_window: !!seat.near_window,
    quiet_zone: !!seat.quiet_zone,
    hot_seat: !!seat.hot_seat,
    status: seatStatusValue(seat.status) || '空闲',
    cell_category: seat.cell_category || (seat.is_seat ? '座位' : '非座位'),
    seat_type: seat.seat_type || '普通'
  })
  seatEditOpen.value = true
}
/** 【F6-4·自习室与座位】功能链实例：superadmin 新增 B 自习室并保存 → 同步 4×6 座位网格 → 在布局图里改 A-12 为「靠窗」。 本处职责：布局图点座位 PUT /admin/seats/{id} 改靠窗/电源等*/
async function saveSeatEdit() { // 【行】进入代码块
  try { // 【行】进入代码块
    await call('put', `/admin/seats/${seatEditForm.id}`, { // 【行】带 JWT 调用后端 REST API
      isSeat: seatEditForm.is_seat ? 1 : 0, // 【行】执行本行语句，推进功能链中的当前步骤
      hasPower: seatEditForm.has_power ? 1 : 0, // 【行】执行本行语句，推进功能链中的当前步骤
      nearWindow: seatEditForm.near_window ? 1 : 0, // 【行】执行本行语句，推进功能链中的当前步骤
      quietZone: seatEditForm.quiet_zone ? 1 : 0, // 【行】执行本行语句，推进功能链中的当前步骤
      hotSeat: seatEditForm.hot_seat ? 1 : 0, // 【行】执行本行语句，推进功能链中的当前步骤
      status: seatStatusValue(seatEditForm.status) || '空闲', // 【行】执行本行语句，推进功能链中的当前步骤
      cellCategory: seatEditForm.cell_category || (seatEditForm.is_seat ? '座位' : '非座位'), // 【行】执行本行语句，推进功能链中的当前步骤
      seatType: seatEditForm.seat_type || '普通' // 【行】执行本行语句，推进功能链中的当前步骤
    }) // 【行】执行本行语句，推进功能链中的当前步骤
    seatEditOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    notify('座位配置已保存') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadAdminSeats() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
async function saveProfileAndClose() { // 【行】进入代码块
  await saveProfile() // 【行】执行本行语句，推进功能链中的当前步骤
  profileInfoOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
}
async function submitFeedbackModal() { // 【行】进入代码块
  if (!feedbackForm.content.trim()) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请输入反馈内容') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  try { // 【行】进入代码块
    await call('post', '/feedback', { // 【行】带 JWT 调用后端 REST API
      content: feedbackForm.content, // 【行】执行本行语句，推进功能链中的当前步骤
      type: feedbackForm.type, // 【行】执行本行语句，推进功能链中的当前步骤
      severity: feedbackForm.severity, // 【行】执行本行语句，推进功能链中的当前步骤
      roomId: reservationForm.roomId, // 【行】执行本行语句，推进功能链中的当前步骤
      seatId: selectedSeat.value?.id || activeReservation.value?.seatId // 【行】执行本行语句，推进功能链中的当前步骤
    }) // 【行】执行本行语句，推进功能链中的当前步骤
    feedbackModalOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    feedbackForm.content = '' // 【行】执行本行语句，推进功能链中的当前步骤
    notify('反馈已提交') // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
function runGenericConfirm() { // 【行】进入代码块
  if (typeof genericModal.onConfirm === 'function') genericModal.onConfirm() // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  genericModal.open = false // 【行】执行本行语句，推进功能链中的当前步骤
}
async function changeAdminStatsPeriod(period) { // 【行】进入代码块
  adminStatsPeriod.value = period // 【行】执行本行语句，推进功能链中的当前步骤
  await loadAdminStatistics() // 【行】执行本行语句，推进功能链中的当前步骤
}
async function changeAdminStatsRangeMode(mode) { // 【行】进入代码块
  adminStatsRangeMode.value = mode // 【行】执行本行语句，推进功能链中的当前步骤
  if (mode !== 'past') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    adminStatsDateRange.value = null // 【行】执行本行语句，推进功能链中的当前步骤
    adminStatsRangeTouched.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  }
  await loadAdminStatistics() // 【行】执行本行语句，推进功能链中的当前步骤
}
function onAdminStatsDateRangeChange() { // 【行】进入代码块
  adminStatsRangeTouched.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  loadAdminStatistics() // 【行】执行本行语句，推进功能链中的当前步骤
}
function resetAdminStatsDateRange() { // 【行】进入代码块
  adminStatsDateRange.value = null // 【行】执行本行语句，推进功能链中的当前步骤
  adminStatsRangeTouched.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  loadAdminStatistics() // 【行】执行本行语句，推进功能链中的当前步骤
}
function buildAdminStatsParams() { // 【行】进入代码块
  const params = { period: adminStatsPeriod.value, rangeMode: adminStatsRangeMode.value } // 【行】初始化 GET 查询参数字典，键名与后端约定一致
  if (adminStatsRoomId.value) params.roomId = adminStatsRoomId.value // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (adminStatsRangeMode.value === 'past' && adminStatsDateRange.value?.length === 2) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    params.startDate = adminStatsDateRange.value[0] // 【行】往期模式下附加自定义开始日期 query
    params.endDate = adminStatsDateRange.value[1] // 【行】往期模式下附加自定义结束日期 query
  }
  return params // 【行】返回参数字典，供 axios call() 拼接到 URL
}
function syncAdminStatsDateRangeFromSummary(summary = {}) { // 【行】进入代码块
  if (adminStatsRangeMode.value !== 'past' || adminStatsRangeTouched.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (summary.startDate && summary.endDate) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    adminStatsDateRange.value = [summary.startDate, summary.endDate] // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：buildStudyStatsParams 将 period、rangeMode、起止日期 ref 组装为 GET 查询参数 */
function buildStudyStatsParams() { // 【行】进入代码块
  const params = { period: statPeriod.value, rangeMode: studyStatsRangeMode.value } // 【行】初始化 GET 查询参数字典，键名与后端约定一致
  if (studyStatsRangeMode.value === 'past' && studyStatsStartDate.value && studyStatsEndDate.value) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    params.startDate = studyStatsStartDate.value // 【行】读写往期统计的开始日期 ref
    params.endDate = studyStatsEndDate.value // 【行】读写往期统计的结束日期 ref
  }
  return params // 【行】返回参数字典，供 axios call() 拼接到 URL
}
function syncStudyStatsDateRangeFromSummary(summary = {}) { // 【行】API 返回 summary 时回写起止日期（仅往期且用户未手动改过）
  if (studyStatsRangeMode.value !== 'past' || studyStatsRangeTouched.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (summary.startDate && summary.endDate) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    studyStatsStartDate.value = summary.startDate // 【行】读写往期统计的开始日期 ref
    studyStatsEndDate.value = summary.endDate // 【行】读写往期统计的结束日期 ref
  }
}
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：applyStudyStatsShortcut 与起止日期 change 写入 ref 并触发 loadStudyStats */
function normalizeStudyStatsDateRange() { // 【行】保证开始日期不晚于结束日期
  if (!studyStatsStartDate.value || !studyStatsEndDate.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (studyStatsStartDate.value > studyStatsEndDate.value) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    const tmp = studyStatsStartDate.value // 【行】读写往期统计的开始日期 ref
    studyStatsStartDate.value = studyStatsEndDate.value // 【行】读写往期统计的开始日期 ref
    studyStatsEndDate.value = tmp // 【行】读写往期统计的结束日期 ref
  }
}
function onStudyStatsStartDateChange() { // 【行】开始日期变更：纠正逆序后标记 touched 并重新拉数
  normalizeStudyStatsDateRange() // 【行】保证开始日期不晚于结束日期
  studyStatsRangeTouched.value = true // 【行】标记用户已手动改过日期，禁止被 API 回写覆盖
  loadStudyStats().then(drawStudentChart) // 【行】拉数完成后刷新柱图展示
}
function onStudyStatsEndDateChange() { // 【行】结束日期变更：纠正逆序后标记 touched 并重新拉数
  normalizeStudyStatsDateRange() // 【行】保证开始日期不晚于结束日期
  studyStatsRangeTouched.value = true // 【行】标记用户已手动改过日期，禁止被 API 回写覆盖
  loadStudyStats().then(drawStudentChart) // 【行】拉数完成后刷新柱图展示
}
function applyStudyStatsShortcut(shortcut) { // 【行】快捷区间按钮：写入起止 ref 并 loadStudyStats
  const range = shortcut.value() // 【行】从快捷按钮配置函数取出 [起,止] 日期数组
  studyStatsStartDate.value = range[0] // 【行】读写往期统计的开始日期 ref
  studyStatsEndDate.value = range[1] // 【行】读写往期统计的结束日期 ref
  studyStatsRangeTouched.value = true // 【行】标记用户已手动改过日期，禁止被 API 回写覆盖
  loadStudyStats().then(drawStudentChart) // 【行】拉数完成后刷新柱图展示
}
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：changeStudyStatsRangeMode 切换当期/往期 Tab 并重拉统计 */
async function changeStudyStatsRangeMode(mode) { // 【行】进入代码块
  studyStatsRangeMode.value = mode // 【行】更新当期/往期 Tab 对应的 rangeMode 状态
  if (mode !== 'past') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    studyStatsStartDate.value = null // 【行】读写往期统计的开始日期 ref
    studyStatsEndDate.value = null // 【行】读写往期统计的结束日期 ref
    studyStatsRangeTouched.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  }
  await loadStudyStats() // 【行】异步拉取学习统计数据并写入 studyStats ref
  drawStudentChart() // 【行】根据最新 studyBars 重绘 ECharts 柱图
}
function resetStudyStatsDateRange() { // 【行】清空往期起止日期并恢复默认统计窗
  studyStatsStartDate.value = null // 【行】读写往期统计的开始日期 ref
  studyStatsEndDate.value = null // 【行】读写往期统计的结束日期 ref
  studyStatsRangeTouched.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  loadStudyStats().then(drawStudentChart) // 【行】拉数完成后刷新柱图展示
}
/** 【F6-6·运营看板】功能链实例：管理员打开签到页 → 底部实时列表显示「待签到 / 使用中」预约；学生签到页轮询同步状态。 本处职责：管理员签到页底部展示待签到/使用中实时列表*/
async function loadLiveReservations() { // 【行】进入代码块
  try { // 【行】进入代码块
    liveReservations.value = await call('get', '/admin/live-reservations') // 【行】带 JWT 调用后端 REST API
  } catch (e) { // 【行】进入代码块
    liveReservations.value = [] // 【行】执行本行语句，推进功能链中的当前步骤
    notify(e.message) // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
function toDateValue(date) { // 【行】进入代码块
  const y = date.getFullYear() // 【行】声明并赋值变量 `y`
  const m = String(date.getMonth() + 1).padStart(2, '0') // 【行】声明并赋值变量 `m`
  const d = String(date.getDate()).padStart(2, '0') // 【行】声明并赋值变量 `d`
  return `${y}-${m}-${d}` // 【行】返回本函数计算结果给调用方
}
function formatDate(value) { // 【行】进入代码块
  if (!value) return '' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  return String(value).slice(0, 10) // 【行】返回本函数计算结果给调用方
}
function formatStudyLabel(value) { // 【行】进入代码块
  const text = String(value || '') // 【行】声明并赋值变量 `text`
  if (statPeriod.value === 'day' && studyStatsRangeMode.value !== 'past') return `${String(text).padStart(2, '0')}时` // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (statPeriod.value === 'year' || (statPeriod.value === 'month' && studyStatsRangeMode.value === 'past')) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    const match = text.match(/^(\d{4})-(\d{2})$/) // 【行】声明并赋值变量 `match`
    return match ? `${match[2]}月` : text // 【行】返回本函数计算结果给调用方
  }
  if (statPeriod.value === 'week' && studyStatsRangeMode.value === 'past') { // 【行】分支判断：针对往期周报格式化为 xx周
    const match = text.match(/^(\d{4})-(\d{2})$/) // 【行】声明并赋值变量 `match`
    return match ? `${match[2]}周` : text // 【行】返回本函数计算结果给调用方
  }
  return text.length >= 10 ? text.slice(5, 10).replace('-', '/') : text // 【行】返回本函数计算结果给调用方
}
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：buildYearStudyBars 按统计窗口补全无数据的月份为 0 */
function buildYearStudyBars(rows) { // 【行】进入代码块
  const map = new Map((rows || []).map(row => [String(row.label), Number(row.minutes || 0)])) // 【行】声明并赋值变量 `map`
  const bars = [] // 【行】声明并赋值变量 `bars`
  let start // 【行】执行本行语句，推进功能链中的当前步骤
  let end // 【行】执行本行语句，推进功能链中的当前步骤
  if (studyStats.value.startDate && studyStats.value.endDate) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    start = new Date(`${studyStats.value.startDate}T00:00:00`) // 【行】执行本行语句，推进功能链中的当前步骤
    end = new Date(`${studyStats.value.endDate}T00:00:00`) // 【行】执行本行语句，推进功能链中的当前步骤
  } else if (statPeriod.value === 'month' && studyStatsRangeMode.value === 'past') { // 【行】进入代码块
    const now = new Date() // 【行】声明并赋值变量 `now`
    end = new Date(now.getFullYear(), now.getMonth() - 1, 1) // 【行】执行本行语句，推进功能链中的当前步骤
    start = new Date(end.getFullYear(), end.getMonth() - 11, 1) // 【行】执行本行语句，推进功能链中的当前步骤
  } else if (studyStatsRangeMode.value === 'past') { // 【行】进入代码块
    const y = new Date().getFullYear() - 1 // 【行】声明并赋值变量 `y`
    start = new Date(y, 0, 1) // 【行】执行本行语句，推进功能链中的当前步骤
    end = new Date(y, 11, 1) // 【行】执行本行语句，推进功能链中的当前步骤
  } else { // 【行】进入代码块
    const now = new Date() // 【行】声明并赋值变量 `now`
    start = new Date(now.getFullYear(), 0, 1) // 【行】执行本行语句，推进功能链中的当前步骤
    end = new Date(now.getFullYear(), now.getMonth(), 1) // 【行】执行本行语句，推进功能链中的当前步骤
  }
  const cursor = new Date(start.getFullYear(), start.getMonth(), 1) // 【行】声明并赋值变量 `cursor`
  const endMonth = new Date(end.getFullYear(), end.getMonth(), 1) // 【行】声明并赋值变量 `endMonth`
  while (cursor <= endMonth) { // 【行】进入代码块
    const key = `${cursor.getFullYear()}-${String(cursor.getMonth() + 1).padStart(2, '0')}` // 【行】声明并赋值变量 `key`
    bars.push({ // 【行】进入代码块
      label: `${String(cursor.getMonth() + 1).padStart(2, '0')}月`, // 【行】执行本行语句，推进功能链中的当前步骤
      value: Number(((map.get(key) || 0) / 60).toFixed(1)) // 【行】执行本行语句，推进功能链中的当前步骤
    }) // 【行】执行本行语句，推进功能链中的当前步骤
    cursor.setMonth(cursor.getMonth() + 1) // 【行】执行本行语句，推进功能链中的当前步骤
  }
  return bars // 【行】返回本函数计算结果给调用方
}
function barHeight(value) { // 【行】进入代码块
  if (!Number(value)) return 4 // 【行】条件不满足时提前结束，避免无效请求或错误状态
  return Math.max(8, Math.round((Number(value) / maxStudyBarValue.value) * 100)) // 【行】返回本函数计算结果给调用方
}
function timeRangeText(item) { // 【行】进入代码块
  return `${String(item.start_time || item.startTime || '').slice(0, 5)}-${String(item.end_time || item.endTime || '').slice(0, 5)}` // 【行】返回本函数计算结果给调用方
}
function timeToMinutes(value) { // 【行】进入代码块
  const [h, m] = String(value || '00:00').split(':').map(Number) // 【行】声明并赋值变量 ``
  return h * 60 + m // 【行】返回本函数计算结果给调用方
}
function minutesToTime(minutes) { // 【行】进入代码块
  const safe = Math.max(0, Math.min(23 * 60 + 59, minutes)) // 【行】声明并赋值变量 `safe`
  return `${String(Math.floor(safe / 60)).padStart(2, '0')}:${String(safe % 60).padStart(2, '0')}` // 【行】返回本函数计算结果给调用方
}
function addMinutes(value, minutes) { // 【行】进入代码块
  return minutesToTime(timeToMinutes(value) + minutes) // 【行】返回本函数计算结果给调用方
}
function ensureEndAfterStart() { // 【行】进入代码块
  if (!reservationForm.startTime) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (!reservationForm.endTime || timeToMinutes(reservationForm.endTime) <= timeToMinutes(reservationForm.startTime)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    reservationForm.endTime = endSelectStart.value // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (timeToMinutes(reservationForm.endTime) > timeToMinutes(currentRoomCloseTime.value)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    reservationForm.endTime = currentRoomCloseTime.value // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
function formatStudyTime(sec) { // 【行】进入代码块
  const h = String(Math.floor(sec / 3600)).padStart(2, '0') // 【行】声明并赋值变量 `h`
  const m = String(Math.floor((sec % 3600) / 60)).padStart(2, '0') // 【行】声明并赋值变量 `m`
  const s = String(sec % 60).padStart(2, '0') // 【行】声明并赋值变量 `s`
  return `${h}:${m}:${s}` // 【行】返回本函数计算结果给调用方
}
function updateStudyTimer() { // 【行】进入代码块
  const r = activeReservation.value // 【行】声明并赋值变量 `r`
  if (!r || !isUsingReservation(r.status) || !r.sign_in_time) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    studySeconds.value = 0 // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  const start = new Date(String(r.sign_in_time).replace(' ', 'T')) // 【行】声明并赋值变量 `start`
  studySeconds.value = Math.max(0, Math.floor((Date.now() - start.getTime()) / 1000)) // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 学生端分区：仅保留热门/静音/开放座位，静音单独成区，不再使用精品区、标准区或复合标签 */
function resolveSeatSection(seat) { // 【行】进入代码块
  if (!seat.is_seat) return '非座位区' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (seat.quiet_zone) return '静音区' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (seat.hot_seat) return '热门区' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  return '开放座位' // 【行】返回本函数计算结果给调用方
}
function buildReservationTimeOptions(rangeStart, rangeEnd, stepMin = 10) { // 【行】进入代码块
  const options = [] // 【行】声明并赋值变量 `options`
  let cur = timeToMinutes(rangeStart) // 【行】声明并赋值变量 `cur`
  const max = timeToMinutes(rangeEnd) // 【行】声明并赋值变量 `max`
  while (cur <= max) { // 【行】进入代码块
    options.push(minutesToTime(cur)) // 【行】执行本行语句，推进功能链中的当前步骤
    cur += stepMin // 【行】执行本行语句，推进功能链中的当前步骤
  }
  return options // 【行】返回本函数计算结果给调用方
}
function normalizeReservationTimes() { // 【行】进入代码块
  const starts = startTimeOptions.value // 【行】声明并赋值变量 `starts`
  if (starts.length && !starts.includes(reservationForm.startTime)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    reservationForm.startTime = starts[0] // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!reservationForm.endTime || timeToMinutes(reservationForm.endTime) <= timeToMinutes(reservationForm.startTime)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    reservationForm.endTime = endSelectStart.value // 【行】执行本行语句，推进功能链中的当前步骤
  }
  const ends = endTimeOptions.value // 【行】声明并赋值变量 `ends`
  if (ends.length && !ends.includes(reservationForm.endTime)) {
    reservationForm.endTime = ends.includes(endSelectStart.value) ? endSelectStart.value : ends[0]
  }
}
function matchesSeatFilter(seat) {
  if (seatFilter.value === 'all') return true
  if (seatFilter.value === 'power') return !!seat.has_power
  if (seatFilter.value === 'window') return !!seat.near_window
  if (seatFilter.value === 'quiet') return !!seat.quiet_zone
  if (seatFilter.value === 'hot') return !!seat.hot_seat
  return true
}
function seatVisualClass(seat) {
  const classes = []
  if (selectedSeat.value?.id === seat.id) classes.push('sel')
  else if (!seat.is_seat || !seat.available) classes.push('busy')
  else classes.push('free')
  if (!matchesSeatFilter(seat) && seat.is_seat) classes.push('off')
  return classes
}
function canSelectSeat(seat) {
  return !!seat.is_seat && !!seat.available && matchesSeatFilter(seat)
}
function applyQuickSlot(slot) {
  if (slot.expired || isQuickSlotExpired(slot)) {
    notify('该时段已开始超过15分钟，无法预约')
    return
  }
  reservationForm.startTime = slot.start
  reservationForm.endTime = slot.end
  loadAvailableSeats()
}
function isQuickSlotActive(slot) {
  return reservationForm.startTime === slot.start && reservationForm.endTime === slot.end
}
function openConfirmReservation() {
  if (!selectedSeat.value) return
  confirmReservationOpen.value = true
}
function toggleNotifyPref(key) {
  notifyPrefs[key] = !notifyPrefs[key]
  localStorage.setItem('notifyPrefs', JSON.stringify(notifyPrefs))
}
function goBackStudent() {
  const profilePages = ['myres', 'credit', 'stats', 'settings', 'feedback', 'notifications']
  studentPage.value = profilePages.includes(studentPage.value) && studentPage.value !== 'notifications' ? 'profile' : 'home'
}
function selectSeatDirect(seat) {
  if (!canSelectSeat(seat)) return
  selectedSeat.value = seat
  confirmReservationOpen.value = true
}
function openFeedbackModal() {
  feedbackForm.content = ''
  feedbackForm.type = '建议'
  feedbackForm.severity = '中'
  feedbackModalOpen.value = true
}
function openProfileInfo() {
  syncProfileForm()
  profileInfoOpen.value = true
}
function confirmCheckout() {
  // 【F4-2·签退与信用】功能链实例：小明使用中点「签退」→ 确认 → 预约「已完成」→ 信用页看到签到 +5 流水与当前分数。 本处职责：小明点签退，弹窗确认后调用 doCheckout
  if (!activeReservation.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  openModalConfirm('确认签退', '签退后将结束本次学习并释放座位，确定签退吗？', doCheckout) // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F4-2·签退与信用】功能链实例：小明使用中点「签退」→ 确认 → 预约「已完成」→ 信用页看到签到 +5 流水与当前分数。 本处职责：POST /reservations/{id}/checkout，展示学习分钟数*/
async function doCheckout() { // 【行】进入代码块
  try { // 【行】进入代码块
    const data = await call('post', `/reservations/${activeReservation.value.id}/checkout`) // 【行】带 JWT 调用后端 REST API
    checkoutSummary.value = { // 【行】进入代码块
      roomName: activeReservation.value.roomName, // 【行】执行本行语句，推进功能链中的当前步骤
      seatNo: activeReservation.value.seatNo, // 【行】执行本行语句，推进功能链中的当前步骤
      minutes: data.actualMinutes || studySeconds.value / 60, // 【行】执行本行语句，推进功能链中的当前步骤
      creditChange: '+5' // 【行】执行本行语句，推进功能链中的当前步骤
    }
    checkoutModalOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
    await loadReservations() // 【行】执行本行语句，推进功能链中的当前步骤
    await loadCredit() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
function openModalConfirm(title, message, onOk) { // 【行】进入代码块
  genericModal.title = title // 【行】执行本行语句，推进功能链中的当前步骤
  genericModal.message = message // 【行】执行本行语句，推进功能链中的当前步骤
  genericModal.onConfirm = onOk // 【行】执行本行语句，推进功能链中的当前步骤
  genericModal.open = true // 【行】执行本行语句，推进功能链中的当前步骤
}
function clearSession(message) { // 【行】进入代码块
  token.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
  role.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
  me.value = {}
  studentPage.value = 'home' // 【行】执行本行语句，推进功能链中的当前步骤
  adminPage.value = 'checkins' // 【行】执行本行语句，推进功能链中的当前步骤
  loginRole.value = 'student' // 【行】执行本行语句，推进功能链中的当前步骤
  localStorage.removeItem('token') // 【行】执行本行语句，推进功能链中的当前步骤
  localStorage.removeItem('role') // 【行】执行本行语句，推进功能链中的当前步骤
  if (message) notify(message) // 【行】分支判断：根据当前 UI 状态决定后续逻辑
}
function openRegister() { // 【行】进入代码块
  registerPassword2.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
  registerOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F2-3·注册审核】功能链实例：小李注册并上传 PDF 材料 → 尝试登录得「注册资料待审核」→ 管理员在用户管理点「通过」→ 小李再登录进入首页。 本处职责：小李注册前上传身份材料到 uploads/material*/
async function onRegisterFile(event) { // 【行】进入代码块
  const file = event.target.files?.[0] // 【行】声明并赋值变量 `file`
  if (!file) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    registerForm.materialUrl = '' // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  try { // 【行】进入代码块
    const form = new FormData() // 【行】声明并赋值变量 `form`
    form.append('file', file) // 【行】执行本行语句，推进功能链中的当前步骤
    const res = await api.post('/auth/register/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } }) // 【行】声明并赋值变量 `res`
    registerForm.materialUrl = res.data.data.url // 【行】执行本行语句，推进功能链中的当前步骤
    notify('身份材料上传成功') // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { // 【行】进入代码块
    notify(e.message || '材料上传失败') // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F1-2·技术概念】功能链实例：小明点「确认预约」→ 浏览器用 **Vue** 发 **HTTP** **JSON** 到 **REST API** → **Controller** 转 **Service** 写 **MySQL** → 返回 **JSON** `… 本处职责：小明点确认预约时，call 发 POST /api/reservations，body 为 JSON*/
async function call(method, url, data, config) { // 【行】进入代码块
  const res = await api.request({ method, url, data, ...config }) // 【行】声明并赋值变量 `res`
  return res.data.data // 【行】返回本函数计算结果给调用方
}
/** 【F2-1·学生登录】功能链实例：小明在登录页输入 `202225220101` / `123456` → 点「登录」→ 首页显示「你好，小明」→ 再进「我的预约」无需重输密码（`localStorage` 已有 token）。 本处职责：小明 POST /auth/login，保存 token 进 localStorage*/
async function loginStudent() { // 【行】进入代码块
  if (authLoading.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (!studentLogin.username.trim() || !studentLogin.password) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请输入学号和密码') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  authLoading.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  try { // 【行】进入代码块
    const data = await call('post', '/auth/login', studentLogin) // 【行】带 JWT 调用后端 REST API
    afterLogin(data.token, 'STUDENT', data.userInfo) // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { // 【行】进入代码块
    notify(e.message || '登录失败') // 【行】执行本行语句，推进功能链中的当前步骤
  } finally { // 【行】进入代码块
    authLoading.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F2-2·管理员登录】功能链实例：管理员切到「管理员登录」→ 输入 `admin` / `admin123` → 进入管理端签到页；`superadmin` 侧栏额外显示「设置」「管理员管理」。 本处职责：admin POST /admin/auth/login*/
async function loginAdmin() { // 【行】进入代码块
  if (authLoading.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (!adminLogin.account.trim() || !adminLogin.password) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请输入管理员账号和密码') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  authLoading.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  try { // 【行】进入代码块
    const data = await call('post', '/admin/auth/login', adminLogin) // 【行】带 JWT 调用后端 REST API
    afterLogin(data.token, data.adminInfo.role === 'SUPER_ADMIN' ? 'SUPER_ADMIN' : 'ADMIN', data.adminInfo) // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { // 【行】进入代码块
    notify(e.message || '登录失败') // 【行】执行本行语句，推进功能链中的当前步骤
  } finally { // 【行】进入代码块
    authLoading.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F2-1·学生登录】功能链实例：小明在登录页输入 `202225220101` / `123456` → 点「登录」→ 首页显示「你好，小明」→ 再进「我的预约」无需重输密码（`localStorage` 已有 token）。 本处职责：登录成功后 token 写入 localStorage，后续请求带 Bearer*/
async function afterLogin(t, r, info) { // 【行】进入代码块
  token.value = t // 【行】执行本行语句，推进功能链中的当前步骤
  role.value = r // 【行】执行本行语句，推进功能链中的当前步骤
  me.value = info || {}
  localStorage.setItem('token', t) // 【行】执行本行语句，推进功能链中的当前步骤
  localStorage.setItem('role', r) // 【行】执行本行语句，推进功能链中的当前步骤
  notify('登录成功') // 【行】执行本行语句，推进功能链中的当前步骤
  await bootstrap(false) // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F2-3·注册审核】功能链实例：小李注册并上传 PDF 材料 → 尝试登录得「注册资料待审核」→ 管理员在用户管理点「通过」→ 小李再登录进入首页。 本处职责：小李提交注册表单 POST /auth/register*/
async function register() { // 【行】进入代码块
  if (authLoading.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (!registerForm.studentNo.trim() || !registerForm.name.trim() || !registerForm.password) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请填写学号、姓名和密码') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!/^\d{12}$/.test(registerForm.studentNo.trim())) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('学号须为 12 位数字') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!/^[\u4e00-\u9fa5]{2,10}$/.test(registerForm.name.trim())) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('姓名须为 2-10 个汉字') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!/^\d{4}$/.test(registerForm.grade)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('年级须为 4 位年份') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!registerForm.phone.trim() || !/^1\d{10}$/.test(registerForm.phone.trim())) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请输入 11 位中国大陆手机号') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!registerForm.email.trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.email.trim())) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('邮箱格式不正确') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!registerForm.materialUrl) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请上传身份材料') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (registerForm.password !== registerPassword2.value) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('两次密码输入不一致') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (registerForm.password.length < 6 || registerForm.password.length > 20) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('密码长度须为 6-20 位') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (!/(?=.*[A-Za-z])(?=.*\d)/.test(registerForm.password)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('密码须同时包含字母和数字') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  authLoading.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  try { // 【行】进入代码块
    await call('post', '/auth/register', { ...registerForm }) // 【行】带 JWT 调用后端 REST API
    registerOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    registerPassword2.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
    notify('注册申请已提交，请等待管理员审核') // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { // 【行】进入代码块
    notify(e.message || '注册失败') // 【行】执行本行语句，推进功能链中的当前步骤
  } finally { // 【行】进入代码块
    authLoading.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
function logout() { // 【行】进入代码块
  clearSession('已退出登录') // 【行】执行本行语句，推进功能链中的当前步骤
}
function switchAdminAccount() { // 【行】进入代码块
  clearSession('') // 【行】执行本行语句，推进功能链中的当前步骤
  loginRole.value = 'admin' // 【行】执行本行语句，推进功能链中的当前步骤
}
/** @param silent 页面刷新时用旧 token 恢复会话：失败则静默清 token，避免登录页弹 SQL 报错 */
/** 【F2-1·学生登录】功能链实例：小明在登录页输入 `202225220101` / `123456` → 点「登录」→ 首页显示「你好，小明」→ 再进「我的预约」无需重输密码（`localStorage` 已有 token）。 本处职责：刷新页面后 bootstrap 用 localStorage token 调 GET /auth/me 恢复小明会话*/
async function bootstrap(silent = true) { // 【行】进入代码块
  if (!token.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    me.value = await call('get', '/auth/me') // 【行】带 JWT 调用后端 REST API
    syncProfileForm() // 【行】执行本行语句，推进功能链中的当前步骤
    await Promise.all([loadRooms(), loadAnnouncements()]) // 【行】执行本行语句，推进功能链中的当前步骤
    if (role.value === 'STUDENT') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      await Promise.all([loadReservations(), loadNotifications(), loadCredit(), loadStudyStats()]) // 【行】执行本行语句，推进功能链中的当前步骤
    } else { // 【行】进入代码块
      await openAdmin('checkins') // 【行】执行本行语句，推进功能链中的当前步骤
    }
  } catch (e) { // 【行】进入代码块
    clearSession('') // 【行】执行本行语句，推进功能链中的当前步骤
    if (!silent) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      notify(e.message || '登录后加载失败，请重试') // 【行】执行本行语句，推进功能链中的当前步骤
    }
  }
}
async function loadRooms() { // 【行】进入代码块
  rooms.value = await call('get', role.value === 'STUDENT' ? '/rooms' : '/admin/rooms') // 【行】带 JWT 调用后端 REST API
  if (!reservationForm.roomId && rooms.value[0]) reservationForm.roomId = rooms.value[0].id // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  await loadAvailableSeats() // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F3-1·查座预约】功能链实例：小明登录 → 预约 Tab → 选明天 **14:00–16:00** → 座位图点绿色 **A-12** → 确认 → 提示成功，状态「待使用」；库中 `reservation` 一行 + 多条 `reservation_slot`… 本处职责：GET /seats/available，刷新绿色可选座位*/
async function loadAvailableSeats() { // 【行】进入代码块
  if (!reservationForm.roomId) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  normalizeReservationTimes() // 【行】执行本行语句，推进功能链中的当前步骤
  ensureEndAfterStart() // 【行】执行本行语句，推进功能链中的当前步骤
  seats.value = await call('get', '/seats/available', null, { params: { roomId: reservationForm.roomId, date: reservationForm.date, startTime: reservationForm.startTime, endTime: reservationForm.endTime } }) // 【行】带 JWT 调用后端 REST API
  selectedSeat.value = null // 【行】执行本行语句，推进功能链中的当前步骤
}
async function handleRoomChange() { // 【行】进入代码块
  normalizeReservationTimes() // 【行】执行本行语句，推进功能链中的当前步骤
  clampReservationStartForToday() // 【行】执行本行语句，推进功能链中的当前步骤
  await loadAvailableSeats() // 【行】执行本行语句，推进功能链中的当前步骤
}
async function setReservationDate(date) { // 【行】进入代码块
  reservationForm.date = date // 【行】执行本行语句，推进功能链中的当前步骤
  clampReservationStartForToday() // 【行】执行本行语句，推进功能链中的当前步骤
  await loadAvailableSeats() // 【行】执行本行语句，推进功能链中的当前步骤
}
function selectRoom(id) { // 【行】进入代码块
  reservationForm.roomId = id // 【行】执行本行语句，推进功能链中的当前步骤
  studentPage.value = 'reservation' // 【行】执行本行语句，推进功能链中的当前步骤
  handleRoomChange() // 【行】执行本行语句，推进功能链中的当前步骤
}
async function handleStartTimeChange() { // 【行】进入代码块
  normalizeReservationTimes() // 【行】执行本行语句，推进功能链中的当前步骤
  ensureEndAfterStart() // 【行】执行本行语句，推进功能链中的当前步骤
  clampReservationStartForToday() // 【行】执行本行语句，推进功能链中的当前步骤
  await loadAvailableSeats() // 【行】执行本行语句，推进功能链中的当前步骤
}
async function handleEndTimeChange() { // 【行】进入代码块
  normalizeReservationTimes() // 【行】执行本行语句，推进功能链中的当前步骤
  if (timeToMinutes(reservationForm.endTime) <= timeToMinutes(reservationForm.startTime)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    reservationForm.endTime = endSelectStart.value // 【行】执行本行语句，推进功能链中的当前步骤
    notify('结束时间必须晚于开始时间') // 【行】执行本行语句，推进功能链中的当前步骤
  }
  await loadAvailableSeats() // 【行】执行本行语句，推进功能链中的当前步骤
}
function openSeatDetail(seat) { // 【行】进入代码块
  pendingSeat.value = seat // 【行】执行本行语句，推进功能链中的当前步骤
  seatDialogOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
function confirmSeatSelection() { // 【行】进入代码块
  if (!pendingSeat.value?.available) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  selectedSeat.value = pendingSeat.value // 【行】执行本行语句，推进功能链中的当前步骤
  seatDialogOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  confirmReservationOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
function seatUnavailableText(seat) { // 【行】进入代码块
  if (!seat?.is_seat || seat?.reserveState === 'disabled' || seatStatusValue(seat?.status) !== '空闲') return '不可预约' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (seat?.reserveState === 'reserved') return '当前时段已被预约' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  return '不可预约' // 【行】返回本函数计算结果给调用方
}
/** 【F3-1·查座预约】功能链实例：小明登录 → 预约 Tab → 选明天 **14:00–16:00** → 座位图点绿色 **A-12** → 确认 → 提示成功，状态「待使用」；库中 `reservation` 一行 + 多条 `reservation_slot`… 本处职责：小明确认 A-12，POST /reservations 后跳转签到页*/
async function createReservation() { // 【行】进入代码块
  try { // 【行】进入代码块
    ensureEndAfterStart() // 【行】执行本行语句，推进功能链中的当前步骤
    ensureReservationTimeAllowed() // 【行】执行本行语句，推进功能链中的当前步骤
    await call('post', '/reservations', { roomId: reservationForm.roomId, seatId: selectedSeat.value.id, reserveDate: reservationForm.date, startTime: reservationForm.startTime, endTime: reservationForm.endTime }) // 【行】带 JWT 调用后端 REST API
    confirmReservationOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    notify('预约成功') // 【行】执行本行语句，推进功能链中的当前步骤
    await Promise.all([loadReservations(), loadAvailableSeats()]) // 【行】执行本行语句，推进功能链中的当前步骤
    studentPage.value = 'checkin' // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
/** 【F3-3·我的预约】功能链实例：小明在「我的 → 我的预约」按 Tab 筛「待使用」→ 看到刚约的 A-12；管理员签到后，签到页每 2 秒轮询同一接口，状态自动变「使用中」。 本处职责：GET /reservations/my 拉取小明全部预约，供列表与签到页轮询*/
async function loadReservations() { // 【行】进入代码块
  reservations.value = await call('get', '/reservations/my') // 【行】带 JWT 调用后端 REST API
}
/** 【F3-2·取消预约】功能链实例：小明在「我的预约」取消一条「待使用」→ 状态「已取消」→ 信用 **−50**（`credit_cancel_penalty`）→ `reservation_slot` 释放。 本处职责：小明取消待使用预约，提示扣 50 信用分*/
async function cancelReservation(r) { // 【行】进入代码块
  await call('post', `/reservations/${r.id}/cancel`) // 【行】带 JWT 调用后端 REST API
          notify('已取消预约，扣除 50 信用分') // 【行】执行本行语句，推进功能链中的当前步骤
  await Promise.all([loadReservations(), loadCredit()]) // 【行】执行本行语句，推进功能链中的当前步骤
}
async function checkout() { // 【行】进入代码块
  confirmCheckout() // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F2-4·账号资料与安全】功能链实例：小明在「我的 → 设置」改密码 → 成功后强制退出 → 用新密码再登录；或在个人资料里改学院/专业。 本处职责：小明在设置里改学院/专业，PUT /student/profile*/
async function saveProfile() { // 【行】进入代码块
  try { // 【行】进入代码块
    me.value = await call('put', '/student/profile', profileForm) // 【行】带 JWT 调用后端 REST API
    notify('资料已保存') // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
async function uploadLayoutImage(e) { // 【行】进入代码块
  const file = e.target.files?.[0] // 【行】声明并赋值变量 `file`
  if (!file) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (!token.value) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请先登录管理端后再上传图片') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  try { // 【行】进入代码块
    const form = new FormData() // 【行】声明并赋值变量 `form`
    form.append('file', file) // 【行】执行本行语句，推进功能链中的当前步骤
    form.append('category', 'layout') // 【行】执行本行语句，推进功能链中的当前步骤
    const res = await api.post('/upload', form, { headers: { 'Content-Type': 'multipart/form-data' } }) // 【行】声明并赋值变量 `res`
    roomForm.layoutImageUrl = res.data.data.url // 【行】执行本行语句，推进功能链中的当前步骤
    notify('图片上传成功') // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (err) { notify(err.message || '上传失败') }
}
function syncProfileForm() { // 【行】进入代码块
  Object.assign(profileForm, { // 【行】进入代码块
    name: me.value.name || '', // 【行】执行本行语句，推进功能链中的当前步骤
    phone: me.value.phone || '', // 【行】执行本行语句，推进功能链中的当前步骤
    email: me.value.email || '', // 【行】执行本行语句，推进功能链中的当前步骤
    college: me.value.college || '', // 【行】执行本行语句，推进功能链中的当前步骤
    major: me.value.major || '', // 【行】执行本行语句，推进功能链中的当前步骤
    grade: me.value.grade || '' // 【行】执行本行语句，推进功能链中的当前步骤
  }) // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F4-2·签退与信用】功能链实例：小明使用中点「签退」→ 确认 → 预约「已完成」→ 信用页看到签到 +5 流水与当前分数。 本处职责：小明签退后 loadCredit 拉取 credit_log 与当前积分*/
async function loadCredit() { // 【行】进入代码块
  credit.value = await call('get', '/credits/my') // 【行】带 JWT 调用后端 REST API
}
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：小明签退后 loadStudyStats 拉取学习时长并 sync 起止日期 */
async function loadStudyStats() { // 【行】进入代码块
  studyStats.value = await call('get', '/statistics/my-study-duration', null, { params: buildStudyStatsParams() }) // 【行】带 JWT 调用后端 REST API
  syncStudyStatsDateRangeFromSummary(studyStats.value) // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：小明首页 loadAnnouncements 展示公告卡片*/
async function loadAnnouncements() { // 【行】进入代码块
  announcements.value = await call('get', '/announcements') // 【行】带 JWT 调用后端 REST API
}
async function readAnnouncement(a) { // 【行】进入代码块
  await call('post', `/announcements/${a.id}/read`) // 【行】带 JWT 调用后端 REST API
  activeAnnouncement.value = a // 【行】执行本行语句，推进功能链中的当前步骤
  announcementDetailOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  await loadAnnouncements() // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：小明首页铃铛 loadNotifications 展示预约成功等站内通知*/
async function loadNotifications() { // 【行】进入代码块
  notifications.value = await call('get', '/notifications') // 【行】带 JWT 调用后端 REST API
}
function openNotifications() { // 【行】进入代码块
  studentPage.value = 'notifications' // 【行】执行本行语句，推进功能链中的当前步骤
  loadNotifications() // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：小明点一条通知 POST /notifications/{id}/read*/
async function readNotification(n) { // 【行】进入代码块
  await call('post', `/notifications/${n.id}/read`) // 【行】带 JWT 调用后端 REST API
  await loadNotifications() // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：小明点「全部已读」POST /notifications/read-all*/
async function readAllNotifications() { // 【行】进入代码块
  await call('post', '/notifications/read-all') // 【行】带 JWT 调用后端 REST API
  await loadNotifications() // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-3·问题反馈】功能链实例：小明提交「A-12 椅子损坏」→ 管理员标记已处理。 本处职责：小明 POST /feedback 提交座位问题*/
async function submitFeedback(payload) { // 【行】进入代码块
  const content = typeof payload === 'string' ? payload : payload?.content // 【行】声明并赋值变量 `content`
  const severity = typeof payload === 'object' && payload?.severity ? payload.severity : '中' // 【行】声明并赋值变量 `severity`
  if (!String(content || '').trim()) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  await call('post', '/feedback', { content, type: '建议', severity, roomId: reservationForm.roomId, seatId: selectedSeat.value?.id }) // 【行】带 JWT 调用后端 REST API
  notify('反馈已提交') // 【行】执行本行语句，推进功能链中的当前步骤
  studentPage.value = 'profile' // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：openStudyStats 从「我的」进入统计页并首次拉取数据 */
async function openStudyStats() { // 【行】进入代码块
  studentPage.value = 'stats' // 【行】切换学生端子页面为学习统计
  await loadStudyStats() // 【行】异步拉取学习统计数据并写入 studyStats ref
  drawStudentChart() // 【行】根据最新 studyBars 重绘 ECharts 柱图
}
async function changeStatPeriod(period) { // 【行】进入代码块
  statPeriod.value = period // 【行】切换日报/周报/月报/年报周期 Tab
  await loadStudyStats() // 【行】异步拉取学习统计数据并写入 studyStats ref
  drawStudentChart() // 【行】根据最新 studyBars 重绘 ECharts 柱图
}
function statusText(status) { // 【行】进入代码块
  return reservationStatusValue(status) || '-' // 【行】返回本函数计算结果给调用方
}
async function openAdmin(page) { // 【行】进入代码块
  adminPage.value = page // 【行】执行本行语句，推进功能链中的当前步骤
  if (page === 'users') await loadUsers() // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (page === 'admins') await loadAdminAccounts() // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (page === 'rooms') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    await loadRooms() // 【行】执行本行语句，推进功能链中的当前步骤
    if (isSuperAdmin.value) await loadAdminAccounts() // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  }
  /** 【F6-5·预约监管】功能链实例：小明被标「已违约」→ 管理员在预约管理点「撤销违约」→ 信用分恢复。 本处职责：管理员预约监管页 GET /admin/reservations 拉全站预约*/
  if (page === 'reservations') adminReservations.value = await call('get', '/admin/reservations') // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (page === 'checkins') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    checkins.value = await call('get', '/admin/checkins') // 【行】带 JWT 调用后端 REST API
    scanStudentNo.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
    scanHint.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
    await loadLiveReservations() // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (page === 'announcements') await loadAnnouncements() // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (page === 'statistics') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    await loadRooms() // 【行】执行本行语句，推进功能链中的当前步骤
    await loadAdminStatistics() // 【行】执行本行语句，推进功能链中的当前步骤
  }
  if (page === 'feedback') adminFeedback.value = await call('get', '/admin/feedback') // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (page === 'settings') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    operationLogs.value = await call('get', '/admin/operation-logs') // 【行】带 JWT 调用后端 REST API
    await loadSystemConfig() // 【行】执行本行语句，推进功能链中的当前步骤
    if (isSuperAdmin.value) await loadAdminAccounts() // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  }
}
async function loadSystemConfig() { // 【行】进入代码块
  try { // 【行】进入代码块
    const config = await call('get', '/admin/settings/config') // 【行】带 JWT 调用后端 REST API
    if (config) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      sysConfigForm.reservation_advance_days = Number(config.reservation_advance_days ?? 7) // 【行】执行本行语句，推进功能链中的当前步骤
      sysConfigForm.reservation_limit_duration = Number(config.reservation_limit_duration ?? 4) // 【行】执行本行语句，推进功能链中的当前步骤
      sysConfigForm.reservation_limit_daily = Number(config.reservation_limit_daily ?? 3) // 【行】执行本行语句，推进功能链中的当前步骤
      sysConfigForm.credit_checkin_reward = Number(config.credit_checkin_reward ?? 5) // 【行】执行本行语句，推进功能链中的当前步骤
      sysConfigForm.credit_cancel_penalty = Number(config.credit_cancel_penalty ?? -50) // 【行】执行本行语句，推进功能链中的当前步骤
      sysConfigForm.credit_violation_penalty = Number(config.credit_violation_penalty ?? -50) // 【行】执行本行语句，推进功能链中的当前步骤
      sysConfigForm.credit_blocked_threshold = Number(config.credit_blocked_threshold ?? 0) // 【行】执行本行语句，推进功能链中的当前步骤
      sysConfigForm.blacklist_days = Number(config.blacklist_days ?? 7) // 【行】执行本行语句，推进功能链中的当前步骤
    }
  } catch (e) { // 【行】进入代码块
    notify('加载系统配置失败: ' + e.message) // 【行】执行本行语句，推进功能链中的当前步骤
  }
}

/** 【F6-2·系统配置】功能链实例：superadmin 把单次最长预约改为 4 小时 → 保存 → 写入 `system_config.json` → 下次预约立即按新规则校验。 本处职责：superadmin saveSystemConfig 写入预约/信用规则*/
async function saveSystemConfig() { // 【行】进入代码块
  try { // 【行】进入代码块
    const payload = { // 【行】声明并赋值变量 `payload`
      reservation_advance_days: String(sysConfigForm.reservation_advance_days), // 【行】执行本行语句，推进功能链中的当前步骤
      reservation_limit_duration: String(sysConfigForm.reservation_limit_duration), // 【行】执行本行语句，推进功能链中的当前步骤
      reservation_limit_daily: String(sysConfigForm.reservation_limit_daily), // 【行】执行本行语句，推进功能链中的当前步骤
      credit_checkin_reward: String(sysConfigForm.credit_checkin_reward), // 【行】执行本行语句，推进功能链中的当前步骤
      credit_cancel_penalty: String(sysConfigForm.credit_cancel_penalty), // 【行】执行本行语句，推进功能链中的当前步骤
      credit_violation_penalty: String(sysConfigForm.credit_violation_penalty), // 【行】执行本行语句，推进功能链中的当前步骤
      credit_blocked_threshold: String(sysConfigForm.credit_blocked_threshold), // 【行】执行本行语句，推进功能链中的当前步骤
      blacklist_days: String(sysConfigForm.blacklist_days) // 【行】执行本行语句，推进功能链中的当前步骤
    }
    await call('post', '/admin/settings/config', payload) // 【行】带 JWT 调用后端 REST API
    notify('保存配置成功') // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { // 【行】进入代码块
    notify('保存配置失败: ' + e.message) // 【行】执行本行语句，推进功能链中的当前步骤
  }
}

async function loadAdminAccounts() { // 【行】进入代码块
  try { // 【行】进入代码块
    adminAccounts.value = await call('get', '/admin/admins') // 【行】带 JWT 调用后端 REST API
  } catch (e) { // 【行】进入代码块
    adminAccounts.value = [] // 【行】执行本行语句，推进功能链中的当前步骤
    if (isSuperAdmin.value) notify(e.message) // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  }
}
function openAdminForm(row = null) { // 【行】进入代码块
  if (!isSuperAdmin.value) return notify('仅超级管理员可管理管理员账号') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  Object.assign(adminForm, { // 【行】进入代码块
    id: row?.id || null, // 【行】执行本行语句，推进功能链中的当前步骤
    account: row?.account || '', // 【行】执行本行语句，推进功能链中的当前步骤
    name: row?.name || '', // 【行】执行本行语句，推进功能链中的当前步骤
    phone: row?.phone || '', // 【行】执行本行语句，推进功能链中的当前步骤
    password: '', // 【行】执行本行语句，推进功能链中的当前步骤
    isSuperAdmin: isSuperAdminRole(row?.role) // 【行】执行本行语句，推进功能链中的当前步骤
  }) // 【行】执行本行语句，推进功能链中的当前步骤
  adminFormOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F6-7·管理员与日志】功能链实例：superadmin 在「设置 → 操作日志」查看审核/改密等记录；在「管理员管理」新增普管账号。 本处职责：superadmin POST/PUT /admin/admins 新增或改普管账号*/
async function saveAdminAccount() { // 【行】进入代码块
  if (!adminForm.account.trim() || !adminForm.name.trim()) return notify('请填写账号与姓名') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (!adminForm.id && (!adminForm.password || adminForm.password.length < 6)) return notify('请设置至少6位初始密码') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    if (adminForm.id) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      await call('put', `/admin/admins/${adminForm.id}`, { // 【行】带 JWT 调用后端 REST API
        name: adminForm.name.trim(), // 【行】执行本行语句，推进功能链中的当前步骤
        phone: adminForm.phone.trim(), // 【行】执行本行语句，推进功能链中的当前步骤
        password: adminForm.password || undefined // 【行】执行本行语句，推进功能链中的当前步骤
      }) // 【行】执行本行语句，推进功能链中的当前步骤
    } else { // 【行】进入代码块
      await call('post', '/admin/admins', { // 【行】带 JWT 调用后端 REST API
        account: adminForm.account.trim(), // 【行】执行本行语句，推进功能链中的当前步骤
        name: adminForm.name.trim(), // 【行】执行本行语句，推进功能链中的当前步骤
        phone: adminForm.phone.trim(), // 【行】执行本行语句，推进功能链中的当前步骤
        password: adminForm.password // 【行】执行本行语句，推进功能链中的当前步骤
      }) // 【行】执行本行语句，推进功能链中的当前步骤
    }
    adminFormOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    notify('管理员已保存') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadAdminAccounts() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
async function disableAdminAccount(row) { // 【行】进入代码块
  try { // 【行】进入代码块
    await call('post', `/admin/admins/${row.id}/disable`) // 【行】带 JWT 调用后端 REST API
    notify('已禁用') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadAdminAccounts() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
async function enableAdminAccount(row) { // 【行】进入代码块
  try { // 【行】进入代码块
    await call('post', `/admin/admins/${row.id}/enable`) // 【行】带 JWT 调用后端 REST API
    notify('已启用') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadAdminAccounts() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
function resolveUserId(rowOrId) { // 【行】进入代码块
  if (rowOrId && typeof rowOrId === 'object') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return rowOrId.userId ?? rowOrId.user_id ?? rowOrId.id // 【行】返回本函数计算结果给调用方
  }
  return rowOrId // 【行】返回本函数计算结果给调用方
}
function auditStatusLabel(status) { // 【行】进入代码块
  return auditStatusValue(status) || '-' // 【行】返回本函数计算结果给调用方
}
function accountStatusLabel(status) { // 【行】进入代码块
  return accountStatusValue(status) || '-' // 【行】返回本函数计算结果给调用方
}
function decorateUserRow(row) { // 【行】进入代码块
  return { // 【行】返回本函数计算结果给调用方
    ...row, // 【行】执行本行语句，推进功能链中的当前步骤
    accountStatus: row.accountStatus || row.status, // 【行】执行本行语句，推进功能链中的当前步骤
    auditLabel: auditStatusLabel(row.audit_status), // 【行】执行本行语句，推进功能链中的当前步骤
    statusLabel: accountStatusLabel(row.accountStatus || row.status) // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F6-3·用户管理】功能链实例：管理员在用户管理拒绝小李注册，或禁用违规学生；可导出 CSV。 本处职责：管理员打开用户管理 GET /admin/users 带 keyword/auditStatus 筛选*/
async function loadUsers() { // 【行】进入代码块
  const params = { keyword: userKeyword.value || undefined } // 【行】初始化 GET 查询参数字典，键名与后端约定一致
  if (userAuditFilter.value) params.auditStatus = userAuditFilter.value // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  users.value = (await call('get', '/admin/users', null, { params })).map(decorateUserRow) // 【行】带 JWT 调用后端 REST API
  userPage.value = 1 // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F6-3·用户管理】功能链实例：管理员在用户管理拒绝小李注册，或禁用违规学生；可导出 CSV。 本处职责：管理员导出学生名单 GET /admin/users/export 下载 CSV*/
function exportUsersCsv() { // 【行】进入代码块
  api.get('/admin/users/export', { // 【行】进入代码块
    responseType: 'blob', // 【行】执行本行语句，推进功能链中的当前步骤
    params: { // 【行】进入代码块
      keyword: userKeyword.value || undefined, // 【行】执行本行语句，推进功能链中的当前步骤
      auditStatus: userAuditFilter.value || undefined // 【行】执行本行语句，推进功能链中的当前步骤
    }
  }).then(res => { // 【行】进入代码块
    const url = URL.createObjectURL(res.data) // 【行】声明并赋值变量 `url`
    const a = document.createElement('a') // 【行】声明并赋值变量 `a`
    a.href = url // 【行】执行本行语句，推进功能链中的当前步骤
    a.download = 'student-users.csv' // 【行】执行本行语句，推进功能链中的当前步骤
    a.click() // 【行】执行本行语句，推进功能链中的当前步骤
    URL.revokeObjectURL(url) // 【行】执行本行语句，推进功能链中的当前步骤
    notify('用户 CSV 已导出') // 【行】执行本行语句，推进功能链中的当前步骤
  }).catch(e => notify(e.message || '导出失败')) // 【行】执行本行语句，推进功能链中的当前步骤
}
function openUserDetail(row) { // 【行】进入代码块
  userDetail.value = { ...row }
  userDetailOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
function approveFromDetail() { // 【行】进入代码块
  approve(userDetail.value).then(() => { userDetailOpen.value = false }) // 【行】执行本行语句，推进功能链中的当前步骤
}
function rejectFromDetail() { // 【行】进入代码块
  reject(userDetail.value) // 【行】执行本行语句，推进功能链中的当前步骤
  userDetailOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F2-3·注册审核】功能链实例：小李注册并上传 PDF 材料 → 尝试登录得「注册资料待审核」→ 管理员在用户管理点「通过」→ 小李再登录进入首页。 本处职责：管理员点「通过」，POST /admin/users/{id}/approve*/
async function approve(row) { // 【行】进入代码块
  const id = resolveUserId(row) // 【行】声明并赋值变量 `id`
  if (!id) return notify('无法识别用户 ID') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    await call('post', `/admin/users/${id}/approve`, {}) // 【行】带 JWT 调用后端 REST API
    notify('审核通过') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadUsers() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
function reject(row) { // 【行】进入代码块
  const id = resolveUserId(row) // 【行】声明并赋值变量 `id`
  if (!id) return notify('无法识别用户 ID') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  rejectUserId.value = id // 【行】执行本行语句，推进功能链中的当前步骤
  rejectRemark.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
  rejectOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
function openChangePassword() { // 【行】进入代码块
  changePasswordForm.oldPassword = '' // 【行】执行本行语句，推进功能链中的当前步骤
  changePasswordForm.newPassword = '' // 【行】执行本行语句，推进功能链中的当前步骤
  changePasswordForm.confirmPassword = '' // 【行】执行本行语句，推进功能链中的当前步骤
  changePasswordOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F2-4·账号资料与安全】功能链实例：小明在「我的 → 设置」改密码 → 成功后强制退出 → 用新密码再登录；或在个人资料里改学院/专业。 本处职责：小明改密码 POST /auth/change-password，成功后强制重新登录*/
async function submitChangePassword() { // 【行】进入代码块
  if (!changePasswordForm.oldPassword || !changePasswordForm.newPassword || !changePasswordForm.confirmPassword) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return notify('请填写完整密码信息') // 【行】返回本函数计算结果给调用方
  }
  if (changePasswordForm.newPassword !== changePasswordForm.confirmPassword) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return notify('两次新密码不一致') // 【行】返回本函数计算结果给调用方
  }
  if (changePasswordForm.newPassword.length < 6 || changePasswordForm.newPassword.length > 20) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return notify('新密码长度需为 6-20 位') // 【行】返回本函数计算结果给调用方
  }
  if (!/(?=.*[A-Za-z])(?=.*\d)/.test(changePasswordForm.newPassword)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    return notify('新密码需同时包含字母和数字') // 【行】返回本函数计算结果给调用方
  }
  try { // 【行】进入代码块
    await call('post', '/auth/change-password', { // 【行】带 JWT 调用后端 REST API
      oldPassword: changePasswordForm.oldPassword, // 【行】执行本行语句，推进功能链中的当前步骤
      newPassword: changePasswordForm.newPassword // 【行】执行本行语句，推进功能链中的当前步骤
    }) // 【行】执行本行语句，推进功能链中的当前步骤
    changePasswordOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    notify('密码已修改，请使用新密码重新登录') // 【行】执行本行语句，推进功能链中的当前步骤
    logout() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
/** 【F6-3·用户管理】功能链实例：管理员在用户管理拒绝小李注册，或禁用违规学生；可导出 CSV。 本处职责：管理员拒绝小李注册，POST /admin/users/{id}/reject*/
async function confirmReject() { // 【行】进入代码块
  if (!rejectUserId.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    await call('post', `/admin/users/${rejectUserId.value}/reject`, { remark: rejectRemark.value || '资料不符合要求' }) // 【行】带 JWT 调用后端 REST API
    rejectOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    notify('已拒绝') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadUsers() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
/** 【F6-3·用户管理】功能链实例：管理员在用户管理拒绝小李注册，或禁用违规学生；可导出 CSV。 本处职责：管理员禁用违规学生账号 POST /admin/users/{id}/disable*/
async function disable(row) { // 【行】进入代码块
  const id = resolveUserId(row) // 【行】声明并赋值变量 `id`
  if (!id) return notify('无法识别用户 ID') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    await call('post', `/admin/users/${id}/disable`) // 【行】带 JWT 调用后端 REST API
    notify('已禁用') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadUsers() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
/** 【F6-3·用户管理】功能链实例：管理员在用户管理拒绝小李注册，或禁用违规学生；可导出 CSV。 本处职责：管理员重新启用学生 POST /admin/users/{id}/enable*/
async function enable(row) { // 【行】进入代码块
  const id = resolveUserId(row) // 【行】声明并赋值变量 `id`
  if (!id) return notify('无法识别用户 ID') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    await call('post', `/admin/users/${id}/enable`) // 【行】带 JWT 调用后端 REST API
    notify('已启用') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadUsers() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
function editRoom(r = {}) { // 【行】进入代码块
  Object.assign(roomForm, { // 【行】进入代码块
    id: r.id || null, // 【行】执行本行语句，推进功能链中的当前步骤
    roomCode: r.room_code || '', // 【行】执行本行语句，推进功能链中的当前步骤
    name: r.name || '', // 【行】执行本行语句，推进功能链中的当前步骤
    location: r.location || '', // 【行】执行本行语句，推进功能链中的当前步骤
    floor: r.floor || '1楼', // 【行】执行本行语句，推进功能链中的当前步骤
    openTime: String(r.open_time || '07:00:00'), // 【行】执行本行语句，推进功能链中的当前步骤
    closeTime: String(r.close_time || '22:30:00'), // 【行】执行本行语句，推进功能链中的当前步骤
    layoutImageUrl: r.layout_image_url || '', // 【行】执行本行语句，推进功能链中的当前步骤
    rowCount: r.row_count || 4, // 【行】执行本行语句，推进功能链中的当前步骤
    colCount: r.col_count || 6, // 【行】执行本行语句，推进功能链中的当前步骤
    status: roomStatusValue(r.status) || '开放', // 【行】执行本行语句，推进功能链中的当前步骤
    facilities: r.facilities || '空调,WiFi', // 【行】执行本行语句，推进功能链中的当前步骤
    managerId: r.manager_id || r.managerId || null // 【行】执行本行语句，推进功能链中的当前步骤
  }) // 【行】执行本行语句，推进功能链中的当前步骤
  seatKeyword.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
  seatStatusFilter.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
  roomFormOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  if (r.id) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    nextTick(() => loadAdminSeats()) // 【行】执行本行语句，推进功能链中的当前步骤
  } else { // 【行】进入代码块
    adminSeats.value = [] // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F6-4·自习室与座位】功能链实例：superadmin 新增 B 自习室并保存 → 同步 4×6 座位网格 → 在布局图里改 A-12 为「靠窗」。 本处职责：superadmin 保存自习室 POST/PUT /admin/rooms，同步座位网格*/
async function saveRoom() { // 【行】进入代码块
  if (!roomForm.name?.trim()) return notify('请填写自习室名称') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (!roomForm.location?.trim()) return notify('请填写自习室位置') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (isSuperAdmin.value && !roomForm.id && !roomForm.managerId) return notify('请选择自习室负责人') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  const method = roomForm.id ? 'put' : 'post' // 【行】声明并赋值变量 `method`
  const url = roomForm.id ? `/admin/rooms/${roomForm.id}` : '/admin/rooms' // 【行】声明并赋值变量 `url`
  try { // 【行】进入代码块
    const payload = { // 【行】声明并赋值变量 `payload`
      roomCode: roomForm.roomCode || `ROOM-${Date.now()}`, // 【行】执行本行语句，推进功能链中的当前步骤
      name: roomForm.name.trim(), // 【行】执行本行语句，推进功能链中的当前步骤
      location: roomForm.location.trim(), // 【行】执行本行语句，推进功能链中的当前步骤
      floor: roomForm.floor || '1楼', // 【行】执行本行语句，推进功能链中的当前步骤
      openTime: roomForm.openTime || '07:00:00', // 【行】执行本行语句，推进功能链中的当前步骤
      closeTime: roomForm.closeTime || '22:30:00', // 【行】执行本行语句，推进功能链中的当前步骤
      facilities: roomForm.facilities || '空调,WiFi', // 【行】执行本行语句，推进功能链中的当前步骤
      layoutImageUrl: roomForm.layoutImageUrl || '', // 【行】执行本行语句，推进功能链中的当前步骤
      rowCount: roomForm.rowCount || 4, // 【行】执行本行语句，推进功能链中的当前步骤
      colCount: roomForm.colCount || 6, // 【行】执行本行语句，推进功能链中的当前步骤
      status: roomStatusValue(roomForm.status) || '开放' // 【行】执行本行语句，推进功能链中的当前步骤
    }
    if (isSuperAdmin.value && roomForm.managerId) payload.managerId = roomForm.managerId // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    const isCreate = !roomForm.id // 【行】声明并赋值变量 `isCreate`
    const saved = await call(method, url, payload) // 【行】带 JWT 调用后端 REST API
    if (saved?.id) roomForm.id = saved.id // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify(isCreate ? '自习室已创建，可在下方编辑座位' : '自习室已保存，座位网格已同步，可继续在下方编辑座位') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadRooms() // 【行】执行本行语句，推进功能链中的当前步骤
    await loadAdminSeats() // 【行】执行本行语句，推进功能链中的当前步骤
    if (reservationForm.roomId && Number(reservationForm.roomId) === Number(roomForm.id)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      await loadAvailableSeats() // 【行】执行本行语句，推进功能链中的当前步骤
    }
  } catch (e) { notify(e.message || '保存失败') }
}
/** 【F6-4·自习室与座位】功能链实例：superadmin 新增 B 自习室并保存 → 同步 4×6 座位网格 → 在布局图里改 A-12 为「靠窗」。 本处职责：superadmin DELETE /admin/rooms/{id} 删除空自习室*/
async function deleteRoom(r) { // 【行】进入代码块
  try { // 【行】进入代码块
    await call('delete', `/admin/rooms/${r.id}`) // 【行】带 JWT 调用后端 REST API
    notify('已删除') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadRooms() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
/** 【F6-4·自习室与座位】功能链实例：superadmin 新增 B 自习室并保存 → 同步 4×6 座位网格 → 在布局图里改 A-12 为「靠窗」。 本处职责：编辑室弹窗 GET /admin/rooms/{id}/seats 拉座位网格*/
async function loadAdminSeats() { // 【行】进入代码块
  if (!roomFormOpen.value || !roomForm.id) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    adminSeats.value = [] // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  adminSeats.value = await call('get', `/admin/rooms/${roomForm.id}/seats`) // 【行】带 JWT 调用后端 REST API
}
async function toggleSeat(s) { // 【行】进入代码块
  const nextStatus = seatStatusValue(s.status) === '空闲' ? '停用' : '空闲' // 【行】声明并赋值变量 `nextStatus`
  await call('put', `/admin/seats/${s.id}`, { ...s, isSeat: s.is_seat, cellCategory: s.cell_category, seatType: s.seat_type, hasPower: s.has_power, nearWindow: s.near_window, quietZone: s.quiet_zone, hotSeat: s.hot_seat, status: nextStatus }) // 【行】带 JWT 调用后端 REST API
  await loadAdminSeats() // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：admin 输入小明学号 POST /admin/checkin/scan*/
async function scanCheckin() { // 【行】进入代码块
  if (scanBusy.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  const studentNo = scanStudentNo.value.trim() // 【行】声明并赋值变量 `studentNo`
  if (!studentNo) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    notify('请输入学生学号') // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  scanBusy.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  scanHint.value = `正在提交签到（学号 ${studentNo}）…` // 【行】执行本行语句，推进功能链中的当前步骤
  try { // 【行】进入代码块
    await call('post', '/admin/checkin/scan', { studentNo }) // 【行】带 JWT 调用后端 REST API
    notify('签到成功') // 【行】执行本行语句，推进功能链中的当前步骤
    scanStudentNo.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
    scanHint.value = '签到成功。可继续输入学号或拍照扫码下一位学生。' // 【行】执行本行语句，推进功能链中的当前步骤
    try { // 【行】进入代码块
      checkins.value = await call('get', '/admin/checkins') // 【行】带 JWT 调用后端 REST API
      await loadLiveReservations() // 【行】执行本行语句，推进功能链中的当前步骤
    } catch { // 【行】进入代码块
      /* 列表刷新失败不影响签到结果 */
    }
  } catch (e) { // 【行】进入代码块
    scanHint.value = e.message || '签到失败，请重试或检查网络' // 【行】执行本行语句，推进功能链中的当前步骤
    notify(e.message || '签到失败') // 【行】执行本行语句，推进功能链中的当前步骤
  } finally { // 【行】进入代码块
    scanBusy.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 从拍照/二维码文本解析学号（支持纯学号或旧版 token 二维码） */
function normalizeStudentNoFromScan(raw) { // 【行】进入代码块
  const text = String(raw || '').trim() // 【行】声明并赋值变量 `text`
  if (/^\d{10,20}$/.test(text)) return text // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    let b64 = text.replace(/-/g, '+').replace(/_/g, '/') // 【行】声明并赋值变量 `b64`
    while (b64.length % 4) b64 += '=' // 【行】执行本行语句，推进功能链中的当前步骤
    const decoded = atob(b64) // 【行】声明并赋值变量 `decoded`
    const parts = decoded.split(':') // 【行】声明并赋值变量 `parts`
    if (parts.length >= 4 && /^\d{10,20}$/.test(parts[3])) return parts[3] // 【行】条件不满足时提前结束，避免无效请求或错误状态
  } catch { /* 非 token */ }
  return '' // 【行】返回本函数计算结果给调用方
}
/** 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：admin 拍照/选图，jsQR 解析学号后提交签到（非视频流）*/
function triggerPhotoScan() { // 【行】进入代码块
  if (scanBusy.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  scanPhotoInput.value?.click() // 【行】执行本行语句，推进功能链中的当前步骤
}
function loadImageFromUrl(url) { // 【行】进入代码块
  return new Promise((resolve, reject) => { // 【行】返回本函数计算结果给调用方
    const el = new Image() // 【行】声明并赋值变量 `el`
    el.onload = () => resolve(el) // 【行】执行本行语句，推进功能链中的当前步骤
    el.onerror = () => reject(new Error('无法读取照片')) // 【行】执行本行语句，推进功能链中的当前步骤
    el.src = url // 【行】执行本行语句，推进功能链中的当前步骤
  }) // 【行】执行本行语句，推进功能链中的当前步骤
}
function buildScanCanvas(img, maxSide) { // 【行】进入代码块
  let w = img.naturalWidth || img.width // 【行】声明并赋值变量 `w`
  let h = img.naturalHeight || img.height // 【行】声明并赋值变量 `h`
  if (!w || !h) return null // 【行】条件不满足时提前结束，避免无效请求或错误状态
  if (Math.max(w, h) > maxSide) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    const ratio = maxSide / Math.max(w, h) // 【行】声明并赋值变量 `ratio`
    w = Math.max(1, Math.round(w * ratio)) // 【行】执行本行语句，推进功能链中的当前步骤
    h = Math.max(1, Math.round(h * ratio)) // 【行】执行本行语句，推进功能链中的当前步骤
  }
  const canvas = document.createElement('canvas') // 【行】声明并赋值变量 `canvas`
  canvas.width = w // 【行】执行本行语句，推进功能链中的当前步骤
  canvas.height = h // 【行】执行本行语句，推进功能链中的当前步骤
  const ctx = canvas.getContext('2d', { willReadFrequently: true }) // 【行】声明并赋值变量 `ctx`
  if (!ctx) return null // 【行】条件不满足时提前结束，避免无效请求或错误状态
  ctx.drawImage(img, 0, 0, w, h) // 【行】执行本行语句，推进功能链中的当前步骤
  return canvas // 【行】返回本函数计算结果给调用方
}
function decodeJsQrFromCanvas(canvas) { // 【行】进入代码块
  const ctx = canvas.getContext('2d', { willReadFrequently: true }) // 【行】声明并赋值变量 `ctx`
  if (!ctx) return '' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height) // 【行】声明并赋值变量 `imageData`
  const result = jsQR(imageData.data, imageData.width, imageData.height, { inversionAttempts: 'attemptBoth' }) // 【行】声明并赋值变量 `result`
  return result?.data?.trim() || '' // 【行】返回本函数计算结果给调用方
}
async function tryBarcodeDetectorOnCanvas(canvas) { // 【行】进入代码块
  if (!('BarcodeDetector' in window)) return '' // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    const detector = new window.BarcodeDetector({ formats: ['qr_code'] }) // 【行】声明并赋值变量 `detector`
    const codes = await Promise.race([ // 【行】声明并赋值变量 `codes`
      detector.detect(canvas), // 【行】执行本行语句，推进功能链中的当前步骤
      new Promise((_, reject) => setTimeout(() => reject(new Error('timeout')), 1200)) // 【行】执行本行语句，推进功能链中的当前步骤
    ]) // 【行】执行本行语句，推进功能链中的当前步骤
    return codes[0]?.rawValue?.trim() || '' // 【行】返回本函数计算结果给调用方
  } catch { // 【行】进入代码块
    return '' // 【行】返回本函数计算结果给调用方
  }
}
async function decodeQrFromImageFile(file) { // 【行】进入代码块
  const name = file.name || '' // 【行】声明并赋值变量 `name`
  const type = file.type || '' // 【行】声明并赋值变量 `type`
  if (/heic|heif/i.test(type) || /\.heic$|\.heif$/i.test(name)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    throw new Error('HEIC 照片浏览器无法解析，请点「拍照」现拍 JPG，或直接输入学号') // 【行】执行本行语句，推进功能链中的当前步骤
  }
  const url = URL.createObjectURL(file) // 【行】声明并赋值变量 `url`
  try { // 【行】进入代码块
    const img = await loadImageFromUrl(url) // 【行】声明并赋值变量 `img`
    const sizes = [960, 1280, 640] // 【行】声明并赋值变量 `sizes`
    for (const size of sizes) { // 【行】进入代码块
      const canvas = buildScanCanvas(img, size) // 【行】声明并赋值变量 `canvas`
      if (!canvas) continue // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      const fromJs = decodeJsQrFromCanvas(canvas) // 【行】声明并赋值变量 `fromJs`
      if (fromJs) return fromJs // 【行】条件不满足时提前结束，避免无效请求或错误状态
    }
    const fallbackCanvas = buildScanCanvas(img, 960) // 【行】声明并赋值变量 `fallbackCanvas`
    if (fallbackCanvas) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      const fromNative = await tryBarcodeDetectorOnCanvas(fallbackCanvas) // 【行】声明并赋值变量 `fromNative`
      if (fromNative) return fromNative // 【行】条件不满足时提前结束，避免无效请求或错误状态
    }
    return '' // 【行】返回本函数计算结果给调用方
  } finally { // 【行】进入代码块
    URL.revokeObjectURL(url) // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：照片解码出学号后自动 POST scan，完成小明签到*/
async function onScanPhotoSelected(ev) { // 【行】进入代码块
  const file = ev.target?.files?.[0] // 【行】声明并赋值变量 `file`
  if (ev.target) ev.target.value = '' // 【行】分支判断：根据当前 UI 状态决定后续逻辑
  if (!file || scanBusy.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  scanBusy.value = true // 【行】执行本行语句，推进功能链中的当前步骤
  scanHint.value = '正在识别照片（已自动压缩，请稍候）…' // 【行】执行本行语句，推进功能链中的当前步骤
  try { // 【行】进入代码块
    const raw = await decodeQrFromImageFile(file) // 【行】声明并赋值变量 `raw`
    if (!raw) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      scanHint.value = '未识别到二维码（与手机好坏无关，常因拍屏摩尔纹/相册 HEIC）。请直接输入学号，或让学生把二维码放大、斜 30° 再拍。' // 【行】执行本行语句，推进功能链中的当前步骤
      notify(scanHint.value) // 【行】执行本行语句，推进功能链中的当前步骤
      return // 【行】执行本行语句，推进功能链中的当前步骤
    }
    const studentNo = normalizeStudentNoFromScan(raw) // 【行】声明并赋值变量 `studentNo`
    if (!/^\d{10,20}$/.test(studentNo)) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      scanHint.value = '识别内容不是有效学号，请让学生出示签到页的学号二维码，或手动输入学号。' // 【行】执行本行语句，推进功能链中的当前步骤
      notify(scanHint.value) // 【行】执行本行语句，推进功能链中的当前步骤
      return // 【行】执行本行语句，推进功能链中的当前步骤
    }
    scanStudentNo.value = studentNo // 【行】执行本行语句，推进功能链中的当前步骤
    scanHint.value = `已识别学号 ${studentNo}，正在提交签到…` // 【行】执行本行语句，推进功能链中的当前步骤
    await call('post', '/admin/checkin/scan', { studentNo }) // 【行】带 JWT 调用后端 REST API
    notify('签到成功') // 【行】执行本行语句，推进功能链中的当前步骤
    scanStudentNo.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
    scanHint.value = '签到成功。可继续输入学号或拍照扫码下一位学生。' // 【行】执行本行语句，推进功能链中的当前步骤
    try { // 【行】进入代码块
      checkins.value = await call('get', '/admin/checkins') // 【行】带 JWT 调用后端 REST API
      await loadLiveReservations() // 【行】执行本行语句，推进功能链中的当前步骤
    } catch { /* ignore */ }
  } catch (e) { // 【行】进入代码块
    const msg = e.message || '照片解析或签到失败' // 【行】声明并赋值变量 `msg`
    scanHint.value = msg.includes('timeout') ? '请求超时，请确认与电脑同一 WiFi 后重试' : msg // 【行】执行本行语句，推进功能链中的当前步骤
    notify(scanHint.value) // 【行】执行本行语句，推进功能链中的当前步骤
  } finally { // 【行】进入代码块
    scanBusy.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
/** 【F4-1·签到】功能链实例：小明签到 Tab 显示学号 **202225220101** 与 QR → 管理员输入学号（或拍照 jsQR 识别）→ 预约变「使用中」→ 信用 **+5**。 本处职责：refreshCheckinQr 用 createQrSvg(学号) 生成 SVG QR*/
async function refreshCheckinQr() { // 【行】进入代码块
  const no = studentNoDisplay.value // 【行】声明并赋值变量 `no`
  if (!no || no === '—') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    checkinQrSvg.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  try { // 【行】进入代码块
    checkinQrSvg.value = await createQrSvg(no) // 【行】执行本行语句，推进功能链中的当前步骤
  } catch { // 【行】进入代码块
    checkinQrSvg.value = '' // 【行】执行本行语句，推进功能链中的当前步骤
  }
}
function editAnnouncement(a = {}) { // 【行】进入代码块
  Object.assign(announcementForm, { id: a.id, title: a.title || '', content: a.content || '', type: a.type || '系统通知', pinned: !!a.pinned }) // 【行】执行本行语句，推进功能链中的当前步骤
  announcementDialog.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-2·公告与通知】功能链实例：管理员发布公告 → 小明首页公告卡片可见；预约成功收到站内通知。 本处职责：管理员发布公告 POST/PUT /admin/announcements*/
async function saveAnnouncement() { // 【行】进入代码块
  const payload = { ...announcementForm, pinned: announcementForm.pinned ? 1 : 0, status: 'PUBLISHED' } // 【行】声明并赋值变量 `payload`
  await call(announcementForm.id ? 'put' : 'post', announcementForm.id ? `/admin/announcements/${announcementForm.id}` : '/admin/announcements', payload) // 【行】带 JWT 调用后端 REST API
  announcementDialog.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  notify('公告已保存') // 【行】执行本行语句，推进功能链中的当前步骤
  await loadAnnouncements() // 【行】执行本行语句，推进功能链中的当前步骤
}
function openFeedbackHandle(row) { // 【行】进入代码块
  feedbackHandleForm.id = row.id // 【行】执行本行语句，推进功能链中的当前步骤
  feedbackHandleForm.studentName = row.studentName // 【行】执行本行语句，推进功能链中的当前步骤
  feedbackHandleForm.type = row.type // 【行】执行本行语句，推进功能链中的当前步骤
  feedbackHandleForm.content = row.content // 【行】执行本行语句，推进功能链中的当前步骤
  feedbackHandleForm.handleResult = '' // 【行】执行本行语句，推进功能链中的当前步骤
  feedbackHandleOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-3·问题反馈】功能链实例：小明提交「A-12 椅子损坏」→ 管理员标记已处理。 本处职责：管理员 PUT /admin/feedback/{id} 标记已处理并通知学生*/
async function submitFeedbackHandle() { // 【行】进入代码块
  if (!feedbackHandleForm.handleResult?.trim()) return notify('请填写处理说明') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    await call('put', `/admin/feedback/${feedbackHandleForm.id}`, { // 【行】带 JWT 调用后端 REST API
      status: '已处理', // 【行】执行本行语句，推进功能链中的当前步骤
      handleResult: feedbackHandleForm.handleResult.trim() // 【行】执行本行语句，推进功能链中的当前步骤
    }) // 【行】执行本行语句，推进功能链中的当前步骤
    feedbackHandleOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    notify('反馈已处理，已通知学生') // 【行】执行本行语句，推进功能链中的当前步骤
    adminFeedback.value = await call('get', '/admin/feedback') // 【行】带 JWT 调用后端 REST API
  } catch (e) { notify(e.message) }
}
function openRevokeViolation(row) { // 【行】进入代码块
  revokeViolationForm.id = row._rawId || row.id // 【行】执行本行语句，推进功能链中的当前步骤
  revokeViolationForm.studentName = row.studentName || '—' // 【行】执行本行语句，推进功能链中的当前步骤
  revokeViolationForm.reservationNo = row.reservation_no || '—' // 【行】执行本行语句，推进功能链中的当前步骤
  revokeViolationForm.roomName = row.roomName || '—' // 【行】执行本行语句，推进功能链中的当前步骤
  revokeViolationForm.seatNo = row.seatNo || '—' // 【行】执行本行语句，推进功能链中的当前步骤
  revokeViolationForm.reserveDate = formatDate(row.reserve_date || row.reserveDate) // 【行】执行本行语句，推进功能链中的当前步骤
  revokeViolationForm.remark = '' // 【行】执行本行语句，推进功能链中的当前步骤
  revokeViolationOpen.value = true // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F6-5·预约监管】功能链实例：小明被标「已违约」→ 管理员在预约管理点「撤销违约」→ 信用分恢复。 本处职责：管理员撤销小明违约，POST revoke-violation 恢复信用分*/
async function submitRevokeViolation() { // 【行】进入代码块
  if (!revokeViolationForm.id) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    await call('post', `/admin/reservations/${revokeViolationForm.id}/revoke-violation`, { // 【行】带 JWT 调用后端 REST API
      remark: revokeViolationForm.remark?.trim() || '' // 【行】执行本行语句，推进功能链中的当前步骤
    }) // 【行】执行本行语句，推进功能链中的当前步骤
    revokeViolationOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
    notify('违约已撤销，信用分已恢复') // 【行】执行本行语句，推进功能链中的当前步骤
    adminReservations.value = await call('get', '/admin/reservations') // 【行】带 JWT 调用后端 REST API
  } catch (e) { notify(e.message) }
}
async function addAdminSeat() { // 【行】进入代码块
  if (!roomForm.id) return notify('请先保存自习室') // 【行】条件不满足时提前结束，避免无效请求或错误状态
  try { // 【行】进入代码块
    await call('post', `/admin/rooms/${roomForm.id}/seats`, {}) // 【行】带 JWT 调用后端 REST API
    notify('座位已补全') // 【行】执行本行语句，推进功能链中的当前步骤
    await loadAdminSeats() // 【行】执行本行语句，推进功能链中的当前步骤
    await loadRooms() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
/** 【F6-4·自习室与座位】功能链实例：superadmin 新增 B 自习室并保存 → 同步 4×6 座位网格 → 在布局图里改 A-12 为「靠窗」。 本处职责：超管 DELETE /admin/seats/{id} 删除单个座位格*/
async function deleteSeatEdit() { // 【行】进入代码块
  if (!seatEditForm.id) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  const seatId = seatEditForm.id // 【行】声明并赋值变量 `seatId`
  const seatLabel = seatEditForm.seat_no || '该座位' // 【行】声明并赋值变量 `seatLabel`
  seatEditOpen.value = false // 【行】执行本行语句，推进功能链中的当前步骤
  await nextTick() // 【行】执行本行语句，推进功能链中的当前步骤
  openModalConfirm('删除座位', `确定删除座位 ${seatLabel} 吗？删除后不可恢复。`, async () => { // 【行】进入代码块
    try { // 【行】进入代码块
      await call('delete', `/admin/seats/${seatId}`) // 【行】带 JWT 调用后端 REST API
      notify('座位已删除') // 【行】执行本行语句，推进功能链中的当前步骤
      await loadAdminSeats() // 【行】执行本行语句，推进功能链中的当前步骤
      await loadRooms() // 【行】执行本行语句，推进功能链中的当前步骤
    } catch (e) { notify(e.message) }
  }) // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F6-1·统计与CSV】功能链实例：管理员打开统计页，切换当期/往期与报表类型，查看图表并导出 CSV 本处职责：管理员统计页 loadAdminStatistics 拉取报表*/
async function loadAdminStatistics() { // 【行】进入代码块
  try { // 【行】进入代码块
    const params = buildAdminStatsParams() // 【行】初始化 GET 查询参数字典，键名与后端约定一致
    adminStatsReport.value = await call('get', '/admin/statistics/report', null, { params }) // 【行】带 JWT 调用后端 REST API
    syncAdminStatsDateRangeFromSummary(adminStatsReport.value.summary || {}) // 【行】执行本行语句，推进功能链中的当前步骤
    await nextTick() // 【行】执行本行语句，推进功能链中的当前步骤
    drawUsageChart() // 【行】执行本行语句，推进功能链中的当前步骤
  } catch (e) { notify(e.message) }
}
/** 【F6-1·统计与CSV】功能链实例：管理员打开统计页，切换当期/往期与报表类型，查看图表并导出 CSV 本处职责：管理员点「导出报表」，downloadReport 下载 CSV blob*/
function downloadReport(reportType = 'usage') { // 【行】进入代码块
  const params = buildAdminStatsParams() // 【行】初始化 GET 查询参数字典，键名与后端约定一致
  params.reportType = reportType // 【行】执行本行语句，推进功能链中的当前步骤
  api.get('/admin/statistics/export', { responseType: 'blob', params }).then(res => { // 【行】进入代码块
    const url = URL.createObjectURL(res.data) // 【行】声明并赋值变量 `url`
    const a = document.createElement('a') // 【行】声明并赋值变量 `a`
    a.href = url // 【行】执行本行语句，推进功能链中的当前步骤
    const labels = { // 【行】声明并赋值变量 `labels`
      usage: '座位使用率报表.csv', // 【行】执行本行语句，推进功能链中的当前步骤
      reservation: '预约量趋势报表.csv', // 【行】执行本行语句，推进功能链中的当前步骤
      peak: '高峰时段分析报表.csv', // 【行】执行本行语句，推进功能链中的当前步骤
      activity: '用户活跃度报表.csv', // 【行】执行本行语句，推进功能链中的当前步骤
      studyDuration: '自习时长排名报表.csv', // 【行】执行本行语句，推进功能链中的当前步骤
      credit: '信用与违约统计报表.csv' // 【行】执行本行语句，推进功能链中的当前步骤
    }
    a.download = labels[reportType] || `${reportType}-report.csv` // 【行】执行本行语句，推进功能链中的当前步骤
    a.click() // 【行】执行本行语句，推进功能链中的当前步骤
    URL.revokeObjectURL(url) // 【行】执行本行语句，推进功能链中的当前步骤
  }) // 【行】执行本行语句，推进功能链中的当前步骤
}
function handleExportCommand(command) { // 【行】进入代码块
  let type = command // 【行】声明并赋值变量 `type`
  if (command === 'current') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    if (statAdminView.value === 'peak') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
      type = 'peak' // 【行】执行本行语句，推进功能链中的当前步骤
    } else if (statAdminView.value === 'share') { // 【行】进入代码块
      type = 'usage' // 【行】执行本行语句，推进功能链中的当前步骤
    } else { // statAdminView === 'usage' // 【行】执行本行语句，推进功能链中的当前步骤
      const trend = adminStatsReport.value?.trend || [] // 【行】声明并赋值变量 `trend`
      type = trend.length ? 'reservation' : 'usage' // 【行】执行本行语句，推进功能链中的当前步骤
    }
  }
  downloadReport(type) // 【行】执行本行语句，推进功能链中的当前步骤
}
/** 【F5-1·学习统计】功能链实例：小明打开学习统计，切换当期/往期与日报~年报，查看累计学习时长柱图 本处职责：drawStudentChart 用 ECharts 渲染学习时长柱状图 */
function drawStudentChart() { // 【行】根据最新 studyBars 重绘 ECharts 柱图
  nextTick(() => { // 【行】进入代码块
    const el = studentChart.value // 【行】声明并赋值变量 `el`
    if (!el) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
    const bars = studyBars.value // 【行】声明并赋值变量 `bars`
    echarts.init(el).setOption({ // 【行】进入代码块
      tooltip: hourTooltip(), // 【行】执行本行语句，推进功能链中的当前步骤
      xAxis: { type: 'category', name: statPeriod.value === 'year' ? '月份' : '日期', data: bars.map(b => b.label) }, // 【行】执行本行语句，推进功能链中的当前步骤
      yAxis: hourYAxis(), // 【行】执行本行语句，推进功能链中的当前步骤
      series: [{ name: '学习时长', type: 'bar', data: bars.map(b => Number(b.value || 0)), itemStyle: { color: '#5f73fb' } }] // 【行】执行本行语句，推进功能链中的当前步骤
    }) // 【行】执行本行语句，推进功能链中的当前步骤
  }) // 【行】执行本行语句，推进功能链中的当前步骤
}
function drawUsageChart() { // 【行】进入代码块
  if (!usageChart.value) return // 【行】条件不满足时提前结束，避免无效请求或错误状态
  const chart = echarts.init(usageChart.value) // 【行】声明并赋值变量 `chart`
  const periodLabel = adminStatsReport.value.summary?.periodLabel || '今日' // 【行】声明并赋值变量 `periodLabel`
  if (statAdminView.value === 'peak') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    const data = adminStatsReport.value.peak || [] // 【行】声明并赋值变量 `data`
    chart.setOption({ // 【行】进入代码块
      tooltip: countTooltip(), // 【行】执行本行语句，推进功能链中的当前步骤
      title: { text: `${periodLabel}高峰时段`, left: 'center', textStyle: { fontSize: 14 } }, // 【行】执行本行语句，推进功能链中的当前步骤
      xAxis: { type: 'category', name: '时段', data: data.map(x => peakAxisLabel(x)) }, // 【行】执行本行语句，推进功能链中的当前步骤
      yAxis: countYAxis('预约次数（次）'), // 【行】执行本行语句，推进功能链中的当前步骤
      series: [{ name: '预约数', type: 'bar', data: data.map(x => statCount(x)), itemStyle: { color: '#4f6ef7' } }] // 【行】执行本行语句，推进功能链中的当前步骤
    }, true) // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  const data = adminStatsReport.value.usage || [] // 【行】声明并赋值变量 `data`
  if (statAdminView.value === 'share') { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    chart.setOption({ // 【行】进入代码块
      tooltip: { trigger: 'item', formatter: '{b}<br/>预约 {c} 次（{d}%）' }, // 【行】执行本行语句，推进功能链中的当前步骤
      title: { text: `${periodLabel}自习室预约占比`, left: 'center', textStyle: { fontSize: 14 } }, // 【行】执行本行语句，推进功能链中的当前步骤
      series: [{ name: '预约占比', type: 'pie', radius: '70%', data: data.map(x => ({ name: x.roomName, value: x.reservationCount || x.usageRate })) }] // 【行】执行本行语句，推进功能链中的当前步骤
    }, true) // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  const trend = adminStatsReport.value.trend || [] // 【行】声明并赋值变量 `trend`
  if (trend.length) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
    chart.setOption({ // 【行】进入代码块
      tooltip: countTooltip(), // 【行】执行本行语句，推进功能链中的当前步骤
      title: { text: `${periodLabel}预约趋势`, left: 'center', textStyle: { fontSize: 14 } }, // 【行】执行本行语句，推进功能链中的当前步骤
      xAxis: { type: 'category', name: trendXAxisName(), data: trend.map(x => trendAxisLabel(x)) }, // 【行】执行本行语句，推进功能链中的当前步骤
      yAxis: countYAxis(), // 【行】执行本行语句，推进功能链中的当前步骤
      series: [{ name: '预约数', type: 'line', smooth: true, data: trend.map(x => statCount(x)), itemStyle: { color: '#6c5ce7' } }] // 【行】执行本行语句，推进功能链中的当前步骤
    }, true) // 【行】执行本行语句，推进功能链中的当前步骤
    return // 【行】执行本行语句，推进功能链中的当前步骤
  }
  chart.setOption({ // 【行】进入代码块
    tooltip: { trigger: 'axis', valueFormatter: (v) => `${v}%` }, // 【行】执行本行语句，推进功能链中的当前步骤
    title: { text: `${periodLabel}各自习室使用率`, left: 'center', textStyle: { fontSize: 14 } }, // 【行】执行本行语句，推进功能链中的当前步骤
    xAxis: { type: 'category', name: '自习室', data: data.map(x => x.roomName) }, // 【行】执行本行语句，推进功能链中的当前步骤
    yAxis: percentYAxis(), // 【行】执行本行语句，推进功能链中的当前步骤
    series: [{ name: '使用率', type: 'bar', data: data.map(x => x.usageRate), itemStyle: { color: '#6c5ce7' } }] // 【行】执行本行语句，推进功能链中的当前步骤
  }, true) // 【行】执行本行语句，推进功能链中的当前步骤
}
async function switchStatAdminView(view) { // 【行】进入代码块
  statAdminView.value = view // 【行】执行本行语句，推进功能链中的当前步骤
  await nextTick() // 【行】执行本行语句，推进功能链中的当前步骤
  drawUsageChart() // 【行】执行本行语句，推进功能链中的当前步骤
}

const ReservationCard = defineComponent({ // 【行】声明并赋值变量 `ReservationCard`
  props: { item: Object, statusText: Function }, // 【行】执行本行语句，推进功能链中的当前步骤
  emits: ['cancel'], // 【行】执行本行语句，推进功能链中的当前步骤
  setup(props, { emit }) { // 【行】进入代码块
    return () => h('article', { class: 'card reservation-card' }, [ // 【行】返回本函数计算结果给调用方
      h('div', [ // 【行】执行本行语句，推进功能链中的当前步骤
        h('strong', props.item.roomName || props.item.room), // 【行】执行本行语句，推进功能链中的当前步骤
        h('p', `${props.item.reserve_date || props.item.date} · ${String(props.item.start_time || '').slice(0, 5)}-${String(props.item.end_time || '').slice(0, 5)}`), // 【行】执行本行语句，推进功能链中的当前步骤
        h('span', { class: `reservation-status ${reservationStatusClass(props.item.status)}` }, props.statusText ? props.statusText(props.item.status) : props.item.status) // 【行】执行本行语句，推进功能链中的当前步骤
      ]), // 【行】执行本行语句，推进功能链中的当前步骤
      h('span', { class: 'seat-left' }, props.item.seatNo || props.item.seat), // 【行】执行本行语句，推进功能链中的当前步骤
      isPendingReservation(props.item.status) ? h('button', { class: 'mini-btn', onClick: () => emit('cancel') }, '取消') : null // 【行】执行本行语句，推进功能链中的当前步骤
    ]) // 【行】执行本行语句，推进功能链中的当前步骤
  }
}) // 【行】执行本行语句，推进功能链中的当前步骤
const FeedbackBox = defineComponent({ // 【行】声明并赋值变量 `FeedbackBox`
  emits: ['submit'], // 【行】执行本行语句，推进功能链中的当前步骤
  setup(_, { emit }) { // 【行】进入代码块
    const content = ref('') // 【行】声明并赋值变量 `content`
    const severity = ref('中') // 【行】声明并赋值变量 `severity`
    const severityOptions = [ // 【行】声明并赋值变量 `severityOptions`
      { value: '低', label: '低' }, // 【行】执行本行语句，推进功能链中的当前步骤
      { value: '中', label: '中' }, // 【行】执行本行语句，推进功能链中的当前步骤
      { value: '高', label: '高' }, // 【行】执行本行语句，推进功能链中的当前步骤
      { value: '紧急', label: '紧急' }
    ] // 【行】执行本行语句，推进功能链中的当前步骤
    return () => h('div', { class: 'card feedback-box' }, [ // 【行】返回本函数计算结果给调用方
      h('strong', '问题反馈'), // 【行】执行本行语句，推进功能链中的当前步骤
      h('label', { class: 'feedback-severity-label' }, '严重程度'), // 【行】执行本行语句，推进功能链中的当前步骤
      h('select', { // 【行】进入代码块
        class: 'input', // 【行】执行本行语句，推进功能链中的当前步骤
        value: severity.value, // 【行】执行本行语句，推进功能链中的当前步骤
        onChange: e => { severity.value = e.target.value }
      }, severityOptions.map(opt => h('option', { value: opt.value }, `${opt.label} — ${opt.value === '低' ? '一般建议' : opt.value === '中' ? '影响使用' : opt.value === '高' ? '较严重' : '需立即处理'}`))), // 【行】执行本行语句，推进功能链中的当前步骤
      h('textarea', { placeholder: '描述遇到的问题或建议', value: content.value, onInput: e => { content.value = e.target.value } }), // 【行】执行本行语句，推进功能链中的当前步骤
      h('button', { // 【行】进入代码块
        class: 'primary-action small', // 【行】执行本行语句，推进功能链中的当前步骤
        onClick: () => { // 【行】进入代码块
          if (content.value.trim()) { // 【行】分支判断：根据当前 UI 状态决定后续逻辑
            emit('submit', { content: content.value, severity: severity.value })
            content.value = ''
            severity.value = '中'
          }
        }
      }, '提交反馈')
    ])
  }
})
const DataTable = defineComponent({
  props: { rows: Array, columns: Array, columnLabels: { type: Object, default: () => ADMIN_COLUMN_LABELS }, emptyText: { type: String, default: '暂无数据' } },
  setup(props, { slots }) {
    const label = c => props.columnLabels[c] || c
    const cell = (c, row) => formatAdminCell(c, row[c], row)
    return () => h('div', { class: 'table-wrap' }, [
      !(props.rows || []).length ? h('p', { class: 'muted table-empty' }, props.emptyText) : null,
      h('table', [
        h('thead', h('tr', [...props.columns.map(c => h('th', label(c))), slots.actions ? h('th', '操作') : null].filter(Boolean))),
        h('tbody', (props.rows || []).map(row => h('tr', [
          ...props.columns.map(c => h('td', cell(c, row))),
          slots.actions ? h('td', slots.actions({ row })) : null
        ].filter(Boolean))))
      ])
    ])
  }
})
const AdminPager = defineComponent({
  name: 'AdminPager',
  props: {
    page: { type: Number, required: true },
    total: { type: Number, required: true },
    count: { type: Number, default: 0 },
    pageSize: { type: Number, default: DEFAULT_ADMIN_PAGE_SIZE },
    pageSizeOptions: { type: Array, default: () => ADMIN_PAGE_SIZE_OPTIONS }
  },
  emits: ['update:page', 'update:pageSize'],
  setup(props, { emit }) {
    const clampPage = value => Math.min(Math.max(1, Math.trunc(Number(value) || 1)), props.total)
    const emitPage = value => { emit('update:page', clampPage(value)) }
    const changePageSize = event => {
      emit('update:pageSize', normalizePageSize(event.target.value))
      emit('update:page', 1)
    }
    return () => {
      if (!props.count) return null
      const currentPage = clampPage(props.page)
      const pageSize = normalizePageSize(props.pageSize)
      return h('div', { class: 'admin-pager-wrap' }, [
        h('div', { class: 'admin-pager' }, [
          h('button', {
            type: 'button',
            class: 'admin-pager-btn',
            disabled: currentPage <= 1,
            onClick: () => emitPage(currentPage - 1)
          }, '上一页'),
          h('label', { class: 'admin-pager-jump' }, [
            h('span', '第'),
            h('input', {
              class: 'admin-pager-input',
              type: 'number',
              min: '1',
              max: String(props.total),
              value: currentPage,
              'aria-label': '输入页码',
              onChange: event => emitPage(event.target.value),
              onKeydown: event => {
                if (event.key === 'Enter') emitPage(event.target.value)
              }
            }),
            h('span', `/ ${props.total} 页`)
          ]),
          h('label', { class: 'admin-pager-size' }, [
            h('span', '每页'),
            h('select', {
              class: 'admin-pager-select',
              value: pageSize,
              'aria-label': '选择每页条数',
              onChange: changePageSize
            }, props.pageSizeOptions.map(size => h('option', { value: size }, `${size} 条`)))
          ]),
          h('button', {
            type: 'button',
            class: 'admin-pager-btn',
            disabled: currentPage >= props.total,
            onClick: () => emitPage(currentPage + 1)
          }, '下一页')
        ]),
        h('p', { class: 'admin-pager-meta scanner-hint' }, `共 ${props.count} 条 · 第 ${currentPage}/${props.total} 页 · 每页 ${pageSize} 条`)
      ])
    }
  }
})

const closeProfileMenu = () => { adminProfileMenuOpen.value = false }
window.addEventListener('resize', () => { width.value = window.innerWidth })
onMounted(() => {
  try {
    const saved = JSON.parse(localStorage.getItem('notifyPrefs') || '{}')
    Object.assign(notifyPrefs, saved)
  } catch (e) { /* ignore */ }
  studyTimerHandle = setInterval(updateStudyTimer, 1000)
  bootstrap()
  window.addEventListener('click', closeProfileMenu)
})
watch(studentPage, (page) => {
  if (page === 'checkin') {
    startCheckinPagePoll()
    refreshCheckinQr()
  } else {
    stopCheckinPagePoll()
    checkinQrSvg.value = ''
  }
}, { immediate: true })
watch([activeReservation, studentNoDisplay], () => {
  if (studentPage.value === 'checkin' && isPendingReservation(activeReservation.value?.status)) {
    refreshCheckinQr()
  } else if (!isPendingReservation(activeReservation.value?.status)) {
    checkinQrSvg.value = ''
  }
})
watch([adminKeyword, adminStatusFilter], () => { adminAccountPage.value = 1 })
watch([reservationKeyword, reservationStatusFilter, reservationRoomFilter], () => { reservationPage.value = 1 })
watch([checkinKeyword, checkinResultFilter], () => { checkinPage.value = 1 })
watch(decoratedLiveReservations, () => { liveReservationPage.value = 1 })
watch([feedbackKeyword, feedbackStatusFilter], () => { feedbackPage.value = 1 })
watch([logKeyword, logModuleFilter], () => { logPage.value = 1 })
watch([roomKeyword, roomStatusFilter], () => { roomPage.value = 1 })
watch(announcementKeyword, () => { announcementPage.value = 1 })
watch(users, () => { userPage.value = 1 })
onBeforeUnmount(() => {
  stopCheckinPagePoll()
  if (studyTimerHandle) clearInterval(studyTimerHandle)
  window.removeEventListener('click', closeProfileMenu)
})
</script>
