from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random

USER_AGENTS = [
    # 모바일 에이전트
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36',
    # 데스크톱 에이전트
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]


def get_html_content(url: str, load_time: int = 3) -> str:
    """
    Execute chrome browser (with auto install) and retrieve html content.
    """
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

    wait_time = random.uniform(float(load_time) * 1.1, float(load_time) * 2.0)

    # 드라이버 실행 (여기서 딱 한 번만 실행)
    service = Service(ChromeDriverManager().install())
    with webdriver.Chrome(service=service, options=options) as driver:
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            """
        })

        driver.get(url)
        time.sleep(wait_time)
        
        return driver.page_source