# region Imports
import time
from pathlib import Path

from wplay.utils import browser_config
from wplay.utils.Logger import Logger
from wplay.utils.helpers import profile_photos_path
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def get_profile_photos():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    total_contacts = int(input("Please provide total whatsapp contacts: "))
    loop = round(total_contacts/7)
    images_list =  []
    
    await page.waitForSelector('#pane-side > div:nth-child(1) > div > div > div:nth-child(1) > div > div > div > div > img')

    for c in range(loop):
        for i in range(1, 18):
            selector = f"#pane-side > div:nth-child(1) > div > div > div:nth-child({i}) > div > div > div > div > img"
            try:
                await page.waitForSelector(selector, timeout=2000)
                image_url = await page.evaluate(f'document.querySelector("{selector}").getAttribute("src")')
                print(f"{c}:{i}-{image_url}")
                if image_url not in images_list:
                    images_list.append(image_url)
            except:
                print("No profile image found")
        await page.evaluate("document.querySelector('#pane-side').scrollBy(0, 500)")
  
    for count in range(len(images_list)):
        try:
            viewSource = await page.goto(images_list[count])
            f = open(profile_photos_path / f'{count}.jpg', 'wb')
            f.write(await viewSource.buffer())
            f.close()
        except:
            print("Error saving image")
    
    print("Saved all the images to media_folder.")
    time.sleep(5)
