from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.webkit.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto("http://localhost:8089")
        page.wait_for_timeout(3000)
        
        # Try to click on the svg
        try:
            page.mouse.click(700, 400)
            print("Click successful")
            # Hover over a search box in the left panel
            page.click("#q")
            print("Click on search box successful")
        except Exception as e:
            print("Error: ", e)
            
        browser.close()

if __name__ == "__main__":
    run()
