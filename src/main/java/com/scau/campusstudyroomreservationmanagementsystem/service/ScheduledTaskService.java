package com.scau.campusstudyroomreservationmanagementsystem.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

/**
 * 【F4-3·步骤0】实例：每分钟触发四条维护（违约/自动签退等）
 */
@Service
public class ScheduledTaskService {
    private static final Logger log = LoggerFactory.getLogger(ScheduledTaskService.class);
    private final AppService appService;

    public ScheduledTaskService(AppService appService) {
        this.appService = appService;
    }

    /** 【F4-3·步骤0–4】实例：cron 每分钟依次执行无效签到/违约/自动签退/黑名单解除 */
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
