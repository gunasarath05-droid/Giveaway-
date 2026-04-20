import time
import re
from playwright.sync_api import sync_playwright

def scrape_instagram_comments(url):
    comments_data = []

    with sync_playwright() as p:
        # Launch browser with recommended stability and anti-detection flags
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled",
                "--single-process"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()

        try:
            print(f"🚀 [Scraper] Navigating to: {url}")
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Check if we were redirected to a login page
            if "/login" in page.url:
                print("⚠️ [Scraper] Blocked by Login Wall! Instagram is requiring login for this IP.")
                return []

            # Wait for content to load (Increase for Render/Instagram stability)
            page.wait_for_timeout(5000)
            print("✅ [Scraper] Page initial load complete.")

            # Try to close login popup if it appears
            try:
                close_button = page.get_by_role("button", name="Close").first
                if close_button.is_visible():
                    close_button.click()
                    print("🔘 [Scraper] Closed login popup.")
                
                not_now = page.get_by_text("Not Now").first
                if not_now.is_visible():
                    not_now.click()
                    print("🔘 [Scraper] Clicked 'Not Now'.")
            except Exception:
                pass

            # Scroll to load comments
            print("🖱️ [Scraper] Scrolling to load comments...")
            for i in range(12):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1500)
                
                if i % 4 == 0:
                    print(f"   - Scroll progress: {i+1}/12")

                # Check for "Load more" button
                try:
                    load_more = page.locator('svg[aria-label="Load more comments"]').first
                    if load_more.is_visible():
                        load_more.click()
                        page.wait_for_timeout(2000)
                except:
                    pass

            # Extraction
            print("🔍 [Scraper] Extracting comments...")
            # Optimized selectors for Instagram's dynamic class names
            comment_elements = page.locator('ul > div > li, ul > li').all()
            print(f"📊 [Scraper] Found {len(comment_elements)} potential comment elements.")
            
            for el in comment_elements:
                try:
                    # Look for username
                    username_el = el.locator('h3, h4, strong, a').first
                    username = username_el.text_content().strip() if username_el.is_visible() else ""
                    
                    # Look for comment text (usually the first span that isn't the username)
                    comment_text_el = el.locator('span').nth(1)
                    if not comment_text_el.is_visible():
                        comment_text_el = el.locator('div[role="none"] > span').first
                        
                    comment_text = comment_text_el.text_content().strip() if comment_text_el.is_visible() else ""
                    
                    # Look for likes
                    likes_count = 0
                    likes_text_el = el.locator('span:has-text("likes")').first
                    if likes_text_el.is_visible():
                        likes_text = likes_text_el.text_content()
                        match = re.search(r'(\d+(?:,\d+)*)', likes_text)
                        if match:
                            likes_count = int(match.group(1).replace(',', ''))

                    if username and comment_text and len(username) < 30: # Filter out noise
                        comments_data.append({
                            "username": username,
                            "comment": comment_text,
                            "likes": likes_count
                        })
                except Exception:
                    continue

            print(f"✨ [Scraper] Successfully extracted {len(comments_data)} raw comments.")

        except Exception as e:
            print(f"❌ [Scraper] Scraping error: {str(e)}")
        finally:
            browser.close()
            print("🔒 [Scraper] Browser closed.")

    # Deduplicate by (username, comment)
    seen = set()
    unique_comments = []
    for c in comments_data:
        key = (c['username'], c['comment'])
        if key not in seen:
            seen.add(key)
            unique_comments.append(c)

    print(f"🏁 [Scraper] Returning {len(unique_comments[:10])} final unique comments.")
    # Sort by likes descending
    unique_comments.sort(key=lambda x: x['likes'], reverse=True)

    return unique_comments[:10]
