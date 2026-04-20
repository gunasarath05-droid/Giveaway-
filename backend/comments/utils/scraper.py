import time
import re
from playwright.sync_api import sync_playwright

def scrape_instagram_comments(url):
    comments_data = []

    with sync_playwright() as p:
        # Launch browser with user-agent spoofing
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print(f"Navigating to {url}...")
            page.goto(url, wait_until="networkidle", timeout=60000)
            
            # Wait for content to load
            page.wait_for_timeout(3000)

            # Try to close login popup if it appears
            try:
                # Sometimes there's a "Not Now" or an 'X' button
                close_button = page.get_by_role("button", name="Close")
                if close_button.is_visible():
                    close_button.click()
                
                not_now = page.get_by_text("Not Now")
                if not_now.is_visible():
                    not_now.click()
            except Exception:
                pass

            # Scroll to load comments
            print("Scrolling to load comments...")
            for i in range(12):
                page.mouse.wheel(0, 2000)
                page.wait_for_timeout(1500)
                
                # Check for "Load more" button if it exists (for some layouts)
                try:
                    load_more = page.locator('svg[aria-label="Load more comments"]')
                    if load_more.is_visible():
                        load_more.click()
                        page.wait_for_timeout(2000)
                except:
                    pass

            # Extraction
            print("Extracting comments...")
            # Instagram post comments usually live in a 'ul'
            # We look for elements that look like comments
            comment_elements = page.locator('ul > div > li, ul > li').all()
            
            for el in comment_elements:
                try:
                    # Look for username (usually in a strong or a tag)
                    username_el = el.locator('h3, strong, a').first
                    username = username_el.text_content().strip() if username_el.is_visible() else ""
                    
                    # Look for comment text
                    # Often the first span after the username
                    comment_text_el = el.locator('span').nth(1)
                    comment_text = comment_text_el.text_content().strip() if comment_text_el.is_visible() else ""
                    
                    # Look for likes
                    # Usually "X likes" or a button with count
                    likes_text = el.locator('span:has-text("likes")').first.text_content() if el.locator('span:has-text("likes")').count() > 0 else "0"
                    # Handle "1,234 likes" -> 1234
                    likes_count = 0
                    if likes_text:
                        match = re.search(r'(\d+(?:,\d+)*)', likes_text)
                        if match:
                            likes_count = int(match.group(1).replace(',', ''))

                    if username and comment_text and username != "Verified": # Filter out some noise
                        comments_data.append({
                            "username": username,
                            "comment": comment_text,
                            "likes": likes_count
                        })
                except Exception as e:
                    continue

        except Exception as e:
            print(f"Scraping error: {e}")
        finally:
            browser.close()

    # Deduplicate by (username, comment)
    seen = set()
    unique_comments = []
    for c in comments_data:
        key = (c['username'], c['comment'])
        if key not in seen:
            seen.add(key)
            unique_comments.append(c)

    # Sort by likes descending
    unique_comments.sort(key=lambda x: x['likes'], reverse=True)

    return unique_comments[:10]
