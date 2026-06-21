package com.scau.campusstudyroomreservationmanagementsystem.support;

/**
 * 【F1-2·JSON】实例：小明点确认后收到 {"code":200,"message":"success","data":{...}}
 */
public record ApiResponse<T>(int code, String message, T data) {
    /** 【F2-1·步骤7】实例：登录成功 code=200，data 含 token */
    public static <T> ApiResponse<T> ok(T data) {
        return new ApiResponse<>(200, "success", data);
    }

    public static <T> ApiResponse<T> fail(int code, String message) {
        return new ApiResponse<>(code, message, null);
    }
}
