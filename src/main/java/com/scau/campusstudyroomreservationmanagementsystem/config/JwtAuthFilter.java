package com.scau.campusstudyroomreservationmanagementsystem.config;

import com.scau.campusstudyroomreservationmanagementsystem.support.CurrentUser;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

/**
 * 【F1-2·技术概念】功能链实例：小明点「确认预约」→ 浏览器用 **Vue** 发 **HTTP** **JSON** 到 **REST API** → **Controller** 转 **Service** 写 **MySQL** → 返回 **JSON** `… 本处职责：小明登录后请求带 Bearer token，此处解析并写入 SecurityContext
 */
@Component
public class JwtAuthFilter extends OncePerRequestFilter { // 【行】进入方法体或分支块
    private final JwtService jwtService; // 【行】执行本行 Java 语句

    public JwtAuthFilter(JwtService jwtService) { // 【行】进入方法体或分支块
        this.jwtService = jwtService; // 【行】执行本行 Java 语句
    }

    @Override
    /** 【F2-1·学生登录】功能链实例：小明在登录页输入 `202225220101` / `123456` → 点「登录」→ 首页显示「你好，小明」→ 再进「我的预约」无需重输密码（`localStorage` 已有 token）。 本处职责：从 Authorization: Bearer 取 token，写入 SecurityContext*/
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        String header = request.getHeader("Authorization");
        if (header != null && header.startsWith("Bearer ")) {
            try {
                CurrentUser user = jwtService.parse(header.substring(7));
                var auth = new UsernamePasswordAuthenticationToken(
                        user,
                        null,
                        List.of(new SimpleGrantedAuthority("ROLE_" + user.role()))
                );
                SecurityContextHolder.getContext().setAuthentication(auth);
            } catch (Exception ignored) {
                SecurityContextHolder.clearContext();
            }
        }
        chain.doFilter(request, response);
    }
}
