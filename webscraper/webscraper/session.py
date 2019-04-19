import datetime

class Session:
    def __init__(self):
        self.start_datetime = "not set"
        self.end_datetime = "not set"

    def update_start_datetime(self):
        self.start_datetime = datetime.datetime.now().isoformat()

    def update_end_datetime(self):
        self.end_datetime = datetime.datetime.now().isoformat()

    def __str__(self):
        return ("{{"
            "start_datetime={}, "
            "end_datetime={}"
        "}}").format(
            self.start_datetime, 
            self.end_datetime 
        )   

    def __repr__(self):
        return self.__str__()
