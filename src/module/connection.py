import requests # type: ignore
from printer import log_msg as log

class headers(dict):
    """
    Custom headers class inheriting from dict. Includes default headers and methods to add or remove headers.
    Default headers include 'User-Agent' and 'Accept-Language' to mimic a real browser.
    Methods:
    - add(key, value): Adds a header key-value pair.
    - remove(key): Removes a header by key, except for necessary headers.
    """
    DEFAULT = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
        }
    
    def __init__(self):
        super().__init__(self.DEFAULT)
        
    def add(self, key, value):
        """Add a header key-value pair."""
        self[key] = value
    
    def remove(self, key):
        """
        Remove a header by key, except for necessary headers.
        To mimic a real browser, 'User-Agent' and 'Accept-Language' cannot be removed.
        """
        if key not in ['User-Agent','Accept-Language']:
            if key in self:
                del self[key]
                return 0 
            else:
                log(f"Invalid key: '{key}'")
        else:
            log(f"Can't remove key: '{key}'. It's necessary.")
            

def connection_test(url:str, headers:headers):
    """
    Tests the connection to a given URL using provided headers.
    Logs the result of the connection test.
    """
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            log("Connection test successful.")
            return True
        else:
            log(f"Connection test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        log(f"Connection test error: {e}")
        return False
    
if __name__ == "__main__":
    # from test.test_config import BASEURL
    # TARGET_URL = BASEURL
    TARGET_URL = "https://www.google.com"

    headers = headers()
    connection_test(TARGET_URL, headers)