# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level code architecture and structure

This is a monolithic Java-based payment system built with Spring Boot and Maven. It is designed to be a lightweight and easy-to-use payment collection system for Internet business systems.

The project is divided into several modules:

*   `roncoo-pay-common-core`: Common basic module, including common tool classes, enumerations, configurations, basic entities, basic DAO layer, etc.
*   `roncoo-pay-service`: The core of the entire system, the implementation of all business functions (ordering, query, account operation...), all web projects and app services need to refer to this module.
*   `roncoo-pay-web-boss`: The operation background module provides configuration and maintenance of the payment system functions, such as maintaining bank information, payment products, merchant information, rates, transaction query, etc.
*   `roncoo-pay-web-gateway`: The payment gateway module provides external gateway payment interfaces for merchants (including payment order placement, payment query...).
*   `roncoo-pay-web-merchant`: The merchant background module provides merchants with viewing transaction order information.
*   `roncoo-pay-web-sample-shop`: The simulated mall module provides a mall that initiates payment requests to the payment system and provides test methods.
*   `roncoo-pay-app-notify`: The merchant notification module notifies the corresponding merchant of the successfully traded order information according to a certain notification strategy.
*   `roncoo-pay-app-order-polling`: The order polling module queries the results of the orders in the platform payment according to the established query strategy, and then performs corresponding processing on the obtained order results.
*   `roncoo-pay-app-reconciliation`: The transaction reconciliation module regularly matches and verifies the transaction orders of the previous day's platform and the bank's (for example: WeChat, Alipay...) orders, and verifies the order status, handling fees, transaction amount, etc.
*   `roncoo-pay-app-settlement`: The transaction settlement module regularly settles the transaction orders that have been confirmed after the previous day's reconciliation, and settles the money to the corresponding merchants and platforms.

## Common commands

*   **Build the project**: `mvn clean install`
*   **Run a module**: `cd <module-name>` and then `mvn spring-boot:run`
*   **Run tests**: `mvn test`
