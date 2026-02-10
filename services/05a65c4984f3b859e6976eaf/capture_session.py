#!/usr/bin/env python3
"""Script to capture session data from login page using Playwright"""

import json
import sys
from playwright.sync_api import sync_playwright

def capture_session(public_ip, port, username, password):
    """Perform login and capture session data"""

    login_url = f"http://{public_ip}:{port}/login.html"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to login page
        print(f"Navigating to {login_url}")
        response = page.goto(login_url)
        print(f"Page loaded with status: {response.status}")

        # Fill in login form
        page.fill('#username', username)
        page.fill('#password', password)

        # Submit form
        page.click('button[type="submit"]')

        # Wait for login to complete
        page.wait_for_load_state('networkidle')

        # Check response
        print(f"Current URL: {page.url}")

        # Capture all cookies
        cookies = []
        for cookie in context.cookies():
            cookies.append({
                "name": cookie["name"],
                "value": cookie["value"],
                "domain": cookie.get("domain", ""),
                "path": cookie.get("path", "/"),
                "httpOnly": cookie.get("httpOnly", False),
                "secure": cookie.get("secure", False),
                "sameSite": cookie.get("sameSite", "Lax"),
                "expires": cookie.get("expires", -1)
            })

        # Capture localStorage
        local_storage = page.evaluate("() => JSON.stringify(localStorage)")

        # Capture sessionStorage
        session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")

        # Get page content to verify login
        page_content = page.content()

        browser.close()

        return {
            "cookies": cookies,
            "local_storage": json.loads(local_storage) if local_storage else {},
            "session_storage": json.loads(session_storage) if session_storage else {},
            "login_success": "userInfo" in page_content or "success" in page_content.lower()
        }

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: capture_session.py <public_ip> <port> <username> <password>")
        sys.exit(1)

    public_ip = sys.argv[1]
    port = sys.argv[2]
    username = sys.argv[3]
    password = sys.argv[4]

    result = capture_session(public_ip, port, username, password)
    print(json.dumps(result, indent=2))