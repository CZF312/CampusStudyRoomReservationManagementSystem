package com.scau.campusstudyroomreservationmanagementsystem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * 【F1-1·环境启动】功能链实例：组长双击 `start.bat` → PowerShell 导入 `database-full.sql` 建库 `study_room_reservation` → Spring Boot 监听 8080 → 浏览器打开登录页 → `… 本处职责：Spring Boot 启动后 8080 托管 static 登录页与 /api
 */
@SpringBootApplication
@EnableScheduling
public class CampusStudyRoomReservationManagementSystemApplication { // 【行】进入方法体或分支块

    public static void main(String[] args) { // 【行】进入方法体或分支块
        SpringApplication.run(CampusStudyRoomReservationManagementSystemApplication.class, args); // 【行】执行本行 Java 语句
    }

}
