from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from PIL import Image
import io
from io import BytesIO

def get_browser_driver(browser, size):
    '''
    Returns a valid Selenium WebDriver for the specified browser and window size.

    Args:
    - browser (str): The browser to use. Options are 'chrome', 'firefox', 'safari'.
    - size (tuple): The size of the browser window in the format (width, height).

    Returns:
    - WebDriver object for the specified browser and size.
    '''

    if browser.lower() == 'chrome':
        # Ensure ChromeDriver is installed and in PATH
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)

    elif browser.lower() == 'firefox':
        # Ensure GeckoDriver is installed and in PATH
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options)

    elif browser.lower() == 'safari':
        # Safari WebDriver comes preinstalled on macOS
        driver = webdriver.Safari()

    else:
        raise ValueError(f"Unsupported browser: {browser}")

    # Set browser window size
    driver.set_window_size(*size)

    return driver


def take_screenshot(driver):
    '''
    Takes a screenshot of the entire current page and returns it as a binary file (scrolls if needed).

    Args:
    - driver: Selenium WebDriver object.

    Returns:
    - Binary data of the screenshot image.
    '''
    return driver.get_screenshot_as_png()
    

def stitch_images(img1, img2):
    '''
    stitches two images together
    '''
    # open the images
    img1 = Image.open(io.BytesIO(img1))
    img2 = Image.open(io.BytesIO(img2))

    # get the size of the images
    width1, height1 = img1.size
    width2, height2 = img2.size

    # create a new image with the correct dimensions
    new_img = Image.new('RGB', (width1, height1 + height2))

    # paste the images
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (0, height1))

    # save the new image as a byte array
    img_byte_array = io.BytesIO()
    new_img.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    return img_byte_array


if __name__ == '__main__':
    # open the browser
    driver = get_browser_driver('chrome', (1920, 1080))
    driver.get('https://en.wikipedia.org/wiki/Main_Page')

    # take a screenshot
    screenshot1 = take_screenshot(driver)