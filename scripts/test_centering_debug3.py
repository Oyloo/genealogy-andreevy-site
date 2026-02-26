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
            
            # Get debug info
            info = page.evaluate("""
                () => {
                    const host = document.getElementById('graphHost');
                    const leftPanel = document.querySelector('.layout > .panel:nth-child(1)');
                    const rightPanel = document.querySelector('.layout > .panel:nth-child(3)');
                    return {
                        hostClientWidth: host.clientWidth,
                        leftPanelWidth: leftPanel.offsetWidth,
                        rightPanelWidth: rightPanel.offsetWidth,
                        worldW: graph.worldW,
                        viewX: view.x,
                        viewW: view.w
                    };
                }
            """)
            
            print(f"Host width: {info['hostClientWidth']}")
            print(f"Left panel: {info['leftPanelWidth']}")
            print(f"Right panel: {info['rightPanelWidth']}")
            print(f"World W: {info['worldW']}")
            print(f"View X: {info['viewX']}")
            print(f"View W: {info['viewW']}")
            
            # Calculate what should be
            panelLeft = info['leftPanelWidth']
            panelRight = info['rightPanelWidth']
            visibleCenterPixels = panelLeft + (info['hostClientWidth'] - panelLeft - panelRight) / 2
            screenCenterPixels = info['hostClientWidth'] / 2
            pixelOffset = visibleCenterPixels - screenCenterPixels
            scaleX = info['viewW'] / info['hostClientWidth']
            worldOffset = pixelOffset * scaleX
            worldCenter = info['worldW'] / 2
            expectedViewX = worldCenter + worldOffset - info['viewW'] / 2
            
            print(f"\nCalculations:")
            print(f"Visible center pixels: {visibleCenterPixels}")
            print(f"Screen center pixels: {screenCenterPixels}")
            print(f"Pixel offset: {pixelOffset}")
            print(f"Scale X: {scaleX}")
            print(f"World offset: {worldOffset}")
            print(f"Expected view.x: {expectedViewX}")
            
            browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
