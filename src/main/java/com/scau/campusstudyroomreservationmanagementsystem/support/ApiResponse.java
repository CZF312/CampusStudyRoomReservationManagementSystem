package com.scau.campusstudyroomreservationmanagementsystem.support;

/**
 * 【F1-2·技术概念】功能链实例：小明点「确认预约」→ 浏览器用 **Vue** 发 **HTTP** **JSON** 到 **REST API** → **Controller** 转 **Service** 写 **MySQL** → 返回 **JSON** `… 本处职责：小明点确认后收到 {"code":200,"message":"success","data":{...}}
 */
public record ApiResponse<T>(int code, String message, T data) { // 【行】进入方法体或分支块
    /** 【F2-1·学生登录】功能链实例：小明在登录页输入 `202225220101` / `123456` → 点「登录」→ 首页显示「你好，小明」→ 再进「我的预约」无需重输密码（`localStorage` 已有 token）。 本处职责：登录成功 code=200，data 含 token*/
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(200, "success", data);
    }

    public static <T> ApiResponse<T> fail(int code, String message) {
        return new ApiResponse<>(code, message, null);
    }
}
