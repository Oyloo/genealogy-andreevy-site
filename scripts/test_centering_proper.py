import subprocess
import time
import sys
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
            
            # Get all visible nodes with actual screen positions
            nodes = page.evaluate("""
                () => {
                    let results = [];
                    document.querySelectorAll('.node').forEach(node => {
                        const rect = node.getBoundingClientRect();
                        results.push({
                            id: node.dataset.id,
                            screenX: rect.x,
                            screenRight: rect.right,
                            screenWidth: rect.width
                        });
                    });
                    return {
                        nodes: results,
                        minScreenX: Math.min(...results.map(n => n.screenX)),
                        maxScreenX: Math.max(...results.map(n => n.screenRight))
                    };
                }
            """)
            
            # Get panel boundaries
            panel1 = page.evaluate("document.querySelector('.layout > .panel:nth-child(1)').getBoundingClientRect()")
            panel3 = page.evaluate("document.querySelector('.layout > .panel:nth-child(3)').getBoundingClientRect()")
            
            left_edge = panel1['right']
            right_edge = panel3['left']
            visible_center = left_edge + (right_edge - left_edge) / 2
            
            print(f"Panel boundaries:")
            print(f"  Left edge (where left panel ends): {left_edge}")
            print(f"  Right edge (where right panel starts): {right_edge}")
            print(f"  Visible center: {visible_center}")
            print(f"\nTree bounds:")
            print(f"  Min X: {nodes['minScreenX']}")
            print(f"  Max X: {nodes['maxScreenX']}")
            print(f"  Tree center: {(nodes['minScreenX'] + nodes['maxScreenX']) / 2}")
            
            # Check if tree overlaps with panels
            if nodes['minScreenX'] < left_edge:
                print(f"\n❌ LEFT PROBLEM: Tree left edge ({nodes['minScreenX']:.1f}) overlaps left panel (ends at {left_edge})")
                overlap = left_edge - nodes['minScreenX']
                print(f"   Overlap: {overlap:.1f}px")
            else:
                print(f"\n✓ Tree right of left panel")
                
            if nodes['maxScreenX'] > right_edge:
                print(f"❌ RIGHT PROBLEM: Tree right edge ({nodes['maxScreenX']:.1f}) overlaps right panel (starts at {right_edge})")
                overlap = nodes['maxScreenX'] - right_edge
                print(f"   Overlap: {overlap:.1f}px")
            else:
                print(f"✓ Tree left of right panel")
            
            tree_center = (nodes['minScreenX'] + nodes['maxScreenX']) / 2
            center_diff = abs(tree_center - visible_center)
            print(f"\nCentering: Tree center at {tree_center:.1f}, visible center at {visible_center:.1f}, diff={center_diff:.1f}px")
            
            if nodes['minScreenX'] >= left_edge and nodes['maxScreenX'] <= right_edge and center_diff < 20:
                print("\n✅ SUCCESS: Tree is properly centered and visible!")
                sys.exit(0)
            else:
                print("\n❌ FAILED: Tree is not properly positioned")
                sys.exit(1)
                
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
