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
            
            # Get node position
            node_pos = page.evaluate("""
                () => {
                    return {
                        selected: selected,
                        nodePos: graph.xy[selected],
                        nodeW: graph.nodeW,
                        nodeH: graph.nodeH,
                        cx: graph.xy[selected].x + graph.nodeW / 2,
                        cy: graph.xy[selected].y + graph.nodeH / 2
                    };
                }
            """)
            
            print(f"Node Position: {node_pos}")
            
            # Calculate what centerOnSelected should do
            leftPanelWidth = 280
            rightPanelWidth = 370
            scaleX = 1790.3999999999999 / 1400
            
            print(f"scaleX: {scaleX}")
            print(f"rightPanel - leftPanel: {rightPanelWidth - leftPanelWidth}")
            print(f"offset: {((rightPanelWidth - leftPanelWidth) / 2) * scaleX}")
            
            browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
