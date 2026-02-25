from playwright.sync_api import sync_playwright
import time

def run():
    print("Starting Playwright...")
    with sync_playwright() as p:
        browser = p.webkit.launch()
        
        # Desktop
        print("Capturing Desktop...")
        page_d = browser.new_page(viewport={"width": 1400, "height": 900})
        page_d.goto("http://localhost:8089")
        page_d.wait_for_timeout(3000)
        
        layout_h = page_d.evaluate("window.getComputedStyle(document.querySelector('.layout')).height")
        panel_h = page_d.evaluate("window.getComputedStyle(document.querySelector('.panel:nth-child(2)')).height")
        content_h = page_d.evaluate("window.getComputedStyle(document.querySelector('.panel:nth-child(2) .content')).height")
        host_h = page_d.evaluate("window.getComputedStyle(document.getElementById('graphHost')).height")
        
        print(f"Layout H: {layout_h}")
        print(f"Panel H: {panel_h}")
        print(f"Content H: {content_h}")
        print(f"Host H: {host_h}")
        
        page_d.screenshot(path="verify-desktop-local.png")
        browser.close()

if __name__ == "__main__":
    run()
