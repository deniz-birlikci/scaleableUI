from scraping.scrape import *
from scraping.db import *

def main(url, browsers = ['chrome'], sizes = [(100, 200), (200, 300), (300, 400)]):
    filepaths = []
    for browser in browsers:
        for size in sizes:
            driver = get_browser_driver(browser, size)
            driver.get(url)
            screenshot = take_screenshot(driver)
            filepath = f'{driver.name}_{size[0]}_{size[1]}.png'
            upload_object_to_wasabi(screenshot, filepath)
            filepaths.append(filepath)
            driver.quit()
            print(f'Uploaded {driver.name}_{size[0]}_{size[1]}.png')

    return filepaths

def scrape_list(url, configurations):
    url = 'https://' + url
    filepaths = []
    for c in configurations:
        browser = c['browser'].lower()
        size = (c['width'], c['height'])
        driver = get_browser_driver(browser, size)
        driver.get(url)
        screenshot = take_screenshot(driver)
        filepath = f'{driver.name}_{size[0]}_{size[1]}.png'
        upload_object_to_wasabi(screenshot, filepath)
        filepaths.append(filepath)
        driver.quit()
        print(f'Uploaded {driver.name}_{size[0]}_{size[1]}.png')

    return ['https://s3.us-west-1.wasabisys.com/hackathon/' + f for f in filepaths]



   
if __name__ == '__main__':
    main('https://en.wikipedia.org/wiki/Main_Page')