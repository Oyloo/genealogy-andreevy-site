import subprocess
import time
from playwright.sync_api import sync_playwright

def run():
    print("Starting server...")
    server = subprocess.Popen(["python3", "-m", "http.server", "8089", "--directory", "/Users/oyloo/.openclaw/workspace/genealogy-site/"])
    time.sleep(2)
    
    try:
        print("Running pan test...")
        with sync_playwright() as p:
            browser = p.webkit.launch()
            page = browser.new_page(viewport={"width": 1400, "height": 900})
            page.goto("http://localhost:8089/index.html")
            page.wait_for_timeout(3000)
            
            # Start by selecting a node to center it
            page.evaluate("document.querySelector('.item').click()")
            page.wait_for_timeout(1000)
            
            init_viewbox = page.evaluate("document.querySelector('svg').getAttribute('viewBox')")
            print(f"Initial viewBox: {init_viewbox}")
            
            page.evaluate("""
                let host = document.getElementById('graphHost');
                const evt1 = new MouseEvent('mousedown', { view: window, bubbles: true, cancelable: true, clientX: 700, clientY: 450 });
                document.querySelector('svg').dispatchEvent(evt1);
            """)
            page.wait_for_timeout(50)
            page.evaluate("""
                const evt2 = new MouseEvent('mousemove', { view: window, bubbles: true, cancelable: true, clientX: 600, clientY: 450 });
                window.dispatchEvent(evt2);
            """)
            page.wait_for_timeout(50)
            page.evaluate("""
                const evt3 = new MouseEvent('mousemove', { view: window, bubbles: true, cancelable: true, clientX: 500, clientY: 450 });
                window.dispatchEvent(evt3);
            """)
            page.wait_for_timeout(50)
            page.evaluate("""
                const evt4 = new MouseEvent('mouseup', { view: window, bubbles: true, cancelable: true, clientX: 500, clientY: 450 });
                window.dispatchEvent(evt4);
            """)
            
            page.wait_for_timeout(1000)
            
            final_viewbox = page.evaluate("document.querySelector('svg').getAttribute('viewBox')")
            print(f"Final viewBox: {final_viewbox}")
            
            if init_viewbox != final_viewbox:
                print("SUCCESS: Panning changes the viewBox.")
            else:
                print("FAILED: Panning did not change the viewBox.")
                
            browser.close()
    finally:
        server.terminate()

if __name__ == "__main__":
    run()
