import subprocess
import time
from playwright.sync_api import sync_playwright

def run():
    print("Starting server...")
    server = subprocess.Popen(["python3", "-m", "http.server", "8089", "--directory", "/Users/oyloo/.openclaw/workspace/genealogy-site/"])
    time.sleep(2)
    
    try:
        print("Running centering debug test...")
        with sync_playwright() as p:
            browser = p.webkit.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto("http://localhost:8089/index.html")
            page.wait_for_timeout(3000)
            
            # Get debug info
            debug_info = page.evaluate("""
                () => {
                    return {
                        innerWidth: window.innerWidth,
                        selected: selected,
                        graphExists: !!graph,
                        graphXy: graph?.xy ? Object.keys(graph.xy).slice(0, 3) : null,
                        hostClientWidth: document.getElementById('graphHost').clientWidth,
                        leftPanelWidth: document.querySelector('.layout > .panel:nth-child(1)').offsetWidth,
                        rightPanelWidth: document.querySelector('.layout > .panel:nth-child(3)').offsetWidth,
                        viewX: view.x,
                        viewY: view.y,
                        viewW: view.w,
                        viewH: view.h
                    };
                }
            """)
            
            print(f"Debug Info: {debug_info}")
            
            browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
