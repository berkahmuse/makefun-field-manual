#!/usr/bin/env python3
"""Screenshot the live GitHub repo page via Playwright + system Chromium,
routing through the VM egress proxy (credentials from env, never printed)."""
import os
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright

proxy_url = os.environ["HTTPS_PROXY"]
u = urlparse(proxy_url)
proxy = {"server": "http://127.0.0.1:18080"}  # local MITM forwarder, no auth

out = os.path.expanduser(
    "~/workspace/makefun-humans02/entries/makefun-field-manual/screenshot.png")
with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path=os.path.expanduser(
            "~/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome"),
        args=["--no-sandbox", "--disable-gpu"],
        proxy=proxy,
    )
    ctx = browser.new_context(viewport={"width": 1280, "height": 1400},
                              ignore_https_errors=True)
    page = ctx.new_page()
    page.goto("https://github.com/chlutud/makefun-field-manual",
              wait_until="networkidle", timeout=60000)
    page.wait_for_timeout(5000)
    page.screenshot(path=out)
    print("title:", page.title())
    print("saved:", out)
    browser.close()
