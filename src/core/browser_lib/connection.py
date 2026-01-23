from .headers import headers

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