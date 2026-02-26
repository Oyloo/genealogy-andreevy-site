from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto("http://localhost:8089")
        page.wait_for_timeout(2000)
        
        # Bring it to front
        page.evaluate("document.getElementById('graphHost').style.zIndex = '0'")
        page.wait_for_timeout(1000)
        page.screenshot(path="/Users/oyloo/.openclaw/workspace/genealogy-site/verify-tree-z0.png")
        
        browser.close()

if __name__ == "__main__":
    run()
