from wplay.utils import browser_config
async def recent_chat():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    selector = '#pane-side > div > div > div > div > div > div > div > div > div'
    await page.waitForSelector(selector)
    values = await page.evaluate(f'''() => [...document.querySelectorAll('{selector}')]
                                                    .map(element => element.textContent)''')
    new_values = '\n'.join([' '.join(i) for i in zip(*[iter(values)]*5)])
    print(new_values)
    print("break")
    final = [' '.join(i) for i in zip(*[iter(values)]*5)]
    reversed_list = final[::-1]
    reversed_list = reversed_list[-1:] + reversed_list[:-1]
    print(*reversed_list, sep = "\n")
    #print(reversed_list)