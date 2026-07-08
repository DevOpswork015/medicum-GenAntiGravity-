from playwright.sync_api import sync_playwright
import os
import sys

def main():
    state_file = "auth/medium_state.json"
    if not os.path.exists(state_file):
        print(f"Error: {state_file} not found. Run get_medium_session.py first.")
        sys.exit(1)
        
    github_pages_url = os.environ.get("PAGES_URL", "http://localhost:8000/") # Default to local test if not set
    
    with sync_playwright() as p:
        # Run headed if not in CI
        is_ci = os.environ.get("CI") == "true"
        browser = p.chromium.launch(
            headless=is_ci,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=state_file,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("Navigating to Medium Import Story page...")
            page.goto("https://medium.com/p/import")
            page.wait_for_load_state("networkidle")
            
            print(f"Pasting URL: {github_pages_url}")
            print(f"Pasting URL: {github_pages_url}")
            
            # Find the descriptive text and click right below it
            label = page.locator('text=/Enter a link/i').first
            box = label.bounding_box()
            if box:
                page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] + 40)
                page.wait_for_timeout(500)
                page.keyboard.type(github_pages_url)
            else:
                print("Warning: Could not find label text!")
                page.mouse.click(500, 400)
                page.keyboard.type(github_pages_url)
            
            page.click('button:has-text("Import")')
            
            print("Waiting for Medium to parse...")
            page.wait_for_timeout(5000)
            page.screenshot(path="debug2_after_import_click.png")
            print("Screenshot saved to debug2_after_import_click.png")
            
            try:
                page.wait_for_selector('button:has-text("See your story")', timeout=15000)
                page.click('button:has-text("See your story")')
            except:
                print("Could not find 'See your story' button, looking for alternative...")
                page.screenshot(path="debug3_no_see_story.png")
                
            page.wait_for_load_state("networkidle")
            print("Finished import sequence.")
            
            if is_ci:
                print("In CI environment, attempting to publish...")
                try:
                    page.click('button:has-text("Publish")', timeout=10000)
                    page.wait_for_selector('button:has-text("Publish now")', timeout=10000)
                    page.click('button:has-text("Publish now")')
                    print("Published successfully!")
                except Exception as e:
                    print(f"Warning: Could not automatically hit publish. Left as draft. Error: {e}")
            else:
                print("Local mode: Left as draft. Please review in browser.")
                input("Press Enter to close browser...")
                
        except Exception as e:
            print(f"Error during import: {e}")
            page.screenshot(path="error.png")
            print("Screenshot saved to error.png")
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    main()
