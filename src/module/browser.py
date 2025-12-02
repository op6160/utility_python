from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def get_html_content(url: str, load_time: int = 3) -> str:
    """
    Execute chrome browser (with auto install) and retrieve html content.

    Parameters:
    url (str): target url to retrieve html content
    load_time (int): time to wait for loading data (js acting)

    Returns:
    str: html content retrieved from the target url
    """

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
        driver.get(url)
        time.sleep(load_time)
        return driver.page_source