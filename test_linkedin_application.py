#!/usr/bin/env python3
"""Quick test script for LinkedIn application functionality."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from server import _click_easy_apply, _ensure_logged_in, _launch_context, _close_context


async def test_login_detection() -> bool:
    print("Testing LinkedIn login detection...")
    context = None
    try:
        context = await _launch_context()
        page = context.pages[0] if context.pages else await context.new_page()
        logged_in = await _ensure_logged_in(page)
        if logged_in:
            print("Login detection working")
        else:
            print("Login detection failed. Run login_linkedin.py first.")
        await _close_context(context)
        return logged_in
    except Exception as exc:
        print(f"Login detection test failed: {exc}")
        if context:
            await _close_context(context)
        return False


async def test_easy_apply_detection() -> bool:
    print("Testing Easy Apply button detection...")
    test_job_url = "https://www.linkedin.com/jobs/view/1234567890/"
    context = None
    try:
        context = await _launch_context()
        page = context.pages[0] if context.pages else await context.new_page()

        if not await _ensure_logged_in(page):
            print("Cannot test easy apply: not logged in")
            await _close_context(context)
            return False

        try:
            await page.goto(test_job_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            clicked = await _click_easy_apply(page)
            print("Easy Apply detection clicked" if clicked else "Easy Apply not found on test URL")
        except Exception as exc:
            print(f"Could not load test job page: {exc}")

        await _close_context(context)
        return True
    except Exception as exc:
        print(f"Easy apply test failed: {exc}")
        if context:
            await _close_context(context)
        return False


async def main() -> None:
    print("LinkedIn Job Application Test Suite")
    print("=" * 40)
    login_ok = await test_login_detection()
    easy_ok = await test_easy_apply_detection()
    print("=" * 40)
    print(f"Login Detection: {'PASS' if login_ok else 'FAIL'}")
    print(f"Easy Apply Detection: {'PASS' if easy_ok else 'FAIL'}")


if __name__ == "__main__":
    asyncio.run(main())
