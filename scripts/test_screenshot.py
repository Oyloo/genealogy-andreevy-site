import subprocess
import time
from playwright.sync_api import sync_playwright

def run():
    print("Starting server...")
    server = subprocess.Popen(["python3", "-m", "http.server", "8089", "--directory", "/Users/oyloo/.openclaw/workspace/genealogy-site/"])
    time.sleep(2)
    
    try:
        with sync_playwright() as p:
            browser = p.webkit.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto("http://localhost:8089/index.html")
            page.wait_for_timeout(3000)
            
            page.screenshot(path="/Users/oyloo/.openclaw/workspace/genealogy-site/verify-centered.png")
            print("Screenshot saved to verify-centered.png")
            
            browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
