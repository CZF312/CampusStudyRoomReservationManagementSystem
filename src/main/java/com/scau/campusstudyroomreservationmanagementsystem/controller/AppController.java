package com.scau.campusstudyroomreservationmanagementsystem.controller;

import com.scau.campusstudyroomreservationmanagementsystem.service.AppService;
import com.scau.campusstudyroomreservationmanagementsystem.support.ApiResponse;
import com.scau.campusstudyroomreservationmanagementsystem.support.CurrentUser;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;

/**
 * 【F1-2·REST API】实例：小明确认预约 POST /api/reservations 由此类接收并转发 Service
 * REST 接口层：全部 /api 路径入口。
 * 理解/答辩文档：docs/09-理解与讲解/01-项目理解指南.md · 02-答辩讲解手册.md
 */
@RestController
@RequestMapping("/api")
public class AppController {
    private final AppService app;

    public AppController(AppService app) {
        this.app = app;
    }

    // —— 认证与账号：F2-3 / F2-1 / F2-2 ——

    /** 【F2-3·步骤2】实例：小李 POST 注册，写入待审核账号与 credit=300 */
    @PostMapping("/auth/register")
    public ApiResponse<Map<String, Object>> register(@RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.register(req));
    }

    /** 【F2-1·步骤3】实例：小明 POST /auth/login，转发至 loginStudent */
    @PostMapping("/auth/login")
    public ApiResponse<Map<String, Object>> login(@RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.loginStudent(req));
    }

    /** 【F2-2·步骤3】实例：admin 登录，转发至 loginAdmin */
    @PostMapping("/admin/auth/login")
    public ApiResponse<Map<String, Object>> adminLogin(@RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.loginAdmin(req));
    }

    /** 【F2-1·步骤8b】实例：bootstrap 刷新后 GET /auth/me 恢复小明或 admin 会话信息 */
    @GetMapping("/auth/me")
    public ApiResponse<Map<String, Object>> me(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(user.isStudent() ? app.studentInfo(user) : app.adminInfo(user));
    }

    /** 【F2-4·步骤1】实例：小明改密码 POST /auth/change-password */
    @PostMapping("/auth/change-password")
    public ApiResponse<Void> changePassword(@AuthenticationPrincipal CurrentUser user,
                                            @RequestBody Map<String, Object> req) {
        app.changePassword(user, req);
        return ApiResponse.ok(null);
    }

    @GetMapping("/student/profile")
    public ApiResponse<Map<String, Object>> profile(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.studentInfo(user));
    }

    /** 【F2-4·步骤2】实例：小明 PUT /student/profile 更新资料 */
    @PutMapping("/student/profile")
    public ApiResponse<Map<String, Object>> updateProfile(@AuthenticationPrincipal CurrentUser user,
                                                           @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.updateProfile(user, req));
    }

    // —— 自习室与预约：F3-1 / F3-2 ——

    /** 【F3-1·步骤1b】实例：小明打开预约页，GET /api/rooms 拉自习室列表 */
    @GetMapping("/rooms")
    public ApiResponse<List<Map<String, Object>>> rooms(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.rooms(user));
    }

    @GetMapping("/rooms/{id}")
    public ApiResponse<Map<String, Object>> room(@PathVariable Long id) {
        return ApiResponse.ok(app.room(id));
    }

    @GetMapping("/rooms/{id}/seats")
    public ApiResponse<List<Map<String, Object>>> roomSeats(@PathVariable Long id) {
        return ApiResponse.ok(app.seats(id));
    }

    /** 【F3-1·步骤3】实例：小明选 14:00–16:00，查 A 自习室未被 slot 占用的绿色座位 */
    @GetMapping("/seats/available")
    public ApiResponse<List<Map<String, Object>>> availableSeats(@RequestParam Long roomId,
                                                                  @RequestParam String date,
                                                                  @RequestParam String startTime,
                                                                  @RequestParam String endTime) {
        return ApiResponse.ok(app.availableSeats(roomId, date, startTime, endTime));
    }

    /** 【F3-1·步骤4】实例：小明确认 A-12 后 POST，转发 createReservation */
    @PostMapping("/reservations")
    public ApiResponse<Map<String, Object>> createReservation(@AuthenticationPrincipal CurrentUser user,
                                                               @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.createReservation(user, req));
    }

    /** 【F3-3·步骤2b】实例：小明「我的预约」GET /reservations/my */
    @GetMapping("/reservations/my")
    public ApiResponse<List<Map<String, Object>>> myReservations(@AuthenticationPrincipal CurrentUser user,
                                                                  @RequestParam(required = false) String status,
                                                                  @RequestParam(required = false) Boolean today) {
        return ApiResponse.ok(app.myReservations(user, status, today));
    }

    @GetMapping("/reservations/{id}")
    public ApiResponse<Map<String, Object>> reservation(@PathVariable Long id) {
        return ApiResponse.ok(app.reservationDetail(id));
    }

    /** 【F3-2·步骤1】实例：小明取消「待使用」预约，转发 cancelReservation */
    @PostMapping("/reservations/{id}/cancel")
    public ApiResponse<Void> cancel(@AuthenticationPrincipal CurrentUser user, @PathVariable Long id) {
        app.cancelReservation(user, id);
        return ApiResponse.ok(null);
    }

    // —— 签到签退：F4-1 / F4-2 ——

    /** 后端 60 秒 token 二维码（当前前端未调用，学生页用本地学号 QR） */
    @GetMapping("/checkin/qrcode")
    public ApiResponse<Map<String, Object>> qr(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.qrCode(user));
    }

    /** 【F4-2·步骤2】实例：小明 POST 签退，转发 checkout */
    @PostMapping("/reservations/{id}/checkout")
    public ApiResponse<Map<String, Object>> checkout(@AuthenticationPrincipal CurrentUser user, @PathVariable Long id) {
        return ApiResponse.ok(app.checkout(user, id));
    }

    /** 【F4-2·步骤4】实例：小明签退后查 credit_log 流水与当前积分 */
    @GetMapping("/credits/my")
    public ApiResponse<Map<String, Object>> credit(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.credit(user));
    }

    /** 【F5-1·步骤2b】实例：小明打开学习统计，GET 按周/月聚合学习时长 */
    @GetMapping("/statistics/my-study-duration")
    public ApiResponse<Map<String, Object>> myStudyDuration(@AuthenticationPrincipal CurrentUser user,
                                                             @RequestParam(required = false) String period) {
        return ApiResponse.ok(app.myStudyDuration(user, period));
    }

    @GetMapping("/announcements")
    public ApiResponse<List<Map<String, Object>>> announcements() {
        return ApiResponse.ok(app.announcements());
    }

    @PostMapping("/announcements/{id}/read")
    public ApiResponse<Void> readAnnouncement(@PathVariable Long id) {
        app.readAnnouncement(id);
        return ApiResponse.ok(null);
    }

    @GetMapping("/notifications")
    public ApiResponse<List<Map<String, Object>>> notifications(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.notifications(user));
    }

    @PostMapping("/notifications/{id}/read")
    public ApiResponse<Void> readNotification(@AuthenticationPrincipal CurrentUser user, @PathVariable Long id) {
        app.readNotification(user, id);
        return ApiResponse.ok(null);
    }

    @PostMapping("/notifications/read-all")
    public ApiResponse<Void> readAllNotifications(@AuthenticationPrincipal CurrentUser user) {
        app.readAllNotifications(user);
        return ApiResponse.ok(null);
    }

    @PostMapping("/feedback")
    public ApiResponse<Map<String, Object>> feedback(@AuthenticationPrincipal CurrentUser user,
                                                      @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.createFeedback(user, req));
    }

    @GetMapping("/feedback/my")
    public ApiResponse<List<Map<String, Object>>> myFeedback(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.myFeedback(user));
    }

    @GetMapping("/admin/dashboard")
    public ApiResponse<Map<String, Object>> dashboard(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.dashboard(user));
    }

    /** 【F6-6·步骤2b】实例：签到页 GET /admin/live-reservations */
    @GetMapping("/admin/live-reservations")
    public ApiResponse<List<Map<String, Object>>> liveReservations(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.liveReservations(user));
    }

    @GetMapping("/admin/users")
    public ApiResponse<List<Map<String, Object>>> users(@RequestParam(required = false) String keyword,
                                                         @RequestParam(required = false) String auditStatus) {
        return ApiResponse.ok(app.adminUsers(keyword, auditStatus));
    }

    @GetMapping("/admin/users/pending")
    public ApiResponse<List<Map<String, Object>>> pendingUsers() {
        return ApiResponse.ok(app.adminUsers(null, "PENDING"));
    }

    @GetMapping("/admin/users/export")
    public ResponseEntity<byte[]> exportUsers(@RequestParam(required = false) String keyword,
                                              @RequestParam(required = false) String auditStatus) {
        byte[] bytes = ("\uFEFF" + app.exportUsersCsv(keyword, auditStatus)).getBytes(StandardCharsets.UTF_8);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=student-users.csv")
                .contentType(new MediaType("text", "csv", StandardCharsets.UTF_8))
                .body(bytes);
    }

    @PostMapping("/admin/users/{id}/approve")
    public ApiResponse<Void> approve(@AuthenticationPrincipal CurrentUser admin, @PathVariable Long id,
                                     @RequestBody(required = false) Map<String, Object> req) {
        app.auditUser(admin, id, true, req == null ? "" : String.valueOf(req.getOrDefault("remark", "")));
        return ApiResponse.ok(null);
    }

    /** 【F6-3·步骤2b】实例：管理员拒绝注册 POST reject，auditUser(approve=false) */
    @PostMapping("/admin/users/{id}/reject")
    public ApiResponse<Void> reject(@AuthenticationPrincipal CurrentUser admin, @PathVariable Long id,
                                    @RequestBody(required = false) Map<String, Object> req) {
        app.auditUser(admin, id, false, req == null ? "资料不符合要求" : String.valueOf(req.getOrDefault("remark", "资料不符合要求")));
        return ApiResponse.ok(null);
    }

    /** 【F6-3·步骤3b】实例：禁用学生账号 POST disable */
    @PostMapping("/admin/users/{id}/disable")
    public ApiResponse<Void> disable(@PathVariable Long id) {
        app.setUserStatus(id, "DISABLED");
        return ApiResponse.ok(null);
    }

    @PostMapping("/admin/users/{id}/enable")
    public ApiResponse<Void> enable(@PathVariable Long id) {
        app.setUserStatus(id, "NORMAL");
        return ApiResponse.ok(null);
    }

    @GetMapping("/admin/rooms")
    public ApiResponse<List<Map<String, Object>>> adminRooms(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.rooms(user));
    }

    @PostMapping("/admin/rooms")
    public ApiResponse<Map<String, Object>> createRoom(@AuthenticationPrincipal CurrentUser user,
                                                        @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.saveRoom(user, null, req));
    }

    @PutMapping("/admin/rooms/{id}")
    public ApiResponse<Map<String, Object>> updateRoom(@AuthenticationPrincipal CurrentUser user,
                                                        @PathVariable Long id,
                                                        @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.saveRoom(user, id, req));
    }

    @DeleteMapping("/admin/rooms/{id}")
    public ApiResponse<Void> deleteRoom(@AuthenticationPrincipal CurrentUser user, @PathVariable Long id) {
        app.deleteRoom(user, id);
        return ApiResponse.ok(null);
    }

    @GetMapping("/admin/rooms/{id}/seats")
    public ApiResponse<List<Map<String, Object>>> adminRoomSeats(@PathVariable Long id) {
        return ApiResponse.ok(app.seats(id));
    }

    @PutMapping("/admin/seats/{id}")
    public ApiResponse<Void> updateSeat(@AuthenticationPrincipal CurrentUser user,
                                      @PathVariable Long id,
                                      @RequestBody Map<String, Object> req) {
        app.updateSeat(user, id, req);
        return ApiResponse.ok(null);
    }

    @PutMapping("/admin/rooms/{id}/seats/batch")
    public ApiResponse<Void> batchSeats(@AuthenticationPrincipal CurrentUser user,
                                        @PathVariable Long id,
                                        @RequestBody Map<String, Object> req) {
        app.batchSeats(user, id, req);
        return ApiResponse.ok(null);
    }

    @PostMapping("/admin/rooms/{roomId}/seats")
    public ApiResponse<Map<String, Object>> createSeat(@AuthenticationPrincipal CurrentUser user,
                                                      @PathVariable Long roomId) {
        return ApiResponse.ok(app.addSeat(user, roomId));
    }

    @DeleteMapping("/admin/seats/{id}")
    public ApiResponse<Void> deleteSeat(@AuthenticationPrincipal CurrentUser user, @PathVariable Long id) {
        app.deleteSeat(user, id);
        return ApiResponse.ok(null);
    }

    @GetMapping("/admin/reservations")
    public ApiResponse<List<Map<String, Object>>> adminReservations(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.adminReservations(user));
    }

    /** 【F6-5·步骤2b】实例：撤销违约 POST /admin/reservations/{id}/revoke-violation */
    @PostMapping("/admin/reservations/{id}/revoke-violation")
    public ApiResponse<Map<String, Object>> revokeViolation(@AuthenticationPrincipal CurrentUser user,
                                                             @PathVariable Long id,
                                                             @RequestBody(required = false) Map<String, Object> req) {
        String remark = req == null ? "" : String.valueOf(req.getOrDefault("remark", ""));
        return ApiResponse.ok(app.revokeViolation(user, id, remark));
    }

    /** 【F4-1·步骤4】实例：管理员扫小明学号，转发 scanCheckin */
    @PostMapping("/admin/checkin/scan")
    public ApiResponse<Map<String, Object>> scan(@AuthenticationPrincipal CurrentUser user,
                                                  @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.scanCheckin(user, req));
    }

    @GetMapping("/admin/checkins")
    public ApiResponse<List<Map<String, Object>>> checkins(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.checkins(user));
    }

    @GetMapping("/admin/announcements")
    public ApiResponse<List<Map<String, Object>>> adminAnnouncements() {
        return ApiResponse.ok(app.announcements());
    }

    @PostMapping("/admin/announcements")
    public ApiResponse<Map<String, Object>> createAnnouncement(@AuthenticationPrincipal CurrentUser user,
                                                                @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.saveAnnouncement(user, null, req));
    }

    @PutMapping("/admin/announcements/{id}")
    public ApiResponse<Map<String, Object>> updateAnnouncement(@AuthenticationPrincipal CurrentUser user,
                                                                @PathVariable Long id,
                                                                @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.saveAnnouncement(user, id, req));
    }

    @DeleteMapping("/admin/announcements/{id}")
    public ApiResponse<Void> deleteAnnouncement(@PathVariable Long id) {
        app.deleteAnnouncement(id);
        return ApiResponse.ok(null);
    }

    @GetMapping("/admin/statistics/usage")
    public ApiResponse<List<Map<String, Object>>> usage(@AuthenticationPrincipal CurrentUser user,
                                                          @RequestParam(defaultValue = "day") String period,
                                                          @RequestParam(required = false) Long roomId,
                                                          @RequestParam(defaultValue = "current") String rangeMode,
                                                          @RequestParam(required = false) String startDate,
                                                          @RequestParam(required = false) String endDate) {
        return ApiResponse.ok(app.statisticsUsage(user, period, roomId, rangeMode, startDate, endDate));
    }

    /** 【F6-1·步骤2c】实例：管理员统计页切换「高峰分析」GET /admin/statistics/peak */
    @GetMapping("/admin/statistics/peak")
    public ApiResponse<List<Map<String, Object>>> peak(@AuthenticationPrincipal CurrentUser user,
                                                        @RequestParam(defaultValue = "day") String period,
                                                        @RequestParam(required = false) Long roomId,
                                                        @RequestParam(defaultValue = "current") String rangeMode,
                                                        @RequestParam(required = false) String startDate,
                                                        @RequestParam(required = false) String endDate) {
        return ApiResponse.ok(app.statisticsPeak(user, period, roomId, rangeMode, startDate, endDate));
    }

    @GetMapping("/admin/statistics/report")
    public ApiResponse<Map<String, Object>> statisticsReport(@AuthenticationPrincipal CurrentUser user,
                                                              @RequestParam(defaultValue = "day") String period,
                                                              @RequestParam(required = false) Long roomId,
                                                              @RequestParam(defaultValue = "current") String rangeMode,
                                                              @RequestParam(required = false) String startDate,
                                                              @RequestParam(required = false) String endDate) {
        return ApiResponse.ok(app.statisticsReport(user, period, roomId, rangeMode, startDate, endDate));
    }

    @GetMapping("/admin/statistics/credit")
    public ApiResponse<List<Map<String, Object>>> creditStats() {
        return ApiResponse.ok(app.statisticsCredit());
    }

    @GetMapping("/admin/statistics/export")
    public ResponseEntity<byte[]> export(@AuthenticationPrincipal CurrentUser user,
                                         @RequestParam(defaultValue = "day") String period,
                                         @RequestParam(required = false) Long roomId,
                                         @RequestParam(defaultValue = "current") String rangeMode,
                                         @RequestParam(defaultValue = "usage") String reportType,
                                         @RequestParam(required = false) String startDate,
                                         @RequestParam(required = false) String endDate) {
        byte[] bytes = ("\uFEFF" + app.exportCsv(user, period, roomId, rangeMode, startDate, endDate, reportType)).getBytes(StandardCharsets.UTF_8);
        String filename = app.statisticsExportFilename(reportType);
        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=" + filename)
                .contentType(new MediaType("text", "csv", StandardCharsets.UTF_8))
                .body(bytes);
    }

    @GetMapping("/admin/feedback")
    public ApiResponse<List<Map<String, Object>>> adminFeedback(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.adminFeedback(user));
    }

    @PutMapping("/admin/feedback/{id}")
    public ApiResponse<Void> handleFeedback(@AuthenticationPrincipal CurrentUser user,
                                             @PathVariable Long id,
                                             @RequestBody Map<String, Object> req) {
        app.handleFeedback(user, id, req);
        return ApiResponse.ok(null);
    }

    @GetMapping("/admin/settings/config")
    public ApiResponse<Map<String, String>> getSystemConfig(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.getSystemConfig(user));
    }

    @PostMapping("/admin/settings/config")
    public ApiResponse<Void> updateSystemConfig(@AuthenticationPrincipal CurrentUser user,
                                                @RequestBody Map<String, String> req) {
        app.updateSystemConfig(user, req);
        return ApiResponse.ok(null);
    }

    /** 【F6-7·步骤2b】实例：superadmin GET /admin/operation-logs */
    @GetMapping("/admin/operation-logs")
    public ApiResponse<List<Map<String, Object>>> operationLogs(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.operationLogs(user));
    }

    @GetMapping("/admin/admins")
    public ApiResponse<List<Map<String, Object>>> adminAccounts(@AuthenticationPrincipal CurrentUser user) {
        return ApiResponse.ok(app.adminAccounts(user));
    }

    @PostMapping("/admin/admins")
    public ApiResponse<Map<String, Object>> createAdmin(@AuthenticationPrincipal CurrentUser user,
                                                        @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.createAdminAccount(user, req));
    }

    @PutMapping("/admin/admins/{id}")
    public ApiResponse<Map<String, Object>> updateAdmin(@AuthenticationPrincipal CurrentUser user,
                                                        @PathVariable Long id,
                                                        @RequestBody Map<String, Object> req) {
        return ApiResponse.ok(app.updateAdminAccount(user, id, req));
    }

    @PostMapping("/admin/admins/{id}/disable")
    public ApiResponse<Void> disableAdmin(@AuthenticationPrincipal CurrentUser user, @PathVariable Long id) {
        app.setAdminAccountStatus(user, id, "DISABLED");
        return ApiResponse.ok(null);
    }

    @PostMapping("/admin/admins/{id}/enable")
    public ApiResponse<Void> enableAdmin(@AuthenticationPrincipal CurrentUser user, @PathVariable Long id) {
        app.setAdminAccountStatus(user, id, "NORMAL");
        return ApiResponse.ok(null);
    }
}
