# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an automated train ticket booking tool for 12306.cn (China Railway). It automates the process of searching for, logging in to, and booking train tickets. The project is currently unmaintained as 12306's queuing/standing-by system now works better than automated tools.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the tool (after configuring configure.py)
python fuckeverything.py
```

## Architecture

### Entry Point
- **`fuckeverything.py`**: Main application with two-thread architecture:
  - `super_hero` thread: Fetches proxy IPs, handles login, queries tickets, submits orders
  - `girl_of_the_night` thread: Heartbeat monitoring to keep session alive and save cookies

### Core Modules (`train/`)

| Directory | Purpose |
|-----------|---------|
| `login/` | Multi-step login flow, CAPTCHA handling, device fingerprint acquisition |
| `query/` | Ticket availability queries with filtering by date, train, seat type, time window |
| `submit/` | Order submission and confirmation |
| `cookie/` | Device fingerprint (RAIL_DEVICEID) retrieval using Selenium/chromedriver |
| `image_captcha/` | CAPTCHA solving via Baidu/Tencent AI or local processing |

### Network Layer (`net/`)

- **`NetUtils.py`**: `EasyHttp` class wraps `requests.Session` with:
  - Persistent cookies across requests
  - Random proxy selection from IP pool
  - Automatic retry logic via `@sendLogic` decorator
  - Header management with rotating User-Agents

- **`spider/`**: Scrapes free proxy IPs to rotate and avoid blocking

### Configuration

- **`configure.py`**: User configuration for credentials, ticket preferences, seat types, notification settings (email/SMS via Twilio), CAPTCHA method selection, proxy pool settings
- **`conf/`**: Constants (`SEAT_TYPE`, `PASSENGER_TYPE`, etc.) and 12306 API URL configurations

### Key Patterns

1. **CAPTCHA Methods** (configured in `SELECT_AUTO_CHECK_CAPTHCA`):
   - `1`: Manual input (default)
   - `2`: Third-party API (legacy)
   - `3`: Baidu/Tencent AI OCR

2. **Device Fingerprint**: `RAIL_DEVICEID` and `RAIL_EXPIRATION` cookies are required. Can be obtained manually or via Selenium (`train/cookie/getCookie.py`).

3. **Maintenance Window**: Tool pauses between 23:00-06:00 when 12306 is down (`utils/deadline.py`).

4. **Proxy Rotation**: `ips` module stores scraped proxies; `EasyHttp` randomly selects one per request.

### Notification Services
- **Email**: SMTP with SSL (configured in `configure.py`)
- **SMS**: Twilio API (`utils/sms.py`)

## Dependencies

Key libraries: `requests`, `selenium`, `beautifulsoup4`, `opencv-python`, `baidu-aip`, `twilio`, `threadpool`, `lxml`, `colorama`, `prettytable`

## Important Notes

- This tool was designed for the 2019 version of 12306. The API and anti-bot measures may have changed.
- The CAPTCHA auto-recognition services (Baidu/Tencent) require valid API credentials.
- Rate limiting is important - the default query interval is 0.4 seconds.