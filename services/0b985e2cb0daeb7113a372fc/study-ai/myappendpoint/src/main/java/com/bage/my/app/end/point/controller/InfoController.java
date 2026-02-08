package com.bage.my.app.end.point.controller;

import com.bage.my.app.end.point.entity.ApiResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@Slf4j
public class InfoController {

    @GetMapping("/")
    public ApiResponse<Map<String, Object>> root() {
        Map<String, Object> data = new HashMap<>();
        data.put("status", "UP");
        data.put("service", "myappendpoint");
        data.put("timestamp", LocalDateTime.now().toString());
        data.put("version", "1.0.0");
        return new ApiResponse<>(200, "OK", data);
    }

    @GetMapping("/info")
    public ApiResponse<Map<String, Object>> info() {
        Map<String, Object> data = new HashMap<>();
        data.put("status", "UP");
        data.put("service", "myappendpoint");
        data.put("timestamp", LocalDateTime.now().toString());
        data.put("version", "1.0.0");
        return new ApiResponse<>(200, "OK", data);
    }
}