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
            
            # Get all visible nodes
            nodes = page.evaluate("""
                () => {
                    let results = [];
                    document.querySelectorAll('.node').forEach(node => {
                        const rect = node.getBoundingClientRect();
                        results.push({
                            id: node.dataset.id,
                            x: rect.x,
                            centerX: rect.x + rect.width / 2
                        });
                    });
                    return results;
                }
            """)
            
            # Get panel info
            panel1 = page.evaluate("document.querySelector('.layout > .panel:nth-child(1)').getBoundingClientRect()")
            panel3 = page.evaluate("document.querySelector('.layout > .panel:nth-child(3)').getBoundingClientRect()")
            
            visible_left = panel1['right']
            visible_right = panel3['left']
            visible_center = visible_left + (visible_right - visible_left) / 2
            
            print(f"Visible area: left={visible_left}, right={visible_right}, center={visible_center}")
            print(f"Nodes (first 5):")
            for node in nodes[:5]:
                print(f"  {node['id']}: centerX={node['centerX']:.1f} (offset from visible center: {node['centerX']-visible_center:.1f}px)")
            
            browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
