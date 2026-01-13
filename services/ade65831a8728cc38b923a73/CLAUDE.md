# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## High-level architecture

`openvpn-monitor` is a Flask application that displays the status of OpenVPN servers by connecting to the OpenVPN management console. The frontend is built with JavaScript and CSS, and the backend is written in Python. The application can be deployed in various ways, including with Apache, Nginx, or Docker.

## Common development tasks

### Setting up the development environment

1.  Clone the repository:
    ```bash
    git clone https://github.com/furlongm/openvpn-monitor
    cd openvpn-monitor
    ```

2.  Create a Python virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    . .venv/bin/activate
    ```

3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  Install the JavaScript dependencies:
    ```bash
    yarnpkg --prod --modules-folder openvpn_monitor/static/dist install
    ```

### Running the development server

To run the Flask development server in debug mode:

```bash
flask --app openvpn_monitor/app run --debug
```

### Running the tests

The tests are run against a mock OpenVPN management server. To run the tests:

1.  Start the mock server in a separate terminal:
    ```bash
    python3 tests/listen.py
    ```

2.  Run the application, which will connect to the mock server.

