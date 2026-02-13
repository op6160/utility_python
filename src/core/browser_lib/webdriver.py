from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
import time
import random
from typing import Callable, Any

USER_AGENTS = [
    # 모바일 에이전트
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36',
    # 데스크톱 에이전트
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

def _create_driver_options() -> Options:
    options = Options()

    # set headless
    options.add_argument("--headless=new") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # set clean work    
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920,1080") # 가상 화면 크기 설정 (탐지 회피 도움)

    # Add options to avoid anti-bot detection    
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Add random user agent
    selected_agent = random.choice(USER_AGENTS)
    options.add_argument(f"user-agent={selected_agent}")
    return options

def _run_browser_task(url: str, load_time: int, callback: Callable[[webdriver.Chrome], Any]) -> Any:
    options = _create_driver_options()
    wait_time = random.uniform(float(load_time) * 1.1, float(load_time) * 2.0)
    
    driver = None
    try:
        # x86_64 server webdriver-manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except OSError as e:
        # ARM64 server webdriver-manager
        if e.errno == 8:
            fallback_service = Service("/usr/bin/chromedriver")
            driver = webdriver.Chrome(service=fallback_service, options=options)
        else:
            raise e
    except Exception as e:
        raise e

    with driver:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

        driver.get(url)
        time.sleep(wait_time)
        
        return callback(driver)


def get_driver_content(url: str, load_time: int = 3) -> str:
    """
    Execute chrome browser (with auto install) and retrieve html content.
    """
    return _run_browser_task(url, load_time, lambda driver: driver.page_source)

def get_driver_mhtml(url: str, load_time: int = 3) -> str:
    """
    Execute chrome browser and retrieve mhtml content using CDP.
    """
    def _get_mhtml(driver):
        res = driver.execute_cdp_cmd("Page.captureSnapshot", {"format": "mhtml"})
        return res['data']
    
    return _run_browser_task(url, load_time, _get_mhtml)