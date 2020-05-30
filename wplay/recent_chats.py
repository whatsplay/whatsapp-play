from wplay.utils import browser_config
async def recent_chat():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    selector = '#pane-side > div > div > div > div > div > div > div'
    await page.waitForSelector(selector)
    values = await page.evaluate(f'''() => [...document.querySelectorAll('{selector}')]
                                                    .map(element => element.textContent)''')
    str_list = list(filter(None, values))
    print(str_list)
    b = [s.split('Monday') for s in str_list]
    print(b)
    print("new")
    new=[i.split('Monday', 1)[0] for i in str_list]
    print(new)