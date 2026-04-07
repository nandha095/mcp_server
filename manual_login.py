"""
Manual LinkedIn Login Helper Script
====================================

This script opens a browser window for you to log in to LinkedIn manually.
After successful login, the browser session will be saved and can be used
by the automation tools.

Instructions:
1. Run this script: python manual_login.py
2. A Chrome browser window will open
3. Log in to LinkedIn with your credentials
4. Complete any verification/CAPTCHA if prompted
5. Once you see your LinkedIn feed, close the browser window
6. The session will be saved automatically

After completing these steps, you can run the automation tools again.
"""

import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright


# Configuration
USER_DATA_DIR = str((Path.home() / ".pw_linkedin_profile").resolve())
LINKEDIN_URL = "https://www.linkedin.com/login"
FEED_URL = "https://www.linkedin.com/feed/"
TIMEOUT = 300  # 5 minutes timeout for manual login


async def manual_login():
    """Open browser for manual LinkedIn login and save session."""
    print("=" * 60)
    print("LinkedIn Manual Login Helper")
    print("=" * 60)
    print()
    print(f"Profile directory: {USER_DATA_DIR}")
    print()
    print("Instructions:")
    print("1. A Chrome browser window will open")
    print("2. Log in to LinkedIn with your credentials")
    print("3. Complete any verification/CAPTCHA if prompted")
    print("4. Once you see your LinkedIn feed, close the browser window")
    print("5. The session will be saved automatically")
    print()
    print("The browser will close automatically after 5 minutes if not closed manually.")
    print()
    input("Press Enter to open the browser...")
    
    playwright = await async_playwright().start()
    
    try:
        # Launch browser with persistent context
        context = await playwright.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            channel="chrome",
            headless=False,
            viewport={"width": 1440, "height": 900},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
        )
        
        page = context.pages[0] if context.pages else await context.new_page()
        
        print("\nBrowser opened. Please log in to LinkedIn...")
        print("Navigate to LinkedIn if the page doesn't load automatically.")
        
        # Navigate to LinkedIn login
        await page.goto(LINKEDIN_URL, wait_until="domcontentloaded")
        
        # Wait for manual login (monitor for feed page)
        print("Waiting for successful login...")
        
        try:
            # Wait until user navigates to feed or timeout
            await page.wait_for_url(FEED_URL, timeout=TIMEOUT * 1000)
            print("\n✓ Login successful! LinkedIn feed detected.")
            await asyncio.sleep(2)  # Give time for page to fully load
        except Exception:
            # Check if we're on feed page anyway
            if FEED_URL in page.url:
                print("\n✓ Login successful! LinkedIn feed detected.")
            else:
                print(f"\n⚠ Timeout reached. Current URL: {page.url}")
                print("If you've logged in successfully, the session should be saved.")
        
        print("\nYou can now close the browser window.")
        print("The session will be saved automatically when the browser closes.")
        
        # Keep the context alive until browser is closed
        try:
            await context.pages[0].wait_for_event("close", timeout=60000)
        except Exception:
            pass
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
    finally:
        await playwright.stop()
    
    print("\n" + "=" * 60)
    print("Session saved successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run your automation script again")
    print("2. The automation will use the saved session")
    print("3. You should be able to apply to jobs without verification")
    print()
    print("If you still encounter verification issues, you may need to:")
    print("- Wait a few hours and try again")
    print("- Use a different network/IP address")
    print("- Complete any additional verification LinkedIn requests")
    print()
    
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(manual_login())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nLogin cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)