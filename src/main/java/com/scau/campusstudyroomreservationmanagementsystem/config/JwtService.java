package com.scau.campusstudyroomreservationmanagementsystem.config;

import com.scau.campusstudyroomreservationmanagementsystem.support.CurrentUser;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Date;
import java.util.Map;

@Service
public class JwtService {
    private final SecretKey key;
    private final long expireHours;

    public JwtService(@Value("${app.jwt.secret}") String secret,
                      @Value("${app.jwt.expire-hours}") long expireHours) {
        this.key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        this.expireHours = expireHours;
    }

    /** 【F2-1·学生登录】功能链实例：小明在登录页输入 `202225220101` / `123456` → 点「登录」→ 首页显示「你好，小明」→ 再进「我的预约」无需重输密码（`localStorage` 已有 token）。 本处职责：小明/admin 登录成功，签发含 userId/role 的 JWT*/
    public String createToken(CurrentUser user) { // 【行】进入方法体或分支块
        Instant now = Instant.now(); // 【行】执行本行 Java 语句
        return Jwts.builder() // 【行】返回 Service 结果给 Controller，最终序列化为 JSON
                .subject(user.username())
                .claims(Map.of(
                        "userId", user.id(),
                        "role", user.role(),
                        "displayName", user.displayName()
                ))
                .issuedAt(Date.from(now))
                .expiration(Date.from(now.plusSeconds(expireHours * 3600)))
                .signWith(key)
                .compact(); // 【行】执行本行 Java 语句
    }

    public CurrentUser parse(String token) {
        Claims claims = Jwts.parser().verifyWith(key).build().parseSignedClaims(token).getPayload();
        Long userId = ((Number) claims.get("userId")).longValue();
        String role = String.valueOf(claims.get("role"));
        String displayName = String.valueOf(claims.get("displayName"));
        return new CurrentUser(userId, claims.getSubject(), role, displayName);
    }
}
