from playwright.sync_api import sync_playwright
import os

def main():
    os.makedirs("auth", exist_ok=True)
    state_file = "auth/medium_state.json"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel="chrome",  # Uses the local installed Chrome instead of Playwright's Chromium
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to Medium login page...")
        page.goto("https://medium.com/m/signin")
        
        print("Please log in manually.")
        print("Press Enter in this console ONCE you have successfully logged in and are on the Medium homepage.")
        input("Press Enter to save session...")
        
        context.storage_state(path=state_file)
        print(f"Session saved to {state_file}")
        
        browser.close()

if __name__ == "__main__":
    main()
