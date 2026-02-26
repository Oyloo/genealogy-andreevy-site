from playwright.sync_api import sync_playwright

def run():
    print("Running mandatory playwright test...")
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto("http://localhost:8089")
        page.wait_for_timeout(3000) # Give it time to render the graph
        
        page.screenshot(path="/Users/oyloo/.openclaw/workspace/genealogy-site/verify-tree-bug.png")
        print("Screenshot saved to verify-tree-bug.png")
        
        # Check elements
        nodes = page.evaluate("document.querySelectorAll('.node').length")
        edges = page.evaluate("document.querySelectorAll('.edge').length")
        print(f"Nodes found in DOM: {nodes}")
        print(f"Edges found in DOM: {edges}")
        
        # Check graphHost bounds and z-index computed
        host = page.evaluate("""() => {
            const el = document.getElementById('graphHost');
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            return { rect, zIndex: style.zIndex, display: style.display, visibility: style.visibility };
        }""")
        print(f"graphHost info: {host}")
        
        # Check layout bounds
        layout = page.evaluate("""() => {
            const el = document.querySelector('.layout');
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            return { rect, zIndex: style.zIndex, background: style.backgroundColor };
        }""")
        print(f"layout info: {layout}")

        browser.close()

if __name__ == "__main__":
    run()
