from wplay.utils import browser_config
async def recent_chat():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    selector = '#pane-side > div > div > div > div > div > div > div > div > div'
    await page.waitForSelector(selector)
    values = await page.evaluate(f'''() => [...document.querySelectorAll('{selector}')]
                                                    .map(element => element.textContent)''')
    print(values)
    new_values = '\n'.join([' '.join(i) for i in zip(*[iter(values)]*5)])
    print(new_values)