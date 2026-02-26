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
            
            # Find the selected node
            node_info = page.evaluate("""
                () => {
                    const node = document.querySelector(`.node[data-id="${selected}"]`);
                    const rect = node.getBoundingClientRect();
                    return { x: rect.x, y: rect.y, w: rect.width, h: rect.height, id: selected };
                }
            """)
            
            if not node_info:
                print("FAILED: No selected node found.")
                sys.exit(1)
                
            node_center_x = node_info['x'] + node_info['w'] / 2
            node_center_y = node_info['y'] + node_info['h'] / 2
            
            # Find the optical center (between the side panels)
            panel1_rect = page.evaluate("document.querySelector('.layout > .panel:nth-child(1)').getBoundingClientRect()")
            panel3_rect = page.evaluate("document.querySelector('.layout > .panel:nth-child(3)').getBoundingClientRect()")
            
            visible_left = panel1_rect['right']
            visible_right = panel3_rect['left']
            visible_center_x = visible_left + (visible_right - visible_left) / 2
            
            # For Y, the optical center is still the middle of the graph canvas
            host_rect = page.evaluate("document.getElementById('graphHost').getBoundingClientRect()")
            visible_center_y = host_rect['y'] + host_rect['height'] / 2
            
            dx = abs(node_center_x - visible_center_x)
            dy = abs(node_center_y - visible_center_y)
            
            print(f"Selected Node ({node_info['id']}) Center: x={node_center_x:.1f}, y={node_center_y:.1f}")
            print(f"Visible Area Center: x={visible_center_x:.1f}, y={visible_center_y:.1f}")
            print(f"Difference: dx={dx:.1f}px, dy={dy:.1f}px")
            
            if dx < 10.0 and dy < 2.0:
                print("SUCCESS: The selected node is optically centered between the side panels.")
                sys.exit(0)
            else:
                print("FAILED: The selected node is NOT centered.")
                sys.exit(1)
                
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
