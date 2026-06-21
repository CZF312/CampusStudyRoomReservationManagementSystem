package com.scau.campusstudyroomreservationmanagementsystem.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

/**
 * 【F4-3·定时维护】功能链实例：小明约了 14:00 未到馆 → 14:15 后任务把单标「已违约」扣 50 分；若使用中过 `end_time` 未签退则自动签退。 本处职责：每分钟触发四条维护（违约/自动签退等）
 */
@Service
public class ScheduledTaskService { // 【行】进入方法体或分支块
    private static final Logger log = LoggerFactory.getLogger(ScheduledTaskService.class); // 【行】执行本行 Java 语句
    private final AppService appService; // 【行】执行本行 Java 语句

    public ScheduledTaskService(AppService appService) { // 【行】进入方法体或分支块
        this.appService = appService; // 【行】执行本行 Java 语句
    }

    /** 【F4-3·定时维护】功能链实例：小明约了 14:00 未到馆 → 14:15 后任务把单标「已违约」扣 50 分；若使用中过 `end_time` 未签退则自动签退。 本处职责：cron 每分钟依次执行无效签到/违约/自动签退/黑名单解除*/
    @Scheduled(cron = "0 * * * * *")
    public void runMaintenanceTasks() {
        try {
            appService.scheduledProcessInvalidCheckin();
            appService.scheduledProcessNoShow();
            appService.scheduledProcessAutoCheckout();
            appService.scheduledProcessBlacklistRelease();
        } catch (Exception ex) {
            log.warn("定时任务执行异常: {}", ex.getMessage());
        }
    }
}
