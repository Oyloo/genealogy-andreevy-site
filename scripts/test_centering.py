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
            
            # Find the center of the graph host (the SVG canvas container)
            host_rect = page.evaluate("document.getElementById('graphHost').getBoundingClientRect()")
            
            host_center_x = host_rect['x'] + host_rect['width'] / 2
            host_center_y = host_rect['y'] + host_rect['height'] / 2
            
            dx = abs(node_center_x - host_center_x)
            dy = abs(node_center_y - host_center_y)
            
            print(f"Selected Node ({node_info['id']}) Center: x={node_center_x:.1f}, y={node_center_y:.1f}")
            print(f"Graph Canvas Center: x={host_center_x:.1f}, y={host_center_y:.1f}")
            print(f"Difference: dx={dx:.1f}px, dy={dy:.1f}px")
            
            if dx < 2.0 and dy < 2.0:
                print("SUCCESS: The selected node is perfectly centered on the graph canvas.")
                sys.exit(0)
            else:
                print("FAILED: The selected node is NOT centered.")
                sys.exit(1)
                
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
