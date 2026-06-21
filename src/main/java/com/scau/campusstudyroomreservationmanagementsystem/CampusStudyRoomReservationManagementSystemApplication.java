package com.scau.campusstudyroomreservationmanagementsystem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * 【F1-1·步骤3】实例：Spring Boot 启动后 8080 托管 static 登录页与 /api
 */
@SpringBootApplication
@EnableScheduling
public class CampusStudyRoomReservationManagementSystemApplication {

    public static void main(String[] args) {
        SpringApplication.run(CampusStudyRoomReservationManagementSystemApplication.class, args);
    }

}
