import subprocess
import time
import sys
from playwright.sync_api import sync_playwright

def run():
    print("Starting server...")
    server = subprocess.Popen(["python3", "-m", "http.server", "8089", "--directory", "/Users/oyloo/.openclaw/workspace/genealogy-site/"])
    time.sleep(2)
    
    try:
        print("Running centering test...")
        with sync_playwright() as p:
            browser = p.webkit.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto("http://localhost:8089/index.html")
            page.wait_for_timeout(3000)
            
            # Find all visible nodes and calculate their spread
            nodes = page.evaluate("""
                () => {
                    let xCoords = [];
                    document.querySelectorAll('.node').forEach(node => {
                        const rect = node.getBoundingClientRect();
                        xCoords.push(rect.x + rect.width / 2);
                    });
                    return {
                        minX: Math.min(...xCoords),
                        maxX: Math.max(...xCoords),
                        centerX: (Math.min(...xCoords) + Math.max(...xCoords)) / 2
                    };
                }
            """)
            
            # Get panel info
            panel1 = page.evaluate("document.querySelector('.layout > .panel:nth-child(1)').getBoundingClientRect()")
            panel3 = page.evaluate("document.querySelector('.layout > .panel:nth-child(3)').getBoundingClientRect()")
            
            visible_left = panel1['right']
            visible_right = panel3['left']
            visible_center = visible_left + (visible_right - visible_left) / 2
            
            print(f"Visible area: left={visible_left}, right={visible_right}, center={visible_center}")
            print(f"Tree spread: min={nodes['minX']:.1f}, max={nodes['maxX']:.1f}, center={nodes['centerX']:.1f}")
            print(f"Difference: {abs(nodes['centerX'] - visible_center):.1f}px")
            
            if abs(nodes['centerX'] - visible_center) < 20.0:
                print("SUCCESS: Tree is centered between panels.")
                sys.exit(0)
            else:
                print("FAILED: Tree is NOT centered.")
                sys.exit(1)
                
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
