# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

- **Build the project:**
  ```bash
  make all
  ```

- **Run the test server:**
  ```bash
  make test_server
  ```

## Architecture

`sockjs-tornado` is a Python server-side implementation of the SockJS protocol, built on top of the Tornado web framework. It provides a WebSocket-like API for real-time communication between a browser and a server.

The core components of the library are located in the `sockjs/tornado/` directory:

- **`router.py`**: The `SockJSRouter` class is the main entry point for creating a SockJS server. It routes incoming requests to the appropriate transport handler based on the URL.

- **`conn.py`**: The `SockJSConnection` class is the base class for user-defined connection handlers. It provides methods for sending and receiving messages, and for handling connection events.

- **`session.py` / `sessioncontainer.py`**: These modules manage SockJS sessions. A session is created for each client connection and is responsible for handling messages and timeouts.

- **`transports/`**: This directory contains implementations for the various SockJS transports, such as XHR-polling, XHR-streaming, and WebSockets.

- **`basehandler.py`**: This module provides a base class for the transport handlers, which are responsible for handling the specifics of each transport protocol.
