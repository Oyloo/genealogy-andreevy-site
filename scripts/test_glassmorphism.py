import subprocess
import time
from playwright.sync_api import sync_playwright

def run():
    print("Starting server...")
    server = subprocess.Popen(["python3", "-m", "http.server", "8089", "--directory", "/Users/oyloo/.openclaw/workspace/genealogy-site/"])
    time.sleep(2)
    
    try:
        print("Running glassmorphism test...")
        with sync_playwright() as p:
            browser = p.webkit.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto("http://localhost:8089")
            page.wait_for_timeout(3000)
            
            # Use evaluate to click in case the button is somehow unclickable naturally
            print("Zooming in...")
            for _ in range(12):
                page.evaluate("""
                    let btn = document.getElementById('zoomInBtn');
                    if(btn) btn.click();
                """)
                page.wait_for_timeout(200)
            
            # Pan slightly to ensure a dense part of the tree is under the left panel
            print("Panning...")
            page.evaluate("""
                let svg = document.getElementById('graphSvg');
                if(svg) {
                    const evt1 = new MouseEvent('mousedown', { view: window, bubbles: true, cancelable: true, clientX: 700, clientY: 450 });
                    svg.dispatchEvent(evt1);
                    const evt2 = new MouseEvent('mousemove', { view: window, bubbles: true, cancelable: true, clientX: 1100, clientY: 450 });
                    window.dispatchEvent(evt2);
                    const evt3 = new MouseEvent('mouseup', { view: window, bubbles: true, cancelable: true, clientX: 1100, clientY: 450 });
                    window.dispatchEvent(evt3);
                }
            """)
            
            page.wait_for_timeout(1000)
            
            screenshot_path = "/Users/oyloo/.openclaw/workspace/genealogy-site/verify-glassmorphism.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            
            browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
