from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils import browser_config
async def change_about():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()

    await page.waitForSelector(whatsapp_selectors_dict['profile_photo_element'], visible=True)
    await page.click(whatsapp_selectors_dict['profile_photo_element'])
    await page.waitForSelector(whatsapp_selectors_dict['about_edit_button_element'])
    await page.click(whatsapp_selectors_dict['about_edit_button_element'])
    for _ in range(140):
        await page.keyboard.press('Backspace')
    status = input("enter: ")
    await page.type(whatsapp_selectors_dict['about_text_area'], status)
    await page.keyboard.press('Enter')
