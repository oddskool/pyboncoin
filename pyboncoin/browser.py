import asyncio
import random

from pyppeteer import launch


async def crawl(url):
    browser = await launch(headless=False, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto(url)

    # needed for proper image loading
    await asyncio.sleep(random.randint(1, 3))
    await page.evaluate('''() => {
                window.scrollBy(0, window.innerHeight);
            }''')
    await asyncio.sleep(random.randint(1, 3))
    await page.evaluate('''() => {
                window.scrollBy(0, window.innerHeight);
            }''')
    await asyncio.sleep(random.randint(1, 3))
    await page.evaluate('''() => {
                window.scrollBy(0, window.innerHeight);
            }''')
    await asyncio.sleep(random.randint(1, 3))

    content = await page.evaluate('document.body.innerHTML', force_expr=True)
    return content
