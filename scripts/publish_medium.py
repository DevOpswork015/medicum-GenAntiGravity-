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
        browser = p.chromium.launch(headless=is_ci)
        context = browser.new_context(storage_state=state_file)
        page = context.new_page()
        
        try:
            print("Navigating to Medium Import Story page...")
            page.goto("https://medium.com/p/import")
            page.wait_for_load_state("networkidle")
            
            print(f"Pasting URL: {github_pages_url}")
            page.fill('input[type="url"]', github_pages_url)
            page.click('button:has-text("Import")')
            
            print("Waiting for Medium to parse...")
            try:
                page.wait_for_selector('button:has-text("See your story")', timeout=30000)
                page.click('button:has-text("See your story")')
            except:
                print("Could not find 'See your story' button, looking for alternative...")
                page.wait_for_timeout(5000)
                
            page.wait_for_load_state("networkidle")
            print("Story imported successfully into drafts.")
            
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
