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