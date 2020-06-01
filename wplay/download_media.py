# region Imports
from pathlib import Path

from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils.helpers import media_path
from wplay.utils.Logger import Logger
from wplay.utils.helpers import whatsapp_selectors_dict
import time
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def download_media(target):
    page, browser = await browser_config.configure_browser_and_load_whatsapp()

    if target is not None:
        try:
            await target_search.search_and_select_target(page, target)
        except Exception as e:
            print(e)
            await page.reload()
            await target_search.search_and_select_target_without_new_chat_button(
                    page,
                    target
                    )
    else:
        await target_select.manual_select_target(page)

    count = int(input("Count of media you want to download: "))

    # Click on the photo element of the target
    await page.waitForSelector(whatsapp_selectors_dict['target_name_selector'], visible=True)
    await page.evaluate(f'''document.querySelector('{whatsapp_selectors_dict['target_name_selector']}').click()''')

    time.sleep(1)

    # Click on the `Media, Link and Docs` text
    await page.waitForSelector(whatsapp_selectors_dict['media_text'])
    await page.click(whatsapp_selectors_dict['media_text'])

    # Click on the most recent media element
    while True:
        try:
            await page.evaluate(f'''document.querySelector('{whatsapp_selectors_dict['media_images']}').click()''')
            break
        except Exception as e:
            print("", end='')

    media_arr = {'img': [], 'vid': []}

    # Currently downloads the last 50 medias
    for _ in range(count):
        try:
            try:
                # If media is an image
                countTry = 0  # Threshold of how many times to try looking for media
                while True:
                    if countTry > 500:
                        await page.waitForSelector(whatsapp_selectors_dict['left_arrow_button'])

                    img = await page.evaluate(f'''() => [...document.querySelectorAll('{whatsapp_selectors_dict['media_url_img']}')]
                                                        .map(element => element.src)''')
                    if img and len(img) == 2:
                        img = img[-1]
                        if img not in media_arr:
                            media_arr['img'].append(img)
                        break
                    countTry += 1
                    time.sleep(0.3)
            except Exception as e:
                # If media is a video or gif
                countTry = 0
                while True:
                    vid = await page.evaluate(f'''() => [...document.querySelectorAll('{whatsapp_selectors_dict['media_url_vid']}')]
                                                        .map(element => element.src)''')
                    if vid:
                        vid = vid[-1]
                        media_arr['vid'].append(vid)
                        break

            # Go to next media element
            await page.waitForSelector(whatsapp_selectors_dict['left_arrow_button'])
            await page.evaluate(f'''document.querySelector('{whatsapp_selectors_dict['left_arrow_button']}').click()''')
            time.sleep(0.5)

        except Exception as e:
            print(e)

    count = 0
    newPage = await browser.newPage()
    # Downloading media
    for image in media_arr['img']:
        try:
            count += 1
            print(image)
            viewSource = await newPage.goto(image)
            f = open(media_path / f'{count}.jpg', 'wb')
            f.write(await viewSource.buffer())
            f.close()
        except Exception as e:
            print("Error saving image", e)

    for video in media_arr['vid']:
        try:
            count += 1
            viewSource = await newPage.goto(video)
            f = open(media_path / f'{count}.mp4', 'wb')
            f.write(await viewSource.buffer())
            f.close()
        except Exception as e:
            print("Error saving video", e)

    print("Saved the media to the 'media' dir")
    time.sleep(10)
