from datetime import datetime

class TimeAlias:
    """
    A class to generate formatted current date and time strings.
    """
    MAP = { "year":   "%Y",
            "month":  "%m",
            "day":    "%d",
            "hour":   "%H",
            "minute": "%M",
            "second": "%S"
           }
    date_distributer = "-"
    date_times_distributer = " "
    times_distributer = ":"
    
    def __init__(self, date=True, time=True):
        self._date = date
        self._time = time
        self.set_msg()

    def __call__(self):
        return self._return(self.msg)

    def __str__(self):
        return self._return(self.msg)

    def _return(self, time_message):
        return datetime.now().strftime(time_message)

    def set_msg(self):
        """
        Set the message format based on the current settings.
        """
        date_msg = f"{self.MAP['year']}{self.date_distributer}{self.MAP['month']}{self.date_distributer}{self.MAP['day']}"
        times_msg = f"{self.MAP['hour']}{self.times_distributer}{self.MAP['minute']}{self.times_distributer}{self.MAP['second']}"
        msg = ""
        if self._date:
            msg += date_msg
        if self._date and self._time:
            msg += self.date_times_distributer
        if self._time:
            msg += times_msg
        self.msg = msg
        return 

    @property
    def date_dist(self):
        """
        Get or set the date distributer. ex) "-" : 2025-11-25
        """
        return self.date_distributer
    @date_dist.setter
    def date_dist(self, distributer:str):
        self.date_distributer = distributer
        self.set_msg()
        return

    @property
    def times_dist(self):
        """
        Get or set the times distributer. ex) ":" : 17:53:39
        """
        return self.times_distributer
    @times_dist.setter
    def times_dist(self, distributer:str):
        self.times_distributer = distributer
        self.set_msg()
        return

    @property
    def date_times_dist(self):
        """
        Get or set the date-times distributer. ex) " " : 2025-11-25 17:53:39
        """
        return self.date_times_distributer
    @date_times_dist.setter
    def date_times_dist(self, distributer:str):
        self.date_times_distributer = distributer
        self.set_msg()
        return

# usage example
__star = TimeAlias()
__star.date_times_dist = "*"
__star.date_dist = "*"
__star.times_dist = "*"

# basic usecase
detail = TimeAlias()
date = TimeAlias(True, False)
times = TimeAlias(False, True)

if __name__ == "__main__":
    print(f"__star: {__star}")
    
    print(f"detail: {detail}")
    print(f"date: {date}")
    print(f"times: {times}")