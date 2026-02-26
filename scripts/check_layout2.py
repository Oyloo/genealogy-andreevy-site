from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto("http://localhost:8089")
        page.wait_for_timeout(3000)
        
        rect1 = page.evaluate("document.querySelector('.layout > .panel:nth-child(1)').getBoundingClientRect()")
        rectH = page.evaluate("document.getElementById('graphHost').getBoundingClientRect()")
        
        print(f"Panel1 Rect: {rect1}")
        print(f"Host Rect: {rectH}")
        
        browser.close()

if __name__ == "__main__":
    run()
