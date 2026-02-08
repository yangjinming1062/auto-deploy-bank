package com.impossibl.postgres;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Main entry point for pgjdbc-ng web service.
 */
@SpringBootApplication
@RestController
public class Main {

    public static void main(String[] args) {
        SpringApplication.run(Main.class, args);
    }

    @GetMapping("/")
    public String index() {
        return "pgjdbc-ng - PostgreSQL JDBC Driver\n" +
               "===================================\n" +
               "This is a JDBC driver library. To use it, add the JAR to your classpath.\n" +
               "Maven dependency:\n" +
               "  <dependency>\n" +
               "    <groupId>com.impossibl</groupId>\n" +
               "    <artifactId>pgjdbc-ng</artifactId>\n" +
               "    <version>0.0.1-SNAPSHOT</version>\n" +
               "  </dependency>\n" +
               "\nJDBC URL format: jdbc:postgresql://host:port/database";
    }

    @GetMapping("/health")
    public String health() {
        return "OK";
    }
}