"""Quick debug script - runs only first test case and prints what's happening"""
from playwright.sync_api import sync_playwright
import re, time

URL = "https://www.pixelssuite.com/chat-translator"
INPUT_TEXT = "suba udhasanak saman, kohomadha?"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded")
    page.wait_for_load_state("networkidle", timeout=30000)
    page.wait_for_selector("textarea", timeout=30000)
    print("Page loaded")

    # Print all textareas
    meta = page.evaluate("""() => Array.from(document.querySelectorAll('textarea')).map((t,i) => ({
        index: i,
        placeholder: t.getAttribute('placeholder') || '',
        readOnly: !!t.readOnly,
        disabled: !!t.disabled,
        value: t.value,
        visible: !!(t.offsetParent)
    }))""")
    print("\nTextareas found:")
    for m in meta:
        print(f"  [{m['index']}] placeholder='{m['placeholder']}' readOnly={m['readOnly']} value='{m['value'][:50]}'")

    # Find input textarea (first visible)
    textareas = page.locator("textarea")
    count = textareas.count()
    visible = []
    for i in range(count):
        loc = textareas.nth(i)
        if loc.is_visible():
            visible.append((i, loc))
    
    print(f"\nVisible textareas: {len(visible)}")
    
    if len(visible) >= 2:
        input_loc = visible[0][1]
        output_loc = visible[1][1]
        
        # Type input
        input_loc.click()
        input_loc.fill(INPUT_TEXT)
        print(f"\nTyped: {INPUT_TEXT}")
        
        # Click Transliterate button
        try:
            btn = page.get_by_role("button", name=re.compile(r"Transliterate", re.IGNORECASE)).first
            if btn.is_visible():
                btn.click()
                print("Clicked Transliterate button")
        except Exception as e:
            print(f"No button: {e}")
        
        # Wait and read output
        page.wait_for_timeout(5000)
        
        # Try all read methods
        print("\nOutput reading attempts:")
        
        v1 = page.evaluate("""() => {
            const tas = Array.from(document.querySelectorAll('textarea'));
            return tas.map((t,i) => ({index:i, value: t.value, innerText: t.innerText}));
        }""")
        for item in v1:
            print(f"  textarea[{item['index']}] value='{item['value'][:80]}' innerText='{item['innerText'][:80]}'")
        
        try:
            print(f"  output_loc.input_value() = '{output_loc.input_value()}'")
        except Exception as e:
            print(f"  input_value error: {e}")
        
        try:
            print(f"  output_loc.inner_text() = '{output_loc.inner_text()}'")
        except Exception as e:
            print(f"  inner_text error: {e}")
        
        try:
            v = output_loc.evaluate("(el) => el.value")
            print(f"  evaluate el.value = '{v}'")
        except Exception as e:
            print(f"  evaluate error: {e}")

    input("\nPress Enter to close browser...")
    browser.close()
