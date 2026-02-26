from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto("http://localhost:8089")
        page.wait_for_timeout(3000)
        
        bg1 = page.evaluate("window.getComputedStyle(document.querySelector('.layout > .panel:nth-child(1)')).backgroundColor")
        bg3 = page.evaluate("window.getComputedStyle(document.querySelector('.layout > .panel:nth-child(3)')).backgroundColor")
        
        print(f"Panel 1 bg: {bg1}")
        print(f"Panel 3 bg: {bg3}")
        
        browser.close()

if __name__ == "__main__":
    run()
